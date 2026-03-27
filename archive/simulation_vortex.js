// simulation_vortex.js
// Port Python Simulation Vortex do JavaScript

function initPole() {
  return {
    E: Math.random() * 0.4 + 0.4, // Energy
    C: Math.random() * 0.4 + 0.4, // Coherence
    T: Math.random() * 0.3 + 0.1, // Tension
    M: 0.0,                       // Memory
    S: Math.random() * 0.15 + 0.05 // Entropy
  };
}

function clamp(x, lo=0.0, hi=1.0) {
  return Math.max(lo, Math.min(hi, x));
}

function fieldMeans(poles) {
  const means = { E: 0, C: 0, T: 0, M: 0, S: 0 };
  poles.forEach(pole => {
    means.E += pole.E;
    means.C += pole.C;
    means.T += pole.T;
    means.M += pole.M;
    means.S += pole.S;
  });
  means.E /= poles.length;
  means.C /= poles.length;
  means.T /= poles.length;
  means.M /= poles.length;
  means.S /= poles.length;
  return means;
}

function vortexStep(poles) {
  const means = fieldMeans(poles);
  const ALPHA_E = 0.02;
  const ALPHA_T = 0.03;
  const ALPHA_C = 0.04;
  const ALPHA_M = 0.01;
  const ALPHA_S = 0.015;
  const NOISE = 0.01;
  const DT = 0.05;

  poles.forEach(pole => {
    const dE = ALPHA_E * (means.T - pole.T);
    const dT = ALPHA_T * (1.0 - pole.C) - 0.5 * pole.S;
    const dC = ALPHA_C * (pole.E - Math.abs(pole.T - means.T));
    const anomaly = Math.abs(pole.T - means.T);
    const dM = ALPHA_M * anomaly - 0.1 * pole.M;
    const dS = ALPHA_S * (Math.abs(dE) + Math.abs(dT));

    pole.E = clamp(pole.E + dE * DT + (Math.random() - 0.5) * NOISE);
    pole.T = clamp(pole.T + dT * DT + (Math.random() - 0.5) * NOISE);
    pole.C = clamp(pole.C + dC * DT + (Math.random() - 0.5) * NOISE);
    pole.M = clamp(pole.M + dM * DT);
    pole.S = clamp(pole.S + dS * DT);
  });
}

function runVortex(query, steps=200) {
  const poles = Array(8).fill().map(initPole);

  if (/neviem|neistota/.test(query)) {
    poles[3].T = 0.8; // WIS tension
    poles[2].C = 0.3; // VER coherence drop
  }
  if (/rozhodnut|choice/.test(query)) {
    poles[0].E = 0.9; // INT energy
    poles[3].T = 0.7; // WIS tension
  }

  for (let i = 0; i < steps; i++) {
    vortexStep(poles);
  }

  const means = fieldMeans(poles);
  const K = means.C;
  const κ = 0.4;

  const tensionMatrix = {};
  const axioms = ["INT", "LEX", "VER", "LIB", "UNI", "REL", "WIS", "CRE"];
  axioms.forEach((a1, i) => {
    tensionMatrix[a1] = {};
    axioms.forEach((a2, j) => {
      if (i !== j) {
        const t = 1 - poles[i].C + Math.abs(poles[i].E - poles[j].E);
        tensionMatrix[a1][a2] = clamp(t, 0.1, 0.9);
      }
    });
  });

  return { tensionMatrix, K, κ };
}
