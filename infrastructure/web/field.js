// =========================================
// VECTAETOS — field.js
// Canonical field projection (visual only)
// =========================================

const canvas = document.getElementById("field-canvas");
const ctx = canvas.getContext("2d");

let width, height;
let poles = [];

// ---- Axiomatic centers (8) ----
const POLE_COUNT = 8;

// ---- Init ----
function resize() {
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

// ---- Create poles ----
function initPoles() {
  poles = [];
  for (let i = 0; i < POLE_COUNT; i++) {
    poles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.15,
      vy: (Math.random() - 0.5) * 0.15,
      r: 2 + Math.random() * 1.5,
      phase: Math.random() * Math.PI * 2
    });
  }
}
initPoles();

// ---- Draw loop ----
function draw() {
  ctx.clearRect(0, 0, width, height);

  // background fade (very subtle)
  ctx.fillStyle = "rgba(0, 0, 0, 0.25)";
  ctx.fillRect(0, 0, width, height);

  // connections
  ctx.strokeStyle = "rgba(255, 255, 255, 0.06)";
  ctx.lineWidth = 1;

  for (let i = 0; i < poles.length; i++) {
    for (let j = i + 1; j < poles.length; j++) {
      const dx = poles[i].x - poles[j].x;
      const dy = poles[i].y - poles[j].y;
      const d = Math.sqrt(dx * dx + dy * dy);

      if (d < 260) {
        ctx.globalAlpha = 1 - d / 260;
        ctx.beginPath();
        ctx.moveTo(poles[i].x, poles[i].y);
        ctx.lineTo(poles[j].x, poles[j].y);
        ctx.stroke();
      }
    }
  }

  ctx.globalAlpha = 1;

  // poles
  for (const p of poles) {
    p.phase += 0.01;

    // subtle drift
    p.x += p.vx;
    p.y += p.vy;

    if (p.x < 0 || p.x > width) p.vx *= -1;
    if (p.y < 0 || p.y > height) p.vy *= -1;

    const pulse = 0.5 + Math.sin(p.phase) * 0.5;

    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r + pulse * 0.6, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
    ctx.fill();
  }

  requestAnimationFrame(draw);
}

// ---- Start ----
draw();

// =========================================
// NOTE:
// - žiadne event listenery
// - žiadne kliky
// - žiadna spätná väzba
// - pole len existuje
// =========================================
