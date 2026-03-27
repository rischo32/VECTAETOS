// =========================================
// VECTAETOS — main.js
// Canonical interaction controller
// =========================================

// ---- IMPORTY (ak používaš moduly) ----
// import { Field } from "./field.js";
// import { States } from "./states.js";
// import { projectTension } from "./tension.js";
// import { projectRunes } from "./runes.js";

// =========================================
// GLOBÁLNE STAVY
// =========================================

let interactionConsumed = false;   // 1. interakcia prebehla
let paywallShown = false;          // paywall zobrazený
let secondIntentArmed = false;     // užívateľ sa POKÚSIL znovu vstúpiť

// DOM prvky
const inputLayer   = document.getElementById("input-layer");
const textInput    = document.getElementById("epistemic-input");
const paywallLayer = document.getElementById("paywall-overlay");

// =========================================
// INIT
// =========================================

document.addEventListener("DOMContentLoaded", () => {
  initInputGate();
  hidePaywall();
});

// =========================================
// INPUT GATE LOGIKA
// =========================================

function initInputGate() {
  if (!textInput) return;

  // PRVÝ VSTUP — POVOLENÝ
  textInput.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;

    // zabráni novému riadku
    e.preventDefault();

    const value = textInput.value.trim();
    if (!value) return;

    // Ak už prebehla interakcia → ide o DRUHÝ INTENT
    if (interactionConsumed) {
      armSecondIntent();
      return;
    }

    // PRVÁ A JEDINÁ INTERAKCIA
    consumeFirstInteraction(value);
  });

  // POKUS O FOCUS NA INPUT PO INTERAKCII
  textInput.addEventListener("focus", () => {
    if (interactionConsumed) {
      armSecondIntent();
    }
  });
}

// =========================================
// SPRACOVANIE PRVEJ INTERAKCIE
// =========================================

function consumeFirstInteraction(text) {
  interactionConsumed = true;

  // skry input
  disableInput();

  // ---- TU SA DEJE PROJEKCIA POĽA ----
  // projectTension(text);
  // projectRunes(text);

  // pole má byť ticho — nič viac sa tu nedeje
}

// =========================================
// DRUHÝ INTENT → PAYWALL
// =========================================

function armSecondIntent() {
  if (paywallShown) return;

  secondIntentArmed = true;
  showPaywall();
}

// =========================================
// PAYWALL LOGIKA
// =========================================

function showPaywall() {
  if (!paywallLayer) return;

  paywallShown = true;

  paywallLayer.style.display = "flex";
  paywallLayer.setAttribute("aria-hidden", "false");
}

function hidePaywall() {
  if (!paywallLayer) return;

  paywallLayer.style.display = "none";
  paywallLayer.setAttribute("aria-hidden", "true");
}

// =========================================
// INPUT CONTROL
// =========================================

function disableInput() {
  if (!textInput) return;

  textInput.blur();
  textInput.disabled = true;
  textInput.value = "";
}

// =========================================
// BEZPEČNOSTNÉ POZNÁMKY
// =========================================
//
// ❌ ŽIADNE click listenery na body / canvas
// ❌ ŽIADNE mousemove / touchstart / tap
// ❌ ŽIADNE automatické timeouty na paywall
//
// Paywall je aktivovaný VÝHRADNE:
// - ENTER po prvej interakcii
// - alebo focus na input po uzavretí poľa
//
// =========================================
