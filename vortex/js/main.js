// VORTEX — Main Entry
// Stable orchestration layer

import { SceneManager } from './scene.js';
import { InputManager } from './input.js';
import { OverlayManager } from './overlay.js';

class VortexApp {

  constructor() {
    this.sceneManager = null;
    this.overlayManager = null;
    this.inputManager = null;

    this.init();
  }

  init() {

    // ---------------------------
    // Scene
    // ---------------------------
    this.sceneManager = new SceneManager();
    this.sceneManager.init();

    // ---------------------------
    // Overlay (optional safe init)
    // ---------------------------
    try {
      this.overlayManager = new OverlayManager();
      this.overlayManager.init();
    } catch (e) {
      console.warn("Overlay not initialized:", e);
      this.overlayManager = null;
    }

    // ---------------------------
    // Input
    // ---------------------------
    this.inputManager = new InputManager(
      this.sceneManager,
      this.overlayManager
    );
    this.inputManager.init();

    // ---------------------------
    // Resize handling
    // ---------------------------
    window.addEventListener('resize', () => {
      if (this.sceneManager) {
        this.sceneManager.onResize();
      }
    });

    // ---------------------------
    // Start loop
    // ---------------------------
    this.animate();
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    if (this.sceneManager) {
      this.sceneManager.update();
      this.sceneManager.render();
    }
  }

}

// Boot safely after DOM ready
window.addEventListener("DOMContentLoaded", () => {
  new VortexApp();
});
