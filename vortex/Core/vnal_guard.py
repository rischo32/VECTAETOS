# vnal_guard.py

def validate_output(output):
    # 1. zákaz single answer
    if isinstance(output, dict) and "best" in output:
        raise Exception("VNAL violation: best answer not allowed")

    # 2. zákaz ranking
    if isinstance(output, list):
        for item in output:
            if "score" in item or "rank" in item:
                raise Exception("VNAL violation: ranking detected")

    # 3. povinná neistota
    if "uncertainty" not in str(output):
        raise Exception("VNAL violation: missing uncertainty")

    return True
