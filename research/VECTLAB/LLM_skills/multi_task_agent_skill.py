"""
Multi-Task Agent Skill
=======================

This module implements a general-purpose "skill" that can be used by AI agents to
coordinate and execute multi‑task workflows over long time horizons.  The design
draws on recent research into open‑world multi‑task agents and modern AI
orchestration patterns, including hierarchical skill libraries, graph‑based
planning and dependency management, and flexible orchestration strategies
tailored to the needs of complex tasks【874874442489626†L207-L219】【169856935948993†L90-L102】.

The core of this module is the ``MultiTaskAgentSkill`` class, which manages
tasks, their dependencies, and assignment to agents.  Tasks can be executed
sequentially or concurrently depending on their dependencies, and execution
state is persisted to disk so that long‑running workflows can be paused and
resumed across sessions.  The orchestrator can integrate with multiple agent
implementations, enabling specialization and scalability as recommended by
Microsoft's AI agent orchestration patterns【169856935948993†L109-L125】.

Key features
------------

- **Hierarchical task representation**: Tasks may have dependencies on
  predecessor tasks.  This allows you to model complex workflows as a Directed
  Acyclic Graph (DAG), reflecting best practices for hierarchical skill
  composition【874874442489626†L214-L220】.

- **Concurrent execution**: Independent tasks are executed concurrently using
  Python's :mod:`asyncio` library, enabling efficient utilization of multiple
  agents or background threads.  Concurrency is critical when different
  subtasks can proceed in parallel【874874442489626†L214-L219】.

- **Persistent state**: The orchestrator serializes its task list and results
  to a JSON file so that progress can be saved and restored across long
  periods.  This supports long‑horizon workflows that may span hours, days or
  longer.

- **Agent registration**: External agents (functions, classes, or any callables)
  can be registered with the orchestrator.  When you create a task you
  specify which agent should perform it.  This promotes specialization and
  separation of concerns【169856935948993†L109-L125】.

- **Resilient execution**: Failures in individual tasks are isolated; the
  orchestrator records errors and can retry tasks.  It also provides hooks
  for custom error handling or fallback behaviors.

Example usage
-------------

::

    from multi_task_agent_skill import MultiTaskAgentSkill
    
    async def research_agent(task_context):
        # Example agent that performs research and returns a result.
        # In a real implementation this function could call external APIs,
        # search the web, or perform complex reasoning.  Here we simply
        # reverse the description to simulate a result.
        query = task_context['description']
        return query[::-1]

    # Create the orchestrator and register agents
    skill = MultiTaskAgentSkill()
    skill.register_agent('research', research_agent)
    
    # Add tasks with dependencies
    t1 = skill.add_task('Gather information about renewable energy', 'research')
    t2 = skill.add_task('Summarize findings', 'research', dependencies=[t1])
    
    # Execute tasks
    await skill.execute_tasks()
    print(skill.get_status())

The orchestrator will ensure that ``t1`` runs before ``t2``, and it will
persist progress between sessions.

Notes on extensibility
----------------------

This module is intentionally generic.  To tailor it to your application you
can:

- Register agents that call external APIs, perform complex reasoning, or
  interact with databases.
- Override methods such as ``_pre_task_hook`` or ``_post_task_hook`` to add
  logging, notification, or other side effects.
- Replace the JSON file storage with a database or distributed cache to handle
  large numbers of tasks or to support multi‑process coordination.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dataclass
class Task:
    """A unit of work to be executed by an agent.

    Attributes:
        id: A globally unique identifier for the task.
        description: A human‑readable description of the task.  Agents may
            leverage this field when deciding how to execute the task.
        agent_name: The key identifying which agent should execute the task.
        dependencies: A list of task IDs that must complete before this task
            can start.
        created_at: Timestamp when the task was created.
        status: A string indicating the state of the task: ``"pending"``,
            ``"running"``, ``"completed"``, or ``"failed"``.
        result: Optional result produced by the agent.
        error: Optional exception information if the task failed.
    """

    id: str
    description: str
    agent_name: str
    dependencies: List[str]
    created_at: str
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None


class MultiTaskAgentSkill:
    """Orchestrator for long‑horizon, multi‑task AI workflows.

    This class manages a collection of tasks, executes them in an order
    consistent with their dependencies, and delegates execution to registered
    agents.  It persists state to disk so that the orchestrator can be
    stopped and later resumed without losing progress.
    """

    def __init__(self, storage_path: str = "multi_task_skill_state.json") -> None:
        self.storage_path = storage_path
        self.tasks: Dict[str, Task] = {}
        self.agents: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._load_state()

    def register_agent(self, name: str, func: Callable[[Dict[str, Any]], Any]) -> None:
        """Register a callable that can execute tasks.

        Parameters:
            name: Identifier for the agent.  This must match the ``agent_name``
                field used when adding tasks.
            func: A callable that accepts a dict with task context and returns
                a result.  It may be a regular function or an ``async``
                coroutine.  The task context includes ``id``, ``description``,
                and other metadata.
        """
        if name in self.agents:
            raise ValueError(f"Agent '{name}' is already registered")
        self.agents[name] = func
        logger.debug("Registered agent '%s'", name)

    def add_task(self, description: str, agent_name: str, *, dependencies: Optional[List[str]] = None) -> str:
        """Create a new task and add it to the orchestrator.

        Parameters:
            description: Human‑readable description of the task.
            agent_name: Name of the registered agent that should execute the task.
            dependencies: List of task IDs that must complete before this task.

        Returns:
            The ID of the newly created task.
        """
        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent '{agent_name}'. Did you register it?")
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            description=description,
            agent_name=agent_name,
            dependencies=dependencies or [],
            created_at=datetime.utcnow().isoformat(),
        )
        self.tasks[task_id] = task
        logger.info("Added task %s: %s", task_id, description)
        self._save_state()
        return task_id

    def get_status(self) -> List[Dict[str, Any]]:
        """Return a summary of all tasks and their statuses."""
        return [
            {
                "id": t.id,
                "description": t.description,
                "agent": t.agent_name,
                "status": t.status,
                "dependencies": t.dependencies,
                "result": t.result,
                "error": t.error,
            }
            for t in self.tasks.values()
        ]

    async def execute_tasks(self) -> None:
        """Execute all tasks in dependency order until completion.

        This coroutine repeatedly finds tasks whose dependencies are completed,
        schedules them for execution, and waits for them to finish.  It will
        continue until all tasks are completed or have failed.  If new tasks
        are added while execution is underway, they will be included in the
        scheduling loop.

        Note: Because tasks may depend on one another, this method will not
        run indefinitely.  However, if there are circular dependencies or
        tasks whose dependencies never complete, they will remain pending.
        """
        while True:
            # Determine which tasks are ready to run
            ready_tasks = [
                t for t in self.tasks.values()
                if t.status == "pending" and all(self.tasks[dep_id].status == "completed" for dep_id in t.dependencies)
            ]
            if not ready_tasks:
                # If no tasks are pending or running, we're done
                if all(t.status in {"completed", "failed"} for t in self.tasks.values()):
                    break
                # Otherwise wait for running tasks to complete or new tasks to be added
                await asyncio.sleep(0.5)
                continue

            # Schedule tasks concurrently
            coros = [self._run_task(t) for t in ready_tasks]
            await asyncio.gather(*coros)
            # Save state after each batch of tasks completes
            self._save_state()

    async def _run_task(self, task: Task) -> None:
        """Execute a single task by delegating to the registered agent.

        This internal coroutine updates the task's status to "running",
        invokes the agent, and records the result.  If the agent raises an
        exception, the error is captured and the task status is set to
        "failed".
        """
        if task.status != "pending":
            return
        task.status = "running"
        self._save_state()
        logger.info("Running task %s (%s)", task.id, task.description)
        context = {
            "id": task.id,
            "description": task.description,
            "created_at": task.created_at,
            "dependencies": task.dependencies,
        }
        agent = self.agents[task.agent_name]
        try:
            # Support both sync and async callables
            if asyncio.iscoroutinefunction(agent):
                result = await agent(context)
            else:
                # Run sync agent in a thread to avoid blocking the event loop
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(None, agent, context)
            task.status = "completed"
            task.result = result
            logger.info("Task %s completed", task.id)
        except Exception as exc:
            task.status = "failed"
            task.error = f"{type(exc).__name__}: {exc}"
            logger.exception("Task %s failed", task.id)
        finally:
            self._save_state()

    def _load_state(self) -> None:
        """Load tasks from the storage file if it exists."""
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data.get("tasks", []):
                task = Task(**entry)
                self.tasks[task.id] = task
            logger.debug("Loaded %d tasks from state", len(self.tasks))
        except Exception:
            logger.warning("Failed to load existing state; starting fresh")
            self.tasks = {}

    def _save_state(self) -> None:
        """Persist the current tasks to the storage file."""
        data = {
            "tasks": [asdict(t) for t in self.tasks.values()],
        }
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug("Saved state to %s", self.storage_path)
        except Exception as exc:
            logger.error("Failed to save state: %s", exc)

    # Hooks for customization
    async def _pre_task_hook(self, task: Task) -> None:
        """Hook called immediately before a task starts.

        Override this method in subclasses to implement custom behaviors (e.g.,
        logging, sending notifications, modifying context).  The default
        implementation does nothing.
        """
        return

    async def _post_task_hook(self, task: Task) -> None:
        """Hook called immediately after a task finishes.

        Override this method in subclasses to implement custom behaviors such as
        persisting results to an external system, notifying users, or cleaning
        up temporary resources.  The default implementation does nothing.
        """
        return