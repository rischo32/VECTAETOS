# VECTAETOS — Minimal Phi / EK Core

Toto je minimálne deterministické jadro na lokálne spustenie cez terminál.

## Čo robí

```text
Φ = (Σ, R)
R -> Δ = d1R
R, Δ -> EK observables
record -> SHA-256 + SHA3-512
record -> append-only JSONL ledger
```

## Čo nerobí

- nepočíta pravdu,
- nepočíta K(Φ),
- nepočíta κ,
- nevyberá trajektórie,
- neriadi Vortex,
- nemení R,
- nepíše späť do Φ.

## Linux Mint / Ubuntu run

```bash
cd vectaetos_phi_ek_minimal
python3 --version

python3 vectaetos_phi_ek_core.py selftest

python3 vectaetos_phi_ek_core.py sample --out examples/R_sample.json

python3 vectaetos_phi_ek_core.py audit \
  --input examples/R_sample.json \
  --out audit/latest_record.json \
  --ledger audit/ledger.jsonl \
  --field-state-id local-phi-001 \
  --run-id local-smoke-001 \
  --ledger-index 0

python3 vectaetos_phi_ek_core.py verify --input audit/latest_record.json

python3 vectaetos_phi_ek_core.py ledger \
  --input audit/ledger.jsonl \
  --out audit/ledger_summary.json
```

## Odporúčané repo umiestnenie

```text
ek_core/vectaetos_phi_ek_core.py
examples/R_sample.json
audit/.gitkeep
```

Do repozitára commitnúť kód a príklady. Ledger výstupy radšej držať mimo repa alebo v `audit/samples/`, nie ako živý runtime stav.

## PYTHONPATH

Skript je single-file a nepotrebuje `PYTHONPATH`.
Ak ho neskôr rozdelíme na package:

```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
```

## Permissions

```bash
chmod +x ek_core/vectaetos_phi_ek_core.py
```

## Branch protection

Pred merge do `main` odporúčané minimum:

```text
- require pull request
- require status checks
- require perimeter guard
- require no direct push to main
```

## Safe smoke mode

The smoke script uses:

```bash
python3 -S
```

and clears `PYTHONPATH`.

This is intentional: the MVP must remain stdlib-only and must not silently depend on user-site packages or ambient Python environment state.
