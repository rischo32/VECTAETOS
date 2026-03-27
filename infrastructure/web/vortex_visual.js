// =========================================
// VECTAETOS — VORTEX VISUAL (CANONICAL)
// -------------------------------------
// - no input
// - deterministic
// - no interpretation
// - no state persistence
// =========================================

const VORTEX = (() => {

  // -----------------------------
  // CONFIG
  // -----------------------------
  const NODE_COUNT = 8;
  const RADIUS = 120;
  const SPEED = 0.002;

  // deterministic seed
  let seed = 42;
  function rand() {
    const x = Math.sin(seed++) * 10000;
    return x - Math.floor(x);
  }

  // -----------------------------
  // INIT CANVAS
  // -----------------------------
  const canvas = document.createElement("canvas");
  canvas.id = "vortexCanvas";
  document.body.prepend(canvas);

  const ctx = canvas.getContext("2d");

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  window.addEventListener("resize", resize);
  resize();

  // -----------------------------
  // NODES (Σ₁…Σ₈)
  // -----------------------------
  const nodes = [];

  for (let i = 0; i < NODE_COUNT; i++) {
    nodes.push({
      angle: (Math.PI * 2 * i) / NODE_COUNT,
      radius: RADIUS + rand() * 10,
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

    const positions = [];

    // --- compute positions ---
    nodes.forEach(n => {

      const a = n.angle + t * SPEED + Math.sin(n.phase + t * 0.0005) * 0.2;

      const x = cx + Math.cos(a) * n.radius;
      const y = cy + Math.sin(a) * n.radius;

      positions.push({ x, y });
    });

    // --- draw connections ---
    for (let i = 0; i < positions.length; i++) {
      for (let j = i + 1; j < positions.length; j++) {

        const dx = positions[i].x - positions[j].x;
        const dy = positions[i].y - positions[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        const alpha = Math.max(0, 1 - dist / 300);

        ctx.strokeStyle = `rgba(120, 200, 255, ${alpha * 0.2})`;
        ctx.lineWidth = 1;

        ctx.beginPath();
        ctx.moveTo(positions[i].x, positions[i].y);
        ctx.lineTo(positions[j].x, positions[j].y);
        ctx.stroke();
      }
    }

    // --- draw nodes ---
    positions.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(200, 220, 255, 0.6)";
      ctx.fill();
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
