/* =========================================
   VECTAETOS — Tension Projection Module
   Non-agentic, non-evaluative
   ========================================= */

/*
TENSION ≠ PROBLEM
TENSION ≠ VALUE
TENSION = relational imbalance between axiomatic centers

Input:
- raw user text (opaque, not interpreted semantically)

Output:
- normalized tension weights [0..1] for Σ₁…Σ₈
*/

/* ---------- Configuration ---------- */

const AXIOM_COUNT = 8;

/*
We deliberately do NOT parse meaning.
We only derive structural features of the input:
- length
- density
- asymmetry
- rhythm
*/

/* ---------- Helpers ---------- */

function clamp(x, min = 0, max = 1) {
  return Math.max(min, Math.min(max, x));
}

/* ---------- Feature Extraction ---------- */

function extractFeatures(text) {
  const length = text.length;
  const words = text.split(/\s+/).filter(Boolean);
  const wordCount = words.length;

  const avgWordLength =
    wordCount > 0
      ? words.reduce((s, w) => s + w.length, 0) / wordCount
      : 0;

  const variance =
    wordCount > 0
      ? words.reduce((s, w) => s + Math.pow(w.length - avgWordLength, 2), 0) /
        wordCount
      : 0;

  return {
    length,
    wordCount,
    avgWordLength,
    variance
  };
}

/* ---------- Tension Mapping ---------- */

function mapToTension(features) {
  const base = [];

  /*
  No semantic axes.
  We distribute tension asymmetrically but deterministically,
  to avoid randomness while avoiding interpretation.
  */

  for (let i = 0; i < AXIOM_COUNT; i++) {
    const phase = (i + 1) / AXIOM_COUNT;

    let value =
      Math.sin(features.length * 0.01 * phase) +
      Math.cos(features.wordCount * 0.2 * phase) +
      Math.tanh(features.variance * 0.1);

    value = clamp((value + 2) / 4);
    base.push(value);
  }

  return normalize(base);
}

/* ---------- Normalization ---------- */

function normalize(arr) {
  const sum = arr.reduce((s, v) => s + v, 0);
  if (sum === 0) return arr.map(() => 0);
  return arr.map(v => clamp(v / sum * AXIOM_COUNT));
}

/* ---------- Public API ---------- */

export function computeTension(inputText) {
  if (!inputText || typeof inputText !== "string") {
    return new Array(AXIOM_COUNT).fill(0);
  }

  const features = extractFeatures(inputText);
  return mapToTension(features);
}
