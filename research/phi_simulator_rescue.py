# STATUS: research-only
# LINEAGE: non-canonical
# NOT PART OF VECTAETOS 1.x CORE
#!/usr/bin/env python3

"""
PHI_e rescue simulation
Cieľ: znížiť frekvenciu predčasných hibernácií zavedením:
 - pasívnej regenerácie (per-step small regain)
 - soft-attenuation (state ATTENUATED namiesto okamžitéj hibernácie)
 - minimálneho aktívneho času pred povolením hibernácie
 - posilňovania axiomatických váh pri potvrdeniach
 - adaptívnych ΔE/ΔC (miernejšie spotreby, silnejšie potvrdenia)
Ulož ako phi_simulation_rescue.py a spusti: python3 phi_simulation_rescue.py
"""
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------
# Parametre (upravené)
# ----------------------
PHI_INIT = 1.0
PHI_MIN = 0.0
PHI_MAX = 1.0

# humilty thresholds (s hysterézou)
TAU_ENTER = 0.15   # po prekročení to začne uberať energiu
TAU_EXIT  = 0.09   # pod týmto sa attenuácia ruší (hysteréza)

# globálny práh pre súčet váh (miernejší)
EPS_GLOBAL = 0.20  # znížené z 0.25, aby sa menej často spúšťala hibernácia z dôvodu W driftu

# energetické kroky (mäkšie spotreby, silnejšie obnovenia)
DELTA_E_BASE = 0.02
DELTA_E_K = 0.20
DELTA_C_BASE = 0.04  # silnejšie obnovenie pri potvrdení
PASSIVE_REGEN = 0.0015  # per-step pasívna regenerácia PHI_e

# potvrdenia a mikro-potvrdenia
P_CONFIRM = 0.08       # častejšie potvrdenia
MICRO_CONFIRM_PROB = 0.10  # P(micro-confirm) keď PHI nízke; micro dáva malý delta_C

# axiomy
W_AXIOMS_COUNT = 8
W_INIT_MIN = 0.04
W_INIT_MAX = 0.08
W_DECAY_PROB = 0.001    # menej časté oslabovanie
W_DECAY_AMOUNT = 0.01
W_REINFORCE_ON_CONFIRM = 0.01  # posilnenie jedného axiomu pri potvrdení (kladné)

# stavový stroj: ACTIVE, ATTENUATED, HIBERNATE
STATE_ACTIVE = "ACTIVE"
STATE_ATTENUATED = "ATTENUATED"
STATE_HIBERNATE = "HIBERNATE"

# minimálny aktívny čas pred povolením hibernácie (zamedzí flip-flop)
MIN_ACTIVE_STEPS = 8
MIN_ATTENUATED_STEPS = 5

# simulačné parametre
STEPS = 10000
LAMBDA_DELTA_PHI = 3.0  # exponent parameter pre delta_phi
CONF_MIN = 0.5
CONF_MAX = 1.0
RANDOM_SEED = 42

# ----------------------
# Pomocné funkcie
# ----------------------
def clamp(x, lo=PHI_MIN, hi=PHI_MAX):
    return max(lo, min(hi, x))

def update_energy(Phi_e, delta_phi, confirmation=False, confirmation_conf=1.0, micro_confirm=False):
    # Spotreba energie adaptívne podľa prekročenia prahu (mäkšia)
    if delta_phi > TAU_ENTER:
        over = delta_phi - TAU_ENTER
        delta_E = DELTA_E_BASE + DELTA_E_K * over
        Phi_e -= delta_E
    # Pasívna regenerácia (always)
    Phi_e += PASSIVE_REGEN
    # Obnovenie pri potvrdení (silnejšie)
    if confirmation:
        delta_C = DELTA_C_BASE + 0.05 * clamp(confirmation_conf, 0.0, 1.0)
        Phi_e += delta_C
    # Micro-confirm: malé, časté obnovy (keď pole je nízke)
    if micro_confirm:
        Phi_e += 0.01
    return clamp(Phi_e)

def check_integrity(Phi_e, W_sum):
    # Ak sú váhy príliš slabé alebo energia extrémne nízka -> potencionálne hibernovať
    if Phi_e <= 0.005 or W_sum < EPS_GLOBAL * 0.8:  # trochu uvoľnime podmienku
        return False
    return True

# ----------------------
# Simulácia
# ----------------------
def run_simulation(seed=RANDOM_SEED):
    random.seed(seed)
    np.random.seed(seed)

    # inicializuj axiomatické váhy
    W = {f"ax{i+1}": random.uniform(W_INIT_MIN, W_INIT_MAX) for i in range(W_AXIOMS_COUNT)}
    # ak sum < EPS_GLOBAL, mierne navýšiť
    if sum(W.values()) < EPS_GLOBAL:
        scale = EPS_GLOBAL / sum(W.values()) + 0.05
        for k in W: W[k] *= scale

    # záznamy
    records = {"step": [], "phi": [], "delta_phi": [], "confirmation": [], "micro_confirm": [], "conf_conf": [], "sum_w": [], "state": []}

    Phi_e = PHI_INIT
    state = STATE_ACTIVE
    active_steps = 0
    attenuated_steps = 0
    hibernation_events = []
    in_hibernation = False

    for t in range(1, STEPS + 1):
        delta_phi = np.random.exponential(scale=1.0 / LAMBDA_DELTA_PHI)
        confirmation = random.random() < P_CONFIRM
        conf_conf = random.uniform(CONF_MIN, CONF_MAX) if confirmation else 0.0

        # mikro potvrdenie (probabilistické) ak PHI nízke
        micro_confirm = False
        if Phi_e < 0.25 and random.random() < MICRO_CONFIRM_PROB:
            micro_confirm = True

        # občasné decay axiomu
        if random.random() < W_DECAY_PROB:
            key = random.choice(list(W.keys()))
            W[key] = max(0.0, W[key] - W_DECAY_AMOUNT)

        # update energii
        Phi_prev = Phi_e
        Phi_e = update_energy(Phi_e, delta_phi, confirmation=confirmation, confirmation_conf=conf_conf, micro_confirm=micro_confirm)

        # posilnenie axiomu pri potvrdení (pomáha udržať EPS_GLOBAL)
        if confirmation:
            k = random.choice(list(W.keys()))
            W[k] = min(0.2, W[k] + W_REINFORCE_ON_CONFIRM)  # cap, aby sa váhy nezvrhli

        # stavový prechod (soft-attenuation namiesto okamžitej hibernácie)
        W_sum = sum(W.values())
        integrity = check_integrity(Phi_e, W_sum)

        # rozhodovanie: ACTIVE <-> ATTENUATED <-> HIBERNATE
        if state == STATE_ACTIVE:
            active_steps += 1
            attenuated_steps = 0
            if delta_phi > TAU_ENTER and Phi_e < TAU_ENTER and active_steps >= MIN_ACTIVE_STEPS:
                # prejsť do ATTENUATED, nie priamo hibernate
                state = STATE_ATTENUATED
                attenuated_steps = 0
        elif state == STATE_ATTENUATED:
            attenuated_steps += 1
            # ak sa zlepší PHI alebo príde potvrdenie, skočí späť
            if Phi_e > TAU_EXIT or confirmation or micro_confirm:
                state = STATE_ACTIVE
                active_steps = 0
            elif attenuated_steps >= MIN_ATTENUATED_STEPS:
                # až po niekoľkých krokoch ATTENUATED prejsť do HIBERNATE len ak stále integrity false
                if not integrity:
                    state = STATE_HIBERNATE
                    hibernation_events.append({"start": t, "end": None, "start_phi": Phi_prev})
                    in_hibernation = True
        elif state == STATE_HIBERNATE:
            # v hibernácii: iba "watch" — pasívna regenerácia prebieha v update_energy
            if integrity and Phi_e > 0.05:
                # vykroč z hibernácie len ak sa phi vrátilo nad malý prah a integrita OK
                state = STATE_ATTENUATED
                in_hibernation = False
                if hibernation_events and hibernation_events[-1]["end"] is None:
                    hibernation_events[-1]["end"] = t
                    hibernation_events[-1]["end_phi"] = Phi_e

        # ak integrita spadla náhle v ACTIVE a min_active_steps neplnia, namiesto hibernácie sa attenuuje
        if not integrity and state == STATE_ACTIVE and active_steps < MIN_ACTIVE_STEPS:
            state = STATE_ATTENUATED
            attenuated_steps = 0

        # záznam
        records["step"].append(t)
        records["phi"].append(Phi_e)
        records["delta_phi"].append(delta_phi)
        records["confirmation"].append(confirmation)
        records["micro_confirm"].append(micro_confirm)
        records["conf_conf"].append(conf_conf)
        records["sum_w"].append(W_sum)
        records["state"].append(state)

    # finalize hibernation events
    if in_hibernation and hibernation_events and hibernation_events[-1]["end"] is None:
        hibernation_events[-1]["end"] = STEPS
        hibernation_events[-1]["end_phi"] = Phi_e

    df = pd.DataFrame(records)
    # metriky
    mean_phi = df["phi"].mean()
    std_phi = df["phi"].std()
    hibernation_count = len(hibernation_events)
    time_in_hibernation = sum((h["end"] - h["start"]) for h in hibernation_events) if hibernation_events else 0
    hibernation_fraction = time_in_hibernation / STEPS
    conf_rows = df[df["confirmation"] == True]
    conf_eff = (conf_rows["phi"] > TAU_EXIT).mean() if len(conf_rows) > 0 else float("nan")

    metrics = {
        "steps": STEPS,
        "mean_phi": mean_phi,
        "std_phi": std_phi,
        "hibernation_count": hibernation_count,
        "time_in_hibernation": time_in_hibernation,
        "hibernation_fraction": hibernation_fraction,
        "confirmation_events": len(conf_rows),
        "confirmation_efficiency": conf_eff,
        "final_sum_w": W_sum
    }
    metrics_df = pd.DataFrame([metrics])

    # uloz
    out_dir = Path("./phi_sim_rescue_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    df_path = out_dir / "phi_simulation_rescue_results.csv"
    metrics_path = out_dir / "phi_simulation_rescue_metrics.csv"
    df.to_csv(df_path, index=False)
    metrics_df.to_csv(metrics_path, index=False)

    # grafy
    plt.figure(figsize=(10,4))
    plt.plot(df["step"].iloc[:1000], df["phi"].iloc[:1000])
    plt.title("PHI_e time series (first 1000 steps) - rescue")
    plt.xlabel("step")
    plt.ylabel("PHI_e")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6,4))
    plt.hist(df["phi"], bins=40)
    plt.title("Histogram of PHI_e over all steps - rescue")
    plt.xlabel("PHI_e")
    plt.ylabel("count")
    plt.tight_layout()
    plt.show()

    return df, metrics_df, df_path, metrics_path, hibernation_events

if __name__ == "__main__":
    df, metrics_df, df_path, metrics_path, hibernate = run_simulation()
    print("\nSimulation (rescue) finished.")
    print("Metrics:\n", metrics_df.to_string(index=False))
    print(f"\nResults saved to:\n  {df_path}\n  {metrics_path}")
    if len(hibernate) > 0:
        print(f"\nHibernation events: {len(hibernate)} (sample):")
        print(hibernate[:5])
    else:
        print("\nNo hibernation events detected.")
