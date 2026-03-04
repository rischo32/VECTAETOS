// VORTEX — Epistemic Moment Engine

import { detectLanguage } from './language.js';

let promptsSK = null;
let promptsEN = null;

// -----------------------------
// LOAD PROMPTS (SAFE)
// -----------------------------
async function loadPrompts() {

  if (!promptsSK) {
    try {
      const resSK = await fetch('../projection/delta_prompts_sk.json');
      promptsSK = await resSK.json();
    } catch (e) {
      console.warn("Failed loading SK prompts:", e);
      promptsSK = {};
    }
  }

  if (!promptsEN) {
    try {
      const resEN = await fetch('../projection/delta_prompts.json');
      promptsEN = await resEN.json();
    } catch (e) {
      console.warn("Failed loading EN prompts:", e);
      promptsEN = {};
    }
  }
}

// -----------------------------
// HASH (DETERMINISTIC)
// -----------------------------
function hashString(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h *= 16777619;
  }
  return h >>> 0;
}

// -----------------------------
// GENERATE MIRROR QUESTION
// -----------------------------
export async function generateEpistemicMoment(text, delta_type) {

  await loadPrompts();

  const language = detectLanguage(text);

  const promptSet = language === "sk" ? promptsSK : promptsEN;

  if (!promptSet || !promptSet[delta_type]) {
    return null;
  }

  const prompts = promptSet[delta_type];

  const hash = hashString(text);
  const index = hash % prompts.length;

  return prompts[index];
}

// -----------------------------
// COMPUTE EM INTENSITY
// -----------------------------
export function computeEM(W, H, D) {

  const EM = (0.4 * W + 0.4 * H + 0.2 * D);

  let state;

  if (EM < 0.33) state = "LOW_COHERENCE";
  else if (EM < 0.66) state = "TENSIONAL";
  else state = "EPISTEMICALLY_ACTIVE";

  return {
    value: Number(EM.toFixed(3)),
    state
  };
}
