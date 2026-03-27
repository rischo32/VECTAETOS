// =========================================
// VECTAETOS — RUNIC PROJECTION (VISUAL)
// -------------------------------------
// - no input
// - no meaning
// - deterministic
// - overlay over vortex
// =========================================

const RUNES = (() => {

  // -----------------------------
  // CONFIG
  // -----------------------------
  const symbols = ["ᚨ","ᛚ","ᚱ","ᚦ","ᛜ","ᚷ","ᛟ","ᛞ"];

  let seed = 1337;
  function rand() {
    const x = Math.sin(seed++) * 10000;
    return x - Math.floor(x);
  }

  const canvas = document.createElement("canvas");
  canvas.id = "runesCanvas";
  canvas.style.position = "fixed";
  canvas.style.inset = "0";
  canvas.style.pointerEvents = "none";
  canvas.style.zIndex = "2";

  document.body.appendChild(canvas);

  const ctx = canvas.getContext("2d");

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  window.addEventListener("resize", resize);
  resize();

  // -----------------------------
  // INIT RUNES
  // -----------------------------
  const runes = [];

  for (let i = 0; i < 8; i++) {
    runes.push({
      symbol: symbols[i],
      angle: (Math.PI * 2 * i) / 8,
      radius: 140 + rand() * 20,
      phase: rand() * Math.PI * 2
    });
  }

  // -----------------------------
  // DRAW
  // -----------------------------
  function draw(t) {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const cx = canvas.width / 2;
    const cy = canvas.height / 2;

    runes.forEach(r => {

      const a = r.angle + t * 0.001 + Math.sin(r.phase + t * 0.0005) * 0.2;

      const x = cx + Math.cos(a) * r.radius;
      const y = cy + Math.sin(a) * r.radius;

      ctx.font = "18px monospace";
      ctx.fillStyle = "rgba(200, 220, 255, 0.6)";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      ctx.fillText(r.symbol, x, y);
    });
  }

  // -----------------------------
  // LOOP
  // -----------------------------
  function loop(t) {
    draw(t);
    requestAnimationFrame(loop);
  }

  requestAnimationFrame(loop);

})();
