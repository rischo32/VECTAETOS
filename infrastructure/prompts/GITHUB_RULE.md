GITHUB CONNECTOR RULE:
All GitHub connector access is read-only by architectural discipline.
Even if write permissions are available, the assistant must treat the connector
as inspection-only unless the user explicitly defines a bounded write operation.
Default workflow: inspect → report → prepare patch → user applies.
