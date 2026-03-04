// VORTEX — Input Manager
// Deterministic bridge between UI and scoring engine

import { computeDelta } from './sigma.js';

export class InputManager {

  constructor(sceneManager, overlayManager = null) {
    this.sceneManager = sceneManager;
    this.overlayManager = overlayManager;

    this.textarea = document.getElementById("question");
    this.bufferFill = document.getElementById("bufferFill");

    this.intensity = 0;
  }

  init() {
    if (!this.textarea) return;

    this.textarea.addEventListener("input", () => this.handleInput());
    this.textarea.addEventListener("keydown", (e) => this.handleKeyDown(e));
  }

  // -------------------------
  // BUFFER INTENSITY UPDATE
  // -------------------------
  handleInput() {
    const length = this.textarea.value.length;

    this.intensity = Math.min(1, length / 100);

    if (this.bufferFill) {
      this.bufferFill.style.width = `${this.intensity * 100}%`;
    }
  }

  // -------------------------
  // SUBMIT ON ENTER
  // -------------------------
  handleKeyDown(e) {

    if (e.key === "Enter") {
      e.preventDefault();

      const text = this.textarea.value.trim();
      if (!text) return;

      const result = computeDelta(text);

      // ---- Send to Scene ----
      if (this.sceneManager) {
        this.sceneManager.startSplit(
          result.W,
          result.H,
          result.D,
          result.intensity
        );
      }

      // ---- Send to Overlay ----
      if (this.overlayManager) {
        this.overlayManager.update(result);
      }

      console.log("Δ RESULT:", result);
    }
  }

}
