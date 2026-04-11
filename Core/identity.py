# Core/identity.py


class VectaetosIdentity:

    MIN_HUMILITY = 0.4

    @staticmethod
    def validate(ep: dict):

        h = ep.get("topological_humility", 0.0)
        integrity = ep.get("integrity", 1)
        dominant = ep.get("dominant_mode", False)

        if integrity == 0:
            return "INVALID"

        if dominant:
            return "DEGENERATE"

        if h < VectaetosIdentity.MIN_HUMILITY:
            return "NON_VECTAETOS"

        return "VECTAETOS"
