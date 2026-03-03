// VORTEX — Sigma Scoring Engine
// Version: delta_v1
// Deterministic. No randomness.
// Projection layer only.

export function computeDelta(text) {

  const cleaned = (text || "").trim();

  const characterLength = cleaned.length;
  const words = cleaned.length > 0
    ? cleaned.split(/\s+/).filter(Boolean)
    : [];

  const wordCount = words.length;

  // ----------------------------
  // 1. WIDTH (W)
  // ----------------------------
  // Horizontal scope expansion
  let W = Math.min(1, wordCount / 12);

  // ----------------------------
  // 2. HEIGHT (H)
  // ----------------------------
  // Abstraction / interrogative structure
  const lower = cleaned.toLowerCase();

  const hasQuestionMark = cleaned.includes("?");
  const hasCausalMarker =
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

  // ----------------------------
  // 3. DEPTH (D)
  // ----------------------------
  // Structural load approximation
  let D = Math.min(1, characterLength / 100);

  // ----------------------------
  // 4. GATE PASS
  // ----------------------------
  const gate_pass = Math.min(W, H, D);

  // ----------------------------
  // 5. SIGMA (σ)
  // ----------------------------
  const sigma = 1 - gate_pass;

  // ----------------------------
  // 6. DELTA TYPE
  // ----------------------------
  const epsilon = 0.05;

  let delta_type;

  const minAxis = Math.min(W, H, D);

  const isBalanced =
    Math.abs(W - H) < epsilon &&
    Math.abs(H - D) < epsilon &&
    Math.abs(W - D) < epsilon;

  if (isBalanced) {
    delta_type = "Δ0";
  } else if (minAxis === W) {
    delta_type = "ΔW";
  } else if (minAxis === H) {
    delta_type = "ΔH";
  } else {
    delta_type = "ΔD";
  }

  // ----------------------------
  // 7. STABILITY BAND
  // ----------------------------
  let state;

  if (gate_pass <= 0.25) {
    state = "NON_REPRESENTABLE";
  } else if (gate_pass <= 0.50) {
    state = "LOW_COHERENCE";
  } else if (gate_pass <= 0.75) {
    state = "MEDIUM_COHERENCE";
  } else {
    state = "HIGH_COHERENCE";
  }

  // ----------------------------
  // 8. INTENSITY (buffer-based)
  // ----------------------------
  const intensity = Math.min(1, characterLength / 100);

  return {
    W: round4(W),
    H: round4(H),
    D: round4(D),
    sigma: round4(sigma),
    delta_type,
    state,
    gate_pass: round4(gate_pass),
    intensity: round4(intensity),
    metadata: {
      version: "delta_v1",
      engine: "Vortex"
    }
  };
}

// Utility
function round4(n) {
  return Math.round(n * 10000) / 10000;
}
