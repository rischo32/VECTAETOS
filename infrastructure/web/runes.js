/* =========================================
   VECTAETOS — Rune Projection Module
   Descriptive, Ephemeral, Non-Semantic
   ========================================= */

/*
RUNES:
- are NOT symbols with meaning
- are NOT icons
- are NOT readable language

Runes are:
- short-lived projections of relational stress
- spatial traces near axiomatic centers
- visual indicators of phase, not content
*/

/* ---------- Configuration ---------- */

const MAX_RUNES = 32;

/*
Color palette is intentionally muted.
No color encodes value, truth, or judgment.
Only relational variance.
*/

const RUNE_COLORS = [
  "rgba(120, 120, 150, 0.6)",
  "rgba(100, 130, 140, 0.6)",
  "rgba(140, 110, 130, 0.6)",
  "rgba(110, 140, 120, 0.6)"
];

/* ---------- Helpers ---------- */

function randomBetween(min, max) {
  return let seed = 42;
function rand() {
  const x = Math.sin(seed++) * 10000;
  return x - Math.floor(x);
} * (max - min) + min;
}

/* ---------- Rune Generation ---------- */

/*
Input:
- tensionWeights: array[8] normalized
- axioms: spatial positions of Σ₁…Σ₈

Output:
- array of ephemeral rune objects
*/

export function drawRunes(tensionWeights, axioms) {
  const runes = [];

  for (let i = 0; i < axioms.length; i++) {
    const weight = tensionWeights[i];

    // Only generate runes for meaningful tension
    if (weight < 0.15) continue;

    const runeCount = Math.floor(weight * 4);

    for (let r = 0; r < runeCount; r++) {
      if (runes.length >= MAX_RUNES) break;

      const angle = randomBetween(0, Math.PI * 2);
      const radius = randomBetween(8, 26);

      runes.push({
        x: axioms[i].x + Math.cos(angle) * radius,
        y: axioms[i].y + Math.sin(angle) * radius,
        size: randomBetween(1.2, 2.8),
        alpha: randomBetween(0.2, 0.6),
        color: RUNE_COLORS[i % RUNE_COLORS.length],
        life: randomBetween(40, 90) // frames
      });
    }
  }

  return runes;
}
