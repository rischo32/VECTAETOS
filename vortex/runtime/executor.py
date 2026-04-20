from Core.vortex import run_vortex
from Core.vnal_guard import validate_output

result = run_vortex(input_data)

validate_output(result)

return result
