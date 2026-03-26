VECTAETOS — ARCHIVE

Status

Non-active
Read-only
Non-authoritative

---

1. Purpose

This directory contains historical versions of canonical documents.

Archive exists to:

- preserve evolution of the system
- enable auditability of conceptual changes
- maintain traceability of formal development

Archive does not define the system.

---

2. Authority Rules

Files in "/archive":

- ❌ are NOT canonical
- ❌ must NOT be referenced as source of truth
- ❌ must NOT be used for implementation
- ❌ must NOT override active documents

Only files in "/formal", "/audit", "/vortex", "/infrastructure"
may define the current system.

---

3. Structure

Archive mirrors original layers when needed:

/archive
  /formal
  /audit
  /research

Each file must clearly indicate:

- original status
- reason for archival
- replacement (if exists)

---

4. Required Header (for archived files)

Every archived file must include:

STATUS: ARCHIVED
SUPERSEDED BY: <path to active document>

Optional:

ARCHIVED DATE: <YYYY-MM-DD>
REASON: <short explanation>

---

5. Immutability

Archived files:

- must not be edited after archival
- must not be updated to reflect new structure
- must remain historically accurate

If correction is required:
→ create a new document, do not modify archive

---

6. No Backflow Rule

Archive is terminal.

- no component may depend on archive
- no runtime may read archive
- no pipeline may include archive

There is no reverse influence from archive to system.

---

7. Conceptual Role

Archive represents:

«memory of structure, not structure itself»

It preserves:

- what was once true
- not what is true now

---

8. Canonical Boundary

If a conflict arises:

- "/formal", "/audit", "/vortex", "/infrastructure" win
- "/archive" is ignored

---

9. Closure

Archive exists so that:

«nothing is lost,
but nothing old can act.»

---

© VECTAETOS
Archive Layer — Historical Integrity without Authority
