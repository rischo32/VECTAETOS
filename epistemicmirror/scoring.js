// Epistemic Mirror — Scoring Engine
// Version: mirror_v1
// Deterministic. Projection layer only.
// No randomness. No persistence. No feedback to Φ.

export function scoreQuestion(text) {

  const cleaned = (text || "").trim();

  if (!cleaned) {
    return null;
  }

  const characterLength = cleaned.length;

  const words = cleaned
    .split(/\s+/)
    .filter(Boolean);

  const wordCount = words.length;

  // ---------------------------------
  // 1. WIDTH (Horizontal Scope)
  // ---------------------------------
  // Heuristic: dispersion by word count
  const W = clamp01(wordCount / 12);

  // ---------------------------------
  // 2. HEIGHT (Abstraction / Frame)
  // ---------------------------------
  const lower = cleaned.toLowerCase();

  const hasQuestionMark = cleaned.includes("?");
  const hasCausalMarker =
    lower.includes("prečo") ||
    lower.includes("ako") ||
    lower.includes("why") ||
    lower.includes("how") ||
    lower.includes("explain");

  let H;

  if (hasQuestionMark) {
    H = 0.8;
  } else if (hasCausalMarker) {
    H = 0.6;
  } else {
    H = 0.4;
  }

  H = clamp01(H);

  // ---------------------------------
  // 3. DEPTH (Assumption Load)
  // ---------------------------------
  const D = clamp01(characterLength / 100);

  // ---------------------------------
  // 4. GATE PASS
  // ---------------------------------
  const gate_pass = Math.min(W, H, D);

  // ---------------------------------
  // 5. SIGMA (Structural Tension)
  // ---------------------------------
  const sigma = 1 - gate_pass;

  // ---------------------------------
  // 6. DELTA TYPE (Dominant Distortion)
  // ---------------------------------
  const epsilon = 0.05;

  let delta_type;

  const isBalanced =
    Math.abs(W - H) < epsilon &&
    Math.abs(H - D) < epsilon &&
    Math.abs(W - D) < epsilon;

  if (isBalanced) {
    delta_type = "Δ0";
  } else if (W <= H && W <= D) {
    delta_type = "ΔW";
  } else if (H <= W && H <= D) {
    delta_type = "ΔH";
  } else {
    delta_type = "ΔD";
  }

  // ---------------------------------
  // 7. STATE (User-Facing Bands)
  // ---------------------------------
  let state;

  if (gate_pass <= 0.25) {
    state = "FRAGMENTED";
  } else if (gate_pass <= 0.50) {
    state = "TENSIONAL";
  } else if (gate_pass <= 0.75) {
    state = "UNSTABLE BALANCE";
  } else {
    state = "STRUCTURALLY STABLE";
  }

  // ---------------------------------
  // 8. USER-FACING DISTORTION LABEL
  // ---------------------------------
  const distortionMap = {
    "ΔW": "SCOPE DISTORTION",
    "ΔH": "FRAME DISTORTION",
    "ΔD": "ASSUMPTION DISTORTION",
    "Δ0": "STRUCTURAL BALANCE"
  };

  return {
    W: round2(W),
    H: round2(H),
    D: round2(D),
    gate_pass: round2(gate_pass),
    sigma: round2(sigma),
    state,
    delta_type,
    distortion: distortionMap[delta_type]
  };
}

// ---------------------------------
// Utilities
// ---------------------------------

function clamp01(n) {
  return Math.max(0, Math.min(1, n));
}

function round2(n) {
  return Math.round(n * 100) / 100;
}
