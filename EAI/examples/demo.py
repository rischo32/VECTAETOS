from implementation import run_eai

def system(x):
    return str(x[::-1])  # simple reversible system


transforms = [
    lambda x: x[::-1],
    lambda x: x[:len(x)//2],
    lambda x: x + x
]

inputs = [
    "test system",
    "vectaetos",
    "epistemic",
    "audit"
]

result = run_eai(system, inputs, transforms)

print(result)
