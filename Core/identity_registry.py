You are implementing a PASSIVE IDENTITY REGISTRY.

CRITICAL:

- DO NOT modify vortex
- DO NOT modify epistemic layer
- DO NOT introduce feedback
- DO NOT introduce control logic
- DO NOT optimize anything

This layer is READ-ONLY.

--------------------------------------------------

GOAL

Create identity layer for simulations.

--------------------------------------------------

REQUIREMENTS

1. CREATE:

compute_phi_id(phi)

Returns:
SHA256 hash of:

- Sigma
- R matrix

--------------------------------------------------

2. CREATE:

compute_run_id(phi_id, states)

Returns:
SHA256 hash of:

- phi_id
- trajectory states

--------------------------------------------------

3. CREATE:

create_registry_entry(run_output)

Input = output of run()

Returns:

{
  "phi_id": str,
  "run_id": str,
  "topology_hash": str,
  "epistemic_hash": str,
  "steps": int
}

--------------------------------------------------

4. EPISTEMIC HASH

epistemic_hash = SHA256(epistemic.proof)

--------------------------------------------------

5. STRICT RULES

- NO mutation of inputs
- NO filtering
- NO validation
- NO decisions

--------------------------------------------------

6. OUTPUT

Return ONLY:

registry.py

--------------------------------------------------

7. DO NOT:

- import external libs
- introduce classes unless necessary
- add persistence
- add databases

--------------------------------------------------

If unsure:
leave TODO
