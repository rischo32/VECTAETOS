// Epistemic Mirror — Main Controller
// Minimal. Deterministic. Projection only.

import { scoreQuestion } from "./scoring.js";

let promptsSK = null;
let promptsEN = null;

// -------------------------------------
// LOAD PROMPTS
// -------------------------------------
async function loadPrompts() {
  try {
    const [skRes, enRes] = await Promise.all([
      fetch("./prompts/delta_prompts_sk.json"),
      fetch("./prompts/delta_prompts.json")
    ]);

    promptsSK = await skRes.json();
    promptsEN = await enRes.json();

  } catch (e) {
    console.error("Failed loading prompts:", e);
  }
}

// -------------------------------------
// LANGUAGE DETECTION (Simple Heuristic)
// -------------------------------------
function detectLanguage(text) {
  const lower = text.toLowerCase();

  if (
    lower.includes("prečo") ||
    lower.includes("ako") ||
    lower.includes("čo") ||
    lower.includes("kedy")
  ) {
    return "sk";
  }

  return "en";
}

// -------------------------------------
// DETERMINISTIC HASH
// -------------------------------------
function hashString(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h *= 16777619;
  }
  return h >>> 0;
}

// -------------------------------------
// GET MIRROR QUESTION
// -------------------------------------
function getMirrorPrompt(text, deltaType) {

  const lang = detectLanguage(text);
  const source = lang === "sk" ? promptsSK : promptsEN;

  if (!source || !source[deltaType]) {
    return "Projection unavailable.";
  }

  const list = source[deltaType];
  const index = hashString(text) % list.length;

  return list[index];
}

// -------------------------------------
// MAIN BOOT
// -------------------------------------
document.addEventListener("DOMContentLoaded", async () => {

  await loadPrompts();

  const input = document.getElementById("questionInput");
  const btn = document.getElementById("analyzeBtn");
  const output = document.getElementById("output");
  const projectionData = document.getElementById("projectionData");
  const mirrorQuestion = document.getElementById("mirrorQuestion");
  const charCount = document.getElementById("charCount");

  // -------------------------
  // Character Counter
  // -------------------------
  input.addEventListener("input", () => {
    charCount.textContent = input.value.length;
  });

  // -------------------------
  // Run Projection
  // -------------------------
  function runProjection() {

    const text = input.value.trim();
    if (!text) return;

    const result = scoreQuestion(text);
    if (!result) return;

    const mirror = getMirrorPrompt(text, result.delta_type);

    projectionData.innerHTML = `
      Width: ${result.W}<br>
      Height: ${result.H}<br>
      Depth: ${result.D}<br><br>
      Gate Pass: ${result.gate_pass}<br>
      Sigma: ${result.sigma}<br>
      State: ${result.state}<br>
      Dominant Distortion: ${result.distortion}
    `;

    mirrorQuestion.textContent = mirror;

    output.classList.remove("hidden");

    // Optional: scroll into view
    output.scrollIntoView({ behavior: "smooth" });
  }

  // -------------------------
  // Button Click
  // -------------------------
  btn.addEventListener("click", () => {

    // 🔐 Stripe hook point (future)
    // startCheckout().then(() => runProjection());

    runProjection(); // Demo mode for now

  });

});
