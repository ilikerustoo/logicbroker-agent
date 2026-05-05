// Shared agent simulation logic — canned response that streams in with delays.
// Exposes <AgentLoop>, <Markdown>, sample queries, and a useAgent() hook.

const SAMPLE_QUERIES = [
  "How do I configure a new retailer connection?",
  "What's the schema for shipment confirmations?",
  "Difference between order ack and order release?",
  "Rate limits on the partner API",
];

// One canned conversation per query — keyed by lowercased query, with a default fallback.
const CANNED = {
  "how do i configure a new retailer connection?": {
    steps: [
      { kind: "shell", text: "$ logic-agent ask \"How do I configure a new retailer connection?\"" },
      { kind: "dim",   text: "[init] loading kb index … 14,832 docs · 312 collections" },
      { kind: "step",  tool: "search_kb", arg: "retailer connection setup", delay: 600 },
      { kind: "result", text: "→ 7 hits · top: docs/connections/retailer-onboarding.md (0.91)" },
      { kind: "step",  tool: "read_doc", arg: "docs/connections/retailer-onboarding.md", delay: 700 },
      { kind: "result", text: "→ 4,210 tokens · sections: [Auth, Endpoints, Mapping, Test Mode]" },
      { kind: "step",  tool: "search_kb", arg: "credentials rotation partner", delay: 500 },
      { kind: "result", text: "→ 3 hits · top: docs/auth/credentials.md (0.78)" },
      { kind: "step",  tool: "read_doc", arg: "docs/auth/credentials.md", delay: 600 },
      { kind: "result", text: "→ 1,108 tokens" },
      { kind: "dim",   text: "[think] composing answer · 2 sources · 6,318 ctx tokens" },
      { kind: "ok",    text: "✓ done in 4.2s · 11 steps · $0.018" },
    ],
    answer: {
      md: [
        "To onboard a new retailer connection in Logicbroker:",
        "",
        "1. **Request credentials** from the retailer's EDI contact — you'll need a `subscription_key` and a `partner_id`.",
        "2. In the Commerce Network UI, go to **Connections → New** and select the retailer template. Templates pre-fill endpoint URLs and field mappings.",
        "3. Drop credentials into **Settings → Auth Profiles**. Rotate every 90 days; the agent will warn you 14 days out.",
        "4. Map your SKUs against the retailer's catalog under **Mapping → Items**. Unmapped SKUs are quarantined, not rejected.",
        "5. Flip the connection to **Test Mode**, send 3 sample POs, and verify the round-trip in **Activity**.",
        "",
        "Once test mode passes 24 hours clean, request **Production** from your CSM.",
      ],
      sources: [
        { path: "docs/connections/retailer-onboarding.md", section: "Endpoints" },
        { path: "docs/auth/credentials.md", section: "Rotation policy" },
      ],
    },
  },
};

const DEFAULT_CANNED = {
  steps: [
    { kind: "shell", text: "$ logic-agent ask …" },
    { kind: "dim",   text: "[init] loading kb index … 14,832 docs · 312 collections" },
    { kind: "step",  tool: "search_kb", arg: "(query)", delay: 500 },
    { kind: "result", text: "→ 5 hits" },
    { kind: "step",  tool: "read_doc", arg: "docs/api/overview.md", delay: 600 },
    { kind: "result", text: "→ 2,104 tokens" },
    { kind: "step",  tool: "search_kb", arg: "examples", delay: 500 },
    { kind: "result", text: "→ 4 hits" },
    { kind: "dim",   text: "[think] composing answer" },
    { kind: "ok",    text: "✓ done in 3.1s · 7 steps · $0.011" },
  ],
  answer: {
    md: [
      "Here's a synthesized answer pulled from the Logicbroker knowledge base. The agent reads relevant docs, cross-references examples, and composes a response with citations.",
      "",
      "Replace this with the actual answer for your query — the prototype ships with one fully-canned example (\"How do I configure a new retailer connection?\"); other queries fall back to this generic trace.",
    ],
    sources: [
      { path: "docs/api/overview.md", section: "Concepts" },
    ],
  },
};

function getCanned(query) {
  const key = (query || "").trim().toLowerCase();
  return CANNED[key] || DEFAULT_CANNED;
}

// Hook: drives a single agent run. Returns trace lines, answer (or null while streaming), status.
function useAgent() {
  const [history, setHistory] = React.useState([]); // [{id, query, trace, answer, done}]
  const [activeId, setActiveId] = React.useState(null);
  const timersRef = React.useRef([]);

  const clearTimers = () => {
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];
  };

  const ask = React.useCallback((query) => {
    if (!query || !query.trim()) return;
    clearTimers();
    const id = Math.random().toString(36).slice(2, 9);
    const canned = getCanned(query);
    const entry = { id, query: query.trim(), trace: [], answer: null, done: false };

    setHistory((h) => [entry, ...h]);
    setActiveId(id);

    // Stream in trace lines with delays, then reveal answer.
    let acc = 0;
    canned.steps.forEach((step, i) => {
      const delay = step.delay ?? 350;
      acc += delay;
      const t = setTimeout(() => {
        setHistory((h) => h.map((e) => e.id === id ? { ...e, trace: [...e.trace, { ...step, key: i }] } : e));
      }, acc);
      timersRef.current.push(t);
    });
    acc += 600;
    const finalT = setTimeout(() => {
      setHistory((h) => h.map((e) => e.id === id ? { ...e, answer: canned.answer, done: true } : e));
    }, acc);
    timersRef.current.push(finalT);
  }, []);

  const select = React.useCallback((id) => setActiveId(id), []);
  const active = history.find((e) => e.id === activeId) || null;

  React.useEffect(() => () => clearTimers(), []);

  return { history, active, ask, select };
}

// Renders a trace line with simple ANSI-ish coloring.
function TraceLine({ step, palette }) {
  const c = palette;
  if (step.kind === "shell") {
    return (
      <div style={{ color: c.fg }}>
        <span style={{ color: c.dim }}>›</span> {step.text}
      </div>
    );
  }
  if (step.kind === "dim") {
    return <div style={{ color: c.dim }}>{step.text}</div>;
  }
  if (step.kind === "step") {
    return (
      <div style={{ color: c.fg }}>
        <span style={{ color: c.accent }}>⟶</span>{" "}
        <span style={{ color: c.cyan }}>{step.tool}</span>
        <span style={{ color: c.dim }}>(</span>
        <span style={{ color: c.yellow }}>"{step.arg}"</span>
        <span style={{ color: c.dim }}>)</span>
      </div>
    );
  }
  if (step.kind === "result") {
    return <div style={{ color: c.dim, paddingLeft: 14 }}>{step.text}</div>;
  }
  if (step.kind === "ok") {
    return <div style={{ color: c.accent, marginTop: 6 }}>{step.text}</div>;
  }
  return <div style={{ color: c.fg }}>{step.text}</div>;
}

// A simple terminal viewport. `compact` shrinks padding/font.
function Terminal({ trace, palette, height, blink, label }) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    if (ref.current) ref.current.scrollTop = ref.current.scrollHeight;
  }, [trace.length]);
  return (
    <div style={{
      background: palette.bg,
      border: `1px solid ${palette.border}`,
      borderRadius: 6,
      fontFamily: "'JetBrains Mono', ui-monospace, monospace",
      fontSize: 11.5,
      lineHeight: 1.7,
      color: palette.fg,
      display: "flex",
      flexDirection: "column",
      height,
      overflow: "hidden",
    }}>
      <div style={{
        padding: "8px 12px",
        borderBottom: `1px solid ${palette.border}`,
        color: palette.dim,
        fontSize: 10.5,
        letterSpacing: 0.4,
        textTransform: "uppercase",
        display: "flex",
        justifyContent: "space-between",
      }}>
        <span>{label || "agent.loop"}</span>
        <span>{trace.length} step{trace.length === 1 ? "" : "s"}</span>
      </div>
      <div ref={ref} style={{ padding: "10px 14px", overflowY: "auto", flex: 1 }}>
        {trace.length === 0 && (
          <div style={{ color: palette.dim }}>
            <span style={{ color: palette.accent }}>●</span> idle · waiting for query
          </div>
        )}
        {trace.map((step) => <TraceLine key={step.key} step={step} palette={palette} />)}
        {blink && trace.length > 0 && (
          <span style={{
            display: "inline-block",
            width: 7, height: 13,
            background: palette.fg,
            verticalAlign: "text-bottom",
            animation: "blink 1s steps(2) infinite",
          }} />
        )}
      </div>
    </div>
  );
}

// Tiny markdown renderer — handles headings, bold, italic, code, lists, paragraphs.
function renderMd(lines) {
  const out = [];
  let listBuf = null;
  const flushList = () => {
    if (listBuf) {
      out.push(<ol key={out.length} style={{ paddingLeft: 22, margin: "10px 0", display: "flex", flexDirection: "column", gap: 8 }}>
        {listBuf.map((it, i) => <li key={i} dangerouslySetInnerHTML={{ __html: inline(it) }} />)}
      </ol>);
      listBuf = null;
    }
  };
  const inline = (s) =>
    s.replace(/`([^`]+)`/g, "<code style=\"font-family: 'JetBrains Mono', monospace; font-size: 0.92em; background: rgba(127,127,127,0.18); padding: 1px 5px; border-radius: 3px;\">$1</code>")
     .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
     .replace(/\*([^*]+)\*/g, "<em>$1</em>");

  lines.forEach((ln, i) => {
    const m = ln.match(/^(\d+)\.\s+(.*)/);
    if (m) {
      if (!listBuf) listBuf = [];
      listBuf.push(m[2]);
      return;
    }
    flushList();
    if (ln.trim() === "") {
      out.push(<div key={i} style={{ height: 4 }} />);
      return;
    }
    out.push(<p key={i} style={{ margin: "8px 0", lineHeight: 1.6 }} dangerouslySetInnerHTML={{ __html: inline(ln) }} />);
  });
  flushList();
  return out;
}

Object.assign(window, { useAgent, Terminal, renderMd, SAMPLE_QUERIES, getCanned });
