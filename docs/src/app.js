const papers = [
  {
    "title": "Vectaetos: A Foundational Relational Epistemic Field with Intrinsic Humility",
    "doi": "10.5281/zenodo.18076787",
    "url": "https://doi.org/10.5281/zenodo.18076787",
    "date": "2025-12-28",
    "tags": [
      "epistemic field",
      "non-agentic",
      "so(8)",
      "triality",
      "coherence"
    ],
    "abstract": "Primary publication entry. Placeholder abstract for interface prototype; replace with canonical publication metadata."
  },
  {
    "title": "Supplementary Material I — Structural Decompositions",
    "doi": "10.5281/zenodo.18138226",
    "url": "https://doi.org/10.5281/zenodo.18138226",
    "date": "2026-01-15",
    "tags": [
      "structure",
      "decomposition"
    ],
    "abstract": "Supplementary publication entry for structural decompositions."
  },
  {
    "title": "Supplementary Material II — Projection Topology",
    "doi": "10.5281/zenodo.18739552",
    "url": "https://doi.org/10.5281/zenodo.18739552",
    "date": "2026-02-10",
    "tags": [
      "projection",
      "topology"
    ],
    "abstract": "Supplementary publication entry for projection topology."
  },
  {
    "title": "Supplementary Material III — Coherence Metrics",
    "doi": "10.5281/zenodo.18911932",
    "url": "https://doi.org/10.5281/zenodo.18911932",
    "date": "2026-03-01",
    "tags": [
      "coherence",
      "metrics",
      "descriptive"
    ],
    "abstract": "Supplementary publication entry. UI wording must avoid score/optimization drift."
  },
  {
    "title": "Supplementary Material IV — Epistemic Cryptography",
    "doi": "10.5281/zenodo.19148358",
    "url": "https://doi.org/10.5281/zenodo.19148358",
    "date": "2026-03-28",
    "tags": [
      "audit",
      "fingerprint",
      "read-only"
    ],
    "abstract": "Supplementary publication entry for external structural fingerprinting."
  },
  {
    "title": "Supplementary Material V — Boundary Conditions",
    "doi": "10.5281/zenodo.19370185",
    "url": "https://doi.org/10.5281/zenodo.19370185",
    "date": "2026-04-12",
    "tags": [
      "boundary",
      "representability"
    ],
    "abstract": "Supplementary publication entry for boundary conditions."
  }
];
const licenses = [
  {
    "title": "VCL-2.0 — Canonical Ontology License",
    "doi": "10.5281/zenodo.20533697",
    "url": "https://doi.org/10.5281/zenodo.20533697",
    "layer": "Ontology",
    "description": "Canonical ontology layer. Read-only posture in this prototype."
  },
  {
    "title": "VTP-1.0 — Trademark and Compatibility Policy",
    "doi": "10.5281/zenodo.20534913",
    "url": "https://doi.org/10.5281/zenodo.20534913",
    "layer": "Identity",
    "description": "Identity and compatibility boundary."
  },
  {
    "title": "VNAL-1.1 — Non-Agentic License",
    "doi": "10.5281/zenodo.20571153",
    "url": "https://doi.org/10.5281/zenodo.20571153",
    "layer": "Ethics / Core",
    "description": "Behavioral non-agentic license layer.",
    "warning": true
  },
  {
    "title": "VPL-1.0 — Projection License",
    "doi": "10.5281/zenodo.20574386",
    "url": "https://doi.org/10.5281/zenodo.20574386",
    "layer": "Projection",
    "description": "Projection and trace artifacts."
  },
  {
    "title": "AEPL v2.0 — Axiomatic Epistemic Public License",
    "doi": "10.5281/zenodo.20574489",
    "url": "https://doi.org/10.5281/zenodo.20574489",
    "layer": "Software",
    "description": "Software and tooling layer."
  }
];
const doiRegistry = [
  {
    "title": "Vectaetos: A Foundational Relational Epistemic Field with Intrinsic Humility",
    "doi": "10.5281/zenodo.18076787",
    "url": "https://doi.org/10.5281/zenodo.18076787",
    "type": "publication"
  },
  {
    "title": "Supplementary Material I — Structural Decompositions",
    "doi": "10.5281/zenodo.18138226",
    "url": "https://doi.org/10.5281/zenodo.18138226",
    "type": "publication"
  },
  {
    "title": "Supplementary Material II — Projection Topology",
    "doi": "10.5281/zenodo.18739552",
    "url": "https://doi.org/10.5281/zenodo.18739552",
    "type": "publication"
  },
  {
    "title": "Supplementary Material III — Coherence Metrics",
    "doi": "10.5281/zenodo.18911932",
    "url": "https://doi.org/10.5281/zenodo.18911932",
    "type": "publication"
  },
  {
    "title": "Supplementary Material IV — Epistemic Cryptography",
    "doi": "10.5281/zenodo.19148358",
    "url": "https://doi.org/10.5281/zenodo.19148358",
    "type": "publication"
  },
  {
    "title": "Supplementary Material V — Boundary Conditions",
    "doi": "10.5281/zenodo.19370185",
    "url": "https://doi.org/10.5281/zenodo.19370185",
    "type": "publication"
  },
  {
    "title": "VCL-2.0 — Canonical Ontology License",
    "doi": "10.5281/zenodo.20533697",
    "url": "https://doi.org/10.5281/zenodo.20533697",
    "type": "license"
  },
  {
    "title": "VTP-1.0 — Trademark and Compatibility Policy",
    "doi": "10.5281/zenodo.20534913",
    "url": "https://doi.org/10.5281/zenodo.20534913",
    "type": "license"
  },
  {
    "title": "VNAL-1.1 — Non-Agentic License",
    "doi": "10.5281/zenodo.20571153",
    "url": "https://doi.org/10.5281/zenodo.20571153",
    "type": "license"
  },
  {
    "title": "VPL-1.0 — Projection License",
    "doi": "10.5281/zenodo.20574386",
    "url": "https://doi.org/10.5281/zenodo.20574386",
    "type": "license"
  },
  {
    "title": "AEPL v2.0 — Axiomatic Epistemic Public License",
    "doi": "10.5281/zenodo.20574489",
    "url": "https://doi.org/10.5281/zenodo.20574489",
    "type": "license"
  }
];
const topology = {
  "nodes": [
    {
      "id": "field",
      "label": "field",
      "x": 0.09,
      "y": 0.43,
      "r": 7
    },
    {
      "id": "boundary",
      "label": "boundary",
      "x": 0.1,
      "y": 0.48,
      "r": 8
    },
    {
      "id": "topology",
      "label": "topology",
      "x": 0.07,
      "y": 0.73,
      "r": 6
    },
    {
      "id": "ontology",
      "label": "ontology",
      "x": 0.065,
      "y": 0.86,
      "r": 7
    },
    {
      "id": "nonagentic",
      "label": "non-agentic",
      "x": 0.09,
      "y": 0.91,
      "r": 7
    },
    {
      "id": "projection",
      "label": "projection",
      "x": 0.105,
      "y": 0.89,
      "r": 5
    },
    {
      "id": "episteme",
      "label": "episteme",
      "x": 0.22,
      "y": 0.81,
      "r": 7
    },
    {
      "id": "coherence",
      "label": "coherence",
      "x": 0.4,
      "y": 0.68,
      "r": 7
    },
    {
      "id": "symmetry",
      "label": "symmetry",
      "x": 0.61,
      "y": 0.77,
      "r": 8
    },
    {
      "id": "descriptive",
      "label": "descriptive",
      "x": 0.625,
      "y": 0.84,
      "r": 6
    },
    {
      "id": "tension",
      "label": "tension",
      "x": 0.625,
      "y": 0.47,
      "r": 6
    },
    {
      "id": "humility",
      "label": "humility",
      "x": 0.58,
      "y": 0.32,
      "r": 8
    },
    {
      "id": "structure",
      "label": "structure",
      "x": 0.69,
      "y": 0.24,
      "r": 5
    },
    {
      "id": "so8",
      "label": "so(8)",
      "x": 0.84,
      "y": 0.2,
      "r": 8
    },
    {
      "id": "triality",
      "label": "triality",
      "x": 0.84,
      "y": 0.36,
      "r": 7
    }
  ],
  "edges": [
    [
      "field",
      "boundary"
    ],
    [
      "boundary",
      "topology"
    ],
    [
      "topology",
      "ontology"
    ],
    [
      "ontology",
      "nonagentic"
    ],
    [
      "ontology",
      "projection"
    ],
    [
      "topology",
      "episteme"
    ],
    [
      "episteme",
      "coherence"
    ],
    [
      "coherence",
      "symmetry"
    ],
    [
      "symmetry",
      "descriptive"
    ],
    [
      "symmetry",
      "tension"
    ],
    [
      "tension",
      "humility"
    ],
    [
      "humility",
      "structure"
    ],
    [
      "structure",
      "so8"
    ],
    [
      "so8",
      "triality"
    ],
    [
      "structure",
      "triality"
    ],
    [
      "tension",
      "structure"
    ]
  ]
};

const app = document.querySelector("#app");
const boot = document.querySelector("#boot");
const windowsRoot = document.querySelector("#windows");
const focusActive = document.querySelector("#focusActive");
const clock = document.querySelector("#clock");

const state = {
  z: 20,
  windows: new Map(),
  active: null,
  settings: JSON.parse(localStorage.getItem("vectaetos:settings") || "{}")
};

const MODULES = {
  terminal: { title: "›_ Terminal", x: 24, y: 28, w: 820, h: 520, render: renderTerminal },
  papers: { title: "▤ Papers", x: 36, y: 44, w: 780, h: 520, render: renderPapers },
  doi: { title: "↗ DOI Registry", x: 52, y: 38, w: 760, h: 560, render: renderDoi },
  licenses: { title: "⬡ License Stack", x: 70, y: 58, w: 710, h: 520, render: renderLicenses },
  topology: { title: "⌘ Field Topology", x: 80, y: 62, w: 760, h: 520, render: renderTopology },
  notes: { title: "□ Notes", x: 110, y: 78, w: 680, h: 430, render: renderNotes },
  settings: { title: "⚙ Settings", x: 135, y: 50, w: 560, h: 430, render: renderSettings },
  about: { title: "▱ About VectaetOS", x: 120, y: 70, w: 660, h: 560, render: renderAbout }
};

init();

function init() {
  applySettings();

  const bootEnabled = state.settings.bootAnimation !== false;
  if (bootEnabled) {
    setTimeout(() => {
      boot.classList.add("hidden");
      app.classList.remove("hidden");
      openWindow("terminal");
      startAmbient();
    }, 2300);
  } else {
    boot.classList.add("hidden");
    app.classList.remove("hidden");
    openWindow("terminal");
    startAmbient();
  }

  document.querySelectorAll("[data-open]").forEach(btn => {
    btn.addEventListener("click", () => openWindow(btn.dataset.open));
  });

  focusActive.addEventListener("click", () => {
    if (state.active) openWindow(state.active);
  });

  setInterval(() => {
    const d = new Date();
    clock.textContent = d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }, 500);
}

function applySettings() {
  const s = state.settings;
  app.dataset.font = s.font || "default";
  app.dataset.theme = s.theme || "field";
}

function saveSettings() {
  localStorage.setItem("vectaetos:settings", JSON.stringify(state.settings));
  applySettings();
}

function openWindow(id) {
  const existing = state.windows.get(id);
  if (existing) {
    existing.classList.remove("hidden");
    focusWindow(id, existing);
    return;
  }

  const cfg = MODULES[id];
  if (!cfg) return;

  const tpl = document.querySelector("#window-template");
  const win = tpl.content.firstElementChild.cloneNode(true);
  win.dataset.id = id;
  win.querySelector(".win-name").textContent = cfg.title;
  const body = win.querySelector(".win-body");
  body.innerHTML = "";
  body.appendChild(cfg.render());

  win.style.left = `${cfg.x}px`;
  win.style.top = `${cfg.y}px`;
  win.style.width = `${cfg.w}px`;
  win.style.height = `${cfg.h}px`;
  windowsRoot.appendChild(win);
  state.windows.set(id, win);
  makeWindowInteractive(win);
  focusWindow(id, win);

  if (id === "topology") requestAnimationFrame(() => drawTopology(win.querySelector("#topologyCanvas")));
}

function focusWindow(id, win) {
  state.active = id;
  focusActive.textContent = MODULES[id]?.title.replace(/[›_▤↗⬡⌘□⚙▱]/g, "").trim() || id;
  win.style.zIndex = ++state.z;
  document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.toggle("active", btn.dataset.open === id));
}

function makeWindowInteractive(win) {
  win.addEventListener("mousedown", () => focusWindow(win.dataset.id, win));

  const title = win.querySelector(".win-title");
  let drag = null;

  title.addEventListener("pointerdown", (e) => {
    if (e.target.closest("button")) return;
    const rect = win.getBoundingClientRect();
    drag = { x: e.clientX, y: e.clientY, left: rect.left - windowsRoot.getBoundingClientRect().left, top: rect.top };
    title.setPointerCapture(e.pointerId);
  });

  title.addEventListener("pointermove", (e) => {
    if (!drag || win.classList.contains("max")) return;
    const dx = e.clientX - drag.x;
    const dy = e.clientY - drag.y;
    const maxLeft = Math.max(0, windowsRoot.clientWidth - 120);
    const maxTop = Math.max(0, window.innerHeight - 94);
    win.style.left = `${Math.min(Math.max(0, drag.left + dx), maxLeft)}px`;
    win.style.top = `${Math.min(Math.max(0, drag.top + dy), maxTop)}px`;
  });

  title.addEventListener("pointerup", () => { drag = null; });
  title.addEventListener("pointercancel", () => { drag = null; });

  win.querySelector("[data-action='close']").addEventListener("click", () => {
    state.windows.delete(win.dataset.id);
    win.remove();
  });
  win.querySelector("[data-action='minimize']").addEventListener("click", () => win.classList.add("hidden"));
  win.querySelector("[data-action='maximize']").addEventListener("click", () => {
    win.classList.toggle("max");
    if (win.dataset.id === "topology") setTimeout(() => drawTopology(win.querySelector("#topologyCanvas")), 50);
  });
}

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") node.className = value;
    else if (key === "html") node.innerHTML = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value);
  }
  for (const child of [].concat(children)) {
    if (child === null || child === undefined) continue;
    node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return node;
}

function renderTerminal() {
  const wrap = el("div", { class: "terminal" });
  const output = el("div", { class: "term-output" });
  const input = el("input", { class: "term-input", autocomplete: "off", spellcheck: "false" });
  const line = el("div", { class: "term-inputline" }, [
    el("span", { class: "prompt" }, "vectaetos@field:~$"),
    input
  ]);

  const write = (text = "") => {
    output.textContent += `${text}\n`;
    output.scrollTop = output.scrollHeight;
  };

  write("VectaetOS Terminal v1.0.0");
  write('Type "help" for available commands.');
  write("");

  const commands = {
    help() {
      write([
        "Available commands:",
        "  help                 list commands",
        "  status               show non-agentic status",
        "  guard                show fail-lower guard",
        "  open papers          open publications",
        "  open doi             open DOI registry",
        "  open topology        open field topology projection",
        "  open licenses        open license stack",
        "  open notes           open local notes",
        "  clear                clear terminal"
      ].join("\n"));
    },
    status() {
      write("Interface status: ready");
      write("Field posture: descriptive only");
      write("Coherence check: No blocker detected");
      write("Feedback into Φ: none");
    },
    guard() {
      write("Boot screen ≠ ontology initialization");
      write("Topology graph ≠ Φ itself");
      write("Terminal ≠ decision agent");
      write("DOI registry ≠ truth registry");
      write("Notes ≠ ontological memory");
    },
    clear() {
      output.textContent = "";
    }
  };

  input.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;
    const raw = input.value.trim();
    input.value = "";
    if (!raw) return;
    write(`vectaetos@field:~$ ${raw}`);

    const [cmd, arg] = raw.split(/\s+(.+)/);
    if (cmd === "open" && arg) {
      const target = arg.trim();
      const map = { paper: "papers", papers: "papers", doi: "doi", topology: "topology", licenses: "licenses", license: "licenses", notes: "notes", about: "about", settings: "settings" };
      if (map[target]) {
        openWindow(map[target]);
        write(`Opened ${target}.`);
      } else write(`Unknown module: ${target}`);
      return;
    }
    if (commands[raw]) commands[raw]();
    else if (commands[cmd]) commands[cmd](arg);
    else write(`Unknown command: ${raw}`);
  });

  wrap.append(output, line);
  setTimeout(() => input.focus(), 30);
  return wrap;
}

function renderPapers() {
  const wrap = el("div");
  const head = el("div", { class: "panel-head" }, [
    el("h2", { class: "h1" }, "VECTAETOS™ Publications"),
    el("span", { class: "small" }, `${papers.length} papers`)
  ]);
  const list = el("div", { class: "cards" });

  papers.forEach(p => {
    const details = el("div", { class: "small hidden" }, p.abstract);
    const card = el("article", { class: "card" }, [
      el("h3", { class: "card-title" }, p.title),
      el("a", { class: "doi", href: p.url, target: "_blank", rel: "noreferrer" }, p.doi),
      el("span", { class: "small" }, `   ${p.date}`),
      el("div", { class: "tags" }, p.tags.map(t => el("span", { class: "tag" }, t))),
      details
    ]);
    card.addEventListener("click", () => details.classList.toggle("hidden"));
    list.appendChild(card);
  });

  wrap.append(head, list);
  return wrap;
}

function renderDoi() {
  const wrap = el("div");
  const head = el("div", { class: "panel-head" }, [
    el("h2", { class: "h1" }, "DOI Registry"),
    el("span", { class: "small" }, `${doiRegistry.length} DOIs registered`)
  ]);
  const search = el("input", { class: "search", placeholder: "Search DOIs..." });
  const tabs = el("div", { class: "tabs" });
  const list = el("div", { class: "cards" });
  let filter = "all";

  ["all", "publication", "license"].forEach(t => {
    const b = el("button", { class: `tab ${t === "all" ? "active" : ""}` }, t.toUpperCase() + (t === "publication" ? "S" : t === "license" ? "S" : ""));
    b.addEventListener("click", () => {
      filter = t;
      tabs.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
      b.classList.add("active");
      render();
    });
    tabs.appendChild(b);
  });

  search.addEventListener("input", render);

  function render() {
    list.innerHTML = "";
    const q = search.value.toLowerCase();
    const rows = doiRegistry.filter(d => {
      const text = `${d.title} ${d.doi} ${d.type}`.toLowerCase();
      return (filter === "all" || d.type === filter) && text.includes(q);
    });
    if (!rows.length) {
      list.appendChild(el("div", { class: "empty" }, "No matching DOI entries."));
      return;
    }
    rows.forEach(d => {
      list.appendChild(el("article", { class: "card" }, [
        el("h3", { class: "card-title" }, d.title),
        el("a", { class: "doi", href: d.url, target: "_blank", rel: "noreferrer" }, d.doi),
        el("div", { class: "tags" }, [el("span", { class: "tag" }, d.type)])
      ]));
    });
  }

  render();
  wrap.append(head, search, tabs, list);
  return wrap;
}

function renderLicenses() {
  const wrap = el("div");
  wrap.append(
    el("div", { class: "panel-head" }, [
      el("h2", { class: "h1" }, "VECTAETOS™ License Stack"),
      el("span", { class: "small" }, `${licenses.length} licenses`)
    ]),
    el("p", { class: "small" }, "Layered custom license stack separating canonical ontology, identity/compatibility, implementation behavior, projection/trace artifacts, and software/tooling.")
  );

  const list = el("div", { class: "cards" });
  licenses.forEach(l => {
    list.appendChild(el("article", { class: "card license-card" }, [
      el("h3", { class: "card-title" }, l.title),
      el("span", { class: `badge ${l.warning ? "warn" : ""}` }, l.layer),
      el("a", { class: "doi", href: l.url, target: "_blank", rel: "noreferrer" }, l.doi),
      el("p", { class: "small" }, l.description)
    ]));
  });
  wrap.appendChild(list);
  return wrap;
}

function renderNotes() {
  const wrap = el("div");
  const saved = localStorage.getItem("vectaetos:notes") || `# VectaetOS Notes

Welcome to Vectaetos.

This is your local notepad.
It persists in this browser only.

---

"Knowledge appears as a topology of relational tensions."
`;
  const meta = el("div", { class: "panel-head" }, [
    el("h2", { class: "h1" }, "Notes"),
    el("span", { class: "small" }, "localStorage / browser local")
  ]);
  const area = el("textarea", { class: "notes-area", spellcheck: "true" });
  area.value = saved;
  area.addEventListener("input", () => {
    localStorage.setItem("vectaetos:notes", area.value);
    meta.lastChild.textContent = `${area.value.length} chars saved locally`;
  });
  wrap.append(meta, area);
  return wrap;
}

function renderAbout() {
  const wrap = el("div", { class: "about-card" });
  wrap.append(
    el("pre", { class: "ascii" }, `        /\\
       /  \\        VectaetOS
  /\\  / so \\       v1.0.0
 /__\\/______\\
     \\      /       Non-Agentic Onto-Epistemic
      \\____/        Field Operating System`),
    el("table", { class: "meta-table", html: `
      <tr><td>Framework</td><td>VECTAETOS™</td></tr>
      <tr><td>Algebra</td><td>so(8)</td></tr>
      <tr><td>Symmetry</td><td>Triality S₃</td></tr>
      <tr><td>Coherence</td><td>No blocker detected</td></tr>
      <tr><td>Field</td><td>non-agentic</td></tr>
      <tr><td>Projections</td><td>descriptive only</td></tr>
    `}),
    el("p", { class: "quote" }, "“Knowledge appears as a topology of relational tensions.”"),
    el("p", { class: "small" }, "— Richard Fonfára"),
    el("p", { class: "guard" }, "All projections are descriptive and non-prescriptive. This interface does not initialize, mutate, optimize, validate, or govern Φ.")
  );
  return wrap;
}

function renderSettings() {
  const wrap = el("div", { class: "settings-grid" });
  wrap.append(
    el("h2", { class: "h1" }, "Settings"),
    settingSwitch("Boot Animation", "bootAnimation", state.settings.bootAnimation !== false),
    settingSwitch("Window Animations", "windowAnimations", state.settings.windowAnimations !== false),
    optionGroup("Font Size", "font", ["small", "default", "large"], state.settings.font || "default"),
    optionGroup("Background", "theme", ["void", "grid", "field", "deep"], state.settings.theme || "field"),
    el("div", { class: "small" }, "Settings persist in this browser. They do not tune Φ.")
  );
  return wrap;
}

function settingSwitch(label, key, checked) {
  const input = el("input", { type: "checkbox" });
  input.checked = checked;
  input.addEventListener("change", () => {
    state.settings[key] = input.checked;
    saveSettings();
  });
  return el("div", { class: "setting-row" }, [
    el("span", {}, label),
    el("label", { class: "switch" }, [input, el("span")])
  ]);
}

function optionGroup(label, key, options, current) {
  const row = el("div", { class: "option-row" });
  options.forEach(opt => {
    const b = el("button", { class: `option ${opt === current ? "active" : ""}` }, opt);
    b.addEventListener("click", () => {
      state.settings[key] = opt;
      saveSettings();
      row.querySelectorAll(".option").forEach(x => x.classList.remove("active"));
      b.classList.add("active");
    });
    row.appendChild(b);
  });
  return el("div", { class: "settings-grid" }, [
    el("div", { class: "small" }, label),
    row
  ]);
}

function renderTopology() {
  const wrap = el("div", { class: "topology-wrap" }, [
    el("canvas", { id: "topologyCanvas" }),
    el("div", { class: "topology-caption" }, "Epistemic Field Topology — descriptive projection")
  ]);
  return wrap;
}

function drawTopology(canvas) {
  if (!canvas) return;
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * dpr));
  canvas.height = Math.max(1, Math.floor(rect.height * dpr));
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);

  const nodes = topology.nodes.map(n => ({ ...n, x: n.x * rect.width, y: n.y * rect.height }));
  let hover = null;

  function draw(t = 0) {
    ctx.clearRect(0, 0, rect.width, rect.height);
    ctx.lineWidth = 1;
    topology.edges.forEach(e => {
      const a = nodes.find(n => n.id === e[0]);
      const b = nodes.find(n => n.id === e[1]);
      if (!a || !b) return;
      ctx.strokeStyle = "rgba(49,255,119,.11)";
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    });

    nodes.forEach(n => {
      const pulse = 1 + Math.sin(t / 650 + n.x) * .08;
      const r = (n.r || 8) * pulse;
      ctx.fillStyle = "rgba(49,255,119,.09)";
      ctx.beginPath();
      ctx.arc(n.x, n.y, r * 4.6, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = hover === n.id ? "rgba(121,255,174,.95)" : "rgba(41,210,103,.78)";
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = hover === n.id ? "#d9ffdf" : "rgba(214,222,214,.62)";
      ctx.font = "12px ui-monospace, monospace";
      ctx.fillText(n.label, n.x + 12, n.y + 4);
    });

    requestAnimationFrame(draw);
  }

  canvas.onmousemove = (ev) => {
    const cr = canvas.getBoundingClientRect();
    const x = ev.clientX - cr.left;
    const y = ev.clientY - cr.top;
    hover = null;
    for (const n of nodes) {
      if (Math.hypot(n.x - x, n.y - y) < 20) hover = n.id;
    }
  };
  canvas.onmouseleave = () => { hover = null; };
  draw();
}

function startAmbient() {
  const canvas = document.querySelector("#ambientCanvas");
  const ctx = canvas.getContext("2d");
  let w, h, points;

  function resize() {
    const dpr = window.devicePixelRatio || 1;
    w = canvas.clientWidth;
    h = canvas.clientHeight;
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    points = Array.from({ length: 55 }, (_, i) => ({
      x: Math.random() * w,
      y: Math.random() * h,
      a: Math.random() * Math.PI * 2,
      s: .12 + Math.random() * .22
    }));
  }
  window.addEventListener("resize", resize);
  resize();

  function frame() {
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = "rgba(49,255,119,.04)";
    for (const p of points) {
      p.a += 0.002;
      p.x += Math.cos(p.a) * p.s;
      p.y += Math.sin(p.a) * p.s;
      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 1.3, 0, Math.PI * 2);
      ctx.fill();
    }
    requestAnimationFrame(frame);
  }
  frame();
}
