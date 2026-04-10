# vnal_guard.py

from typing import Any, List, Dict


class VNALViolation(Exception):
    pass


def _check_no_best(output: Any):
    if isinstance(output, dict) and "best" in output:
        raise VNALViolation("VNAL: best answer not allowed")


def _check_no_ranking(output: Any):
    if isinstance(output, list):
        for item in output:
            if isinstance(item, dict):
                if "score" in item or "rank" in item:
                    raise VNALViolation("VNAL: ranking detected")


def _check_uncertainty(output: Any):
    """
    Očakávame explicitnú štruktúru:
    {
        "type": "...",
        "uncertainty": float | dict
    }
    """
    if isinstance(output, dict):
        if "uncertainty" not in output:
            raise VNALViolation("VNAL: missing uncertainty field")
    else:
        raise VNALViolation("VNAL: output must be dict")


def _check_qe(output: Dict):
    """
    QE je legit stav → musí byť explicitný
    """
    if output.get("type") == "QE":
        if "reason" not in output:
            raise VNALViolation("VNAL: QE missing reason")
        return True
    return False


def validate_output(output: Any) -> bool:
    _check_no_best(output)
    _check_no_ranking(output)

    is_qe = _check_qe(output)

    # QE môže mať inú štruktúru, ale stále musí niesť uncertainty
    _check_uncertainty(output)

    return True
