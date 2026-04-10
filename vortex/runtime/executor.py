from core.vortex import run_vortex
from core.vnal_guard import validate_output

result = run_vortex(input_data)

validate_output(result)

return result
