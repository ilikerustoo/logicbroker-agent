import React, { useState, useRef, useEffect, useCallback } from "react";

// ─── Dracula palette ───────────────────────────────────────────────

const DRAC = {
  bg: "#282A36",
  bgAlt: "#21222C",
  line: "#44475A",
  fg: "#F8F8F2",
  comment: "#6272A4",
  pink: "#FF79C6",
  purple: "#BD93F9",
  cyan: "#8BE9FD",
  green: "#50FA7B",
  yellow: "#F1FA8C",
  orange: "#FFB86C",
  red: "#FF5555",
};

const PALETTE = {
  bg: DRAC.bg,
  border: "rgba(248,248,242,0.08)",
  fg: DRAC.fg,
  dim: DRAC.comment,
  accent: DRAC.green,
  cyan: DRAC.cyan,
  yellow: DRAC.yellow,
};

const SAMPLE_QUERIES = [
  "How do I configure a new retailer connection?",
  "What EDI document types does Logicbroker support?",
  "How do I set up order acknowledgements?",
  "Explain the shipment API endpoints",
];

// ─── SSE hook — streams from the real agent ────────────────────────

let _nextId = 1;

function useAgent() {
  const [history, setHistory] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const abortRef = useRef(null);

  const active = history.find((h) => h.id === activeId) || null;

  const ask = useCallback((query) => {
    // Abort any running request
    if (abortRef.current) abortRef.current.abort();

    const id = _nextId++;
    const entry = { id, query, trace: [], answer: null, done: false, error: null };

    setHistory((prev) => [entry, ...prev]);
    setActiveId(id);

    const ctrl = new AbortController();
    abortRef.current = ctrl;

    // Start SSE fetch
    fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
      signal: ctrl.signal,
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          // Parse SSE events from buffer
          const lines = buffer.split("\n");
          buffer = lines.pop(); // keep incomplete line

          let eventType = null;
          let dataStr = "";

          for (const line of lines) {
            if (line.startsWith("event: ")) {
              eventType = line.slice(7).trim();
            } else if (line.startsWith("data: ")) {
              dataStr = line.slice(6);
            } else if (line === "" && eventType && dataStr) {
              // Complete event
              try {
                const data = JSON.parse(dataStr);
                handleEvent(id, eventType, data);
              } catch {
                // ignore parse errors
              }
              eventType = null;
              dataStr = "";
            }
          }
        }
      })
      .catch((err) => {
        if (err.name === "AbortError") return;
        setHistory((prev) =>
          prev.map((h) =>
            h.id === id ? { ...h, done: true, error: err.message } : h
          )
        );
      });
  }, []);

  function handleEvent(id, event, data) {
    if (event === "trace") {
      setHistory((prev) =>
        prev.map((h) =>
          h.id === id ? { ...h, trace: [...h.trace, data] } : h
        )
      );
    } else if (event === "answer") {
      setHistory((prev) =>
        prev.map((h) =>
          h.id === id ? { ...h, answer: data } : h
        )
      );
    } else if (event === "error") {
      setHistory((prev) =>
        prev.map((h) =>
          h.id === id ? { ...h, error: data.message, done: true } : h
        )
      );
    } else if (event === "done") {
      setHistory((prev) =>
        prev.map((h) =>
          h.id === id ? { ...h, done: true } : h
        )
      );
    }
  }

  const select = useCallback((id) => setActiveId(id), []);

  return { history, active, ask, select };
}

// ─── Terminal component ────────────────────────────────────────────

function TraceLine({ step, palette }) {
  const p = palette;
  if (step.kind === "shell") {
    return (
      <div style={{ color: p.dim }}>
        <span style={{ color: p.accent }}>{">"}</span> {step.text}
      </div>
    );
  }
  if (step.kind === "dim") {
    return <div style={{ color: p.dim, fontStyle: "italic" }}>{step.text}</div>;
  }
  if (step.kind === "step") {
    return (
      <div>
        <span style={{ color: p.dim }}>{"  \u2192 "}</span>
        <span style={{ color: p.cyan }}>{step.tool}</span>
        <span style={{ color: p.yellow }}> {step.arg}</span>
      </div>
    );
  }
  if (step.kind === "result") {
    return <div style={{ color: p.dim }}>{step.text}</div>;
  }
  if (step.kind === "ok") {
    return (
      <div style={{ color: p.accent, marginTop: 6 }}>
        {"  \u2713 "}{step.text}
      </div>
    );
  }
  return <div style={{ color: p.fg }}>{step.text}</div>;
}

function Terminal({ trace, palette, blink, label }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [trace.length]);

  return (
    <div
      style={{
        background: palette.bg,
        border: `1px solid ${palette.border}`,
        borderRadius: 6,
        height: "100%",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "8px 12px",
          fontSize: 10.5,
          letterSpacing: 0.6,
          textTransform: "uppercase",
          color: palette.dim,
          borderBottom: `1px solid ${palette.border}`,
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <span>{label}</span>
        <span>{trace.length} steps</span>
      </div>
      <div
        ref={scrollRef}
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "10px 14px",
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 11.5,
          lineHeight: 1.7,
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}
      >
        {trace.map((step, i) => (
          <TraceLine key={i} step={step} palette={palette} />
        ))}
        {blink && (
          <span
            style={{
              display: "inline-block",
              width: 7,
              height: 14,
              background: palette.accent,
              animation: "blink 1s steps(2) infinite",
              verticalAlign: "middle",
              marginLeft: 2,
            }}
          />
        )}
      </div>
    </div>
  );
}

// ─── Markdown renderer (minimal) ──────────────────────────────────

function renderMd(text) {
  if (!text) return null;
  const lines = text.split("\n");
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Numbered list
    const listMatch = line.match(/^(\d+)\.\s+(.+)/);
    if (listMatch) {
      elements.push(
        <div key={i} style={{ display: "flex", gap: 8, marginBottom: 4 }}>
          <span style={{ color: DRAC.comment, minWidth: 18, textAlign: "right" }}>
            {listMatch[1]}.
          </span>
          <span>{inlineMd(listMatch[2])}</span>
        </div>
      );
      i++;
      continue;
    }

    // Empty line
    if (!line.trim()) {
      elements.push(<div key={i} style={{ height: 8 }} />);
      i++;
      continue;
    }

    // Paragraph
    elements.push(
      <p key={i} style={{ margin: "0 0 8px", lineHeight: 1.6 }}>
        {inlineMd(line)}
      </p>
    );
    i++;
  }

  return elements;
}

function inlineMd(text) {
  const parts = [];
  let remaining = text;
  let key = 0;

  while (remaining) {
    // Bold
    const boldMatch = remaining.match(/\*\*(.+?)\*\*/);
    // Inline code
    const codeMatch = remaining.match(/`(.+?)`/);
    // Citation [N]
    const citeMatch = remaining.match(/\[(\d+)\]/);

    // Find earliest match
    let earliest = null;
    let earliestIdx = Infinity;

    if (boldMatch && boldMatch.index < earliestIdx) {
      earliest = { type: "bold", match: boldMatch };
      earliestIdx = boldMatch.index;
    }
    if (codeMatch && codeMatch.index < earliestIdx) {
      earliest = { type: "code", match: codeMatch };
      earliestIdx = codeMatch.index;
    }
    if (citeMatch && citeMatch.index < earliestIdx) {
      earliest = { type: "cite", match: citeMatch };
      earliestIdx = citeMatch.index;
    }

    if (!earliest) {
      parts.push(<span key={key++}>{remaining}</span>);
      break;
    }

    // Text before match
    if (earliestIdx > 0) {
      parts.push(<span key={key++}>{remaining.slice(0, earliestIdx)}</span>);
    }

    const m = earliest.match;
    if (earliest.type === "bold") {
      parts.push(
        <strong key={key++} style={{ fontWeight: 600 }}>
          {m[1]}
        </strong>
      );
    } else if (earliest.type === "code") {
      parts.push(
        <code
          key={key++}
          style={{
            background: "rgba(189,147,249,0.15)",
            padding: "1px 5px",
            borderRadius: 3,
            fontSize: "0.9em",
            fontFamily: "'JetBrains Mono', monospace",
          }}
        >
          {m[1]}
        </code>
      );
    } else if (earliest.type === "cite") {
      parts.push(
        <sup
          key={key++}
          style={{
            color: DRAC.cyan,
            fontSize: "0.75em",
            fontWeight: 600,
            marginLeft: 1,
          }}
        >
          [{m[1]}]
        </sup>
      );
    }

    remaining = remaining.slice(earliestIdx + m[0].length);
  }

  return parts;
}

// ─── Answer panel ──────────────────────────────────────────────────

function AnswerPanel({ answer }) {
  if (!answer) return null;

  return (
    <div style={{ color: DRAC.fg, fontSize: 14.5 }}>
      {renderMd(answer.text)}

      {answer.sources && answer.sources.length > 0 && (
        <div
          style={{
            marginTop: 22,
            paddingTop: 14,
            borderTop: "1px solid rgba(248,248,242,0.10)",
          }}
        >
          <div
            style={{
              fontSize: 10.5,
              letterSpacing: 0.6,
              textTransform: "uppercase",
              color: DRAC.comment,
              marginBottom: 8,
            }}
          >
            Sources
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            {answer.sources.map((s, i) => (
              <a
                key={i}
                href={s.url || "#"}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => { if (!s.url) e.preventDefault(); }}
                style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 12,
                  color: DRAC.cyan,
                  textDecoration: "none",
                  borderBottom: "1px dashed rgba(248,248,242,0.10)",
                  paddingBottom: 4,
                }}
              >
                <span style={{ color: DRAC.pink }}>{"\u2197"}</span> {s.title}
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── History sidebar items ─────────────────────────────────────────

function HistoryItem({ entry, active, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        display: "block",
        width: "100%",
        textAlign: "left",
        background: active ? "rgba(189,147,249,0.14)" : "transparent",
        border: "none",
        borderLeft: active
          ? `2px solid ${DRAC.purple}`
          : "2px solid transparent",
        padding: "8px 10px 8px 12px",
        fontFamily: "inherit",
        fontSize: 12.5,
        color: DRAC.fg,
        cursor: "pointer",
        lineHeight: 1.4,
      }}
    >
      <div
        style={{
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
          opacity: active ? 1 : 0.78,
        }}
      >
        {entry.query}
      </div>
      <div style={{ fontSize: 10.5, color: DRAC.comment, marginTop: 2 }}>
        {entry.done
          ? `${entry.trace.length} steps`
          : `${entry.trace.length} step${entry.trace.length === 1 ? "" : "s"} \u00b7 streaming\u2026`}
      </div>
    </button>
  );
}

function SampleChip({ children, onClick }) {
  const [hover, setHover] = useState(false);
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        fontFamily: "inherit",
        fontSize: 12,
        color: DRAC.fg,
        background: hover ? "rgba(189,147,249,0.18)" : "rgba(98,114,164,0.18)",
        border: `1px solid ${hover ? DRAC.purple : DRAC.line}`,
        borderRadius: 999,
        padding: "5px 12px",
        cursor: "pointer",
        whiteSpace: "nowrap",
      }}
    >
      {children}
    </button>
  );
}

// ─── Main app ──────────────────────────────────────────────────────

export default function App() {
  const { history, active, ask, select } = useAgent();
  const [q, setQ] = useState("");
  const inputRef = useRef(null);

  const submit = (text) => {
    const v = (text ?? q).trim();
    if (!v) return;
    ask(v);
    setQ("");
  };

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        background: DRAC.bg,
        color: DRAC.fg,
        fontFamily: "'Inter', system-ui, sans-serif",
        display: "grid",
        gridTemplateColumns: "220px 1fr 480px",
        overflow: "hidden",
      }}
    >
      {/* ─── History rail ─── */}
      <aside
        style={{
          borderRight: `1px solid ${DRAC.line}`,
          padding: "22px 0",
          display: "flex",
          flexDirection: "column",
          background: DRAC.bgAlt,
        }}
      >
        <div
          style={{
            padding: "0 18px 18px",
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <div
            style={{
              width: 9,
              height: 9,
              borderRadius: 2,
              background: DRAC.pink,
            }}
          />
          <div
            style={{
              fontSize: 13,
              fontWeight: 600,
              letterSpacing: -0.1,
              color: DRAC.fg,
            }}
          >
            Logicbroker Agent
          </div>
        </div>

        <button
          onClick={() => {
            setQ("");
            setTimeout(() => inputRef.current?.focus(), 0);
          }}
          style={{
            margin: "0 14px 14px",
            padding: "8px 10px",
            border: `1px solid ${DRAC.line}`,
            borderRadius: 4,
            background: "transparent",
            cursor: "pointer",
            fontFamily: "inherit",
            fontSize: 12,
            color: DRAC.fg,
            textAlign: "left",
          }}
        >
          + New query
        </button>

        <div
          style={{
            fontSize: 10.5,
            letterSpacing: 0.6,
            textTransform: "uppercase",
            color: DRAC.comment,
            padding: "6px 18px 4px",
          }}
        >
          History
        </div>

        <div style={{ flex: 1, overflowY: "auto" }}>
          {history.length === 0 && (
            <div
              style={{ padding: "10px 18px", fontSize: 12, color: DRAC.comment }}
            >
              Nothing yet.
            </div>
          )}
          {history.map((e) => (
            <HistoryItem
              key={e.id}
              entry={e}
              active={active?.id === e.id}
              onClick={() => select(e.id)}
            />
          ))}
        </div>
      </aside>

      {/* ─── Q & A column ─── */}
      <main
        style={{
          padding: "44px 60px 28px",
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}
      >
        {!active && (
          <div style={{ marginBottom: 18 }}>
            <div
              style={{
                fontSize: 11,
                letterSpacing: 1.2,
                textTransform: "uppercase",
                color: DRAC.comment,
                marginBottom: 12,
              }}
            >
              <span style={{ color: DRAC.pink }}>{"\u25cf"}</span> Knowledge base
            </div>
            <h1
              style={{
                fontFamily: "'Inter', sans-serif",
                fontSize: 38,
                lineHeight: 1.05,
                fontWeight: 500,
                letterSpacing: -0.8,
                margin: 0,
                textWrap: "balance",
                color: DRAC.fg,
              }}
            >
              Ask the{" "}
              <span style={{ color: DRAC.purple }}>Logicbroker</span>
              <br />
              knowledge base.
            </h1>
            <p
              style={{
                marginTop: 14,
                fontSize: 14.5,
                color: DRAC.comment,
                maxWidth: 480,
                lineHeight: 1.55,
              }}
            >
              The agent searches docs, reads sources, and composes a cited
              answer. Watch its loop on the right.
            </p>
          </div>
        )}

        {active && (
          <div
            style={{
              flex: 1,
              overflowY: "auto",
              paddingRight: 8,
              marginBottom: 18,
            }}
          >
            <div
              style={{
                fontSize: 11,
                letterSpacing: 1.2,
                textTransform: "uppercase",
                color: DRAC.comment,
                marginBottom: 8,
              }}
            >
              Query
            </div>
            <div
              style={{
                fontSize: 22,
                fontWeight: 500,
                letterSpacing: -0.3,
                lineHeight: 1.25,
                marginBottom: 28,
                textWrap: "balance",
                color: DRAC.fg,
              }}
            >
              {active.query}
            </div>

            {active.error && (
              <div style={{ color: DRAC.red, fontSize: 13, marginBottom: 16 }}>
                Error: {active.error}
              </div>
            )}

            {active.answer ? (
              <AnswerPanel answer={active.answer} />
            ) : (
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  color: DRAC.comment,
                  fontSize: 13,
                }}
              >
                <span
                  style={{
                    width: 10,
                    height: 10,
                    borderRadius: "50%",
                    background: DRAC.green,
                    animation: "pulse 1.4s ease-in-out infinite",
                  }}
                />
                Thinking — {active.trace.length} step
                {active.trace.length === 1 ? "" : "s"} so far
              </div>
            )}
          </div>
        )}

        {/* ─── Input ─── */}
        <div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              border: `1px solid ${DRAC.line}`,
              borderRadius: 6,
              background: DRAC.bgAlt,
              padding: "0 4px 0 14px",
              transition: "border 0.15s",
            }}
          >
            <span
              style={{
                color: DRAC.green,
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 13,
                marginRight: 10,
              }}
            >
              {"\u203a"}
            </span>
            <input
              ref={inputRef}
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") submit();
              }}
              placeholder="Ask anything in the knowledge base\u2026"
              style={{
                flex: 1,
                border: "none",
                outline: "none",
                fontFamily: "inherit",
                fontSize: 14,
                padding: "12px 0",
                background: "transparent",
                color: DRAC.fg,
              }}
            />
            <button
              onClick={() => submit()}
              disabled={!q.trim()}
              style={{
                padding: "7px 14px",
                background: q.trim() ? DRAC.purple : DRAC.line,
                color: q.trim() ? DRAC.bg : DRAC.comment,
                border: "none",
                borderRadius: 4,
                fontFamily: "inherit",
                fontSize: 12.5,
                fontWeight: 600,
                cursor: q.trim() ? "pointer" : "default",
                margin: "4px",
              }}
            >
              Run {"\u21b5"}
            </button>
          </div>
          <div
            style={{
              display: "flex",
              gap: 6,
              marginTop: 12,
              flexWrap: "wrap",
            }}
          >
            {SAMPLE_QUERIES.map((s) => (
              <SampleChip key={s} onClick={() => submit(s)}>
                {s}
              </SampleChip>
            ))}
          </div>
        </div>
      </main>

      {/* ─── Live terminal ─── */}
      <section
        style={{
          background: DRAC.bgAlt,
          borderLeft: `1px solid ${DRAC.line}`,
          padding: "22px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            fontSize: 10.5,
            letterSpacing: 0.6,
            textTransform: "uppercase",
            color: DRAC.comment,
            marginBottom: 12,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <span>Agent loop</span>
          <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span
              style={{
                width: 7,
                height: 7,
                borderRadius: "50%",
                background:
                  active && !active.done ? DRAC.green : DRAC.line,
                animation:
                  active && !active.done
                    ? "pulse 1.4s ease-in-out infinite"
                    : "none",
              }}
            />
            <span
              style={{
                color:
                  active && !active.done ? DRAC.green : DRAC.comment,
              }}
            >
              {active && !active.done ? "running" : "idle"}
            </span>
          </span>
        </div>
        <div style={{ flex: 1, minHeight: 0 }}>
          <Terminal
            trace={active?.trace || []}
            palette={PALETTE}
            blink={active != null && !active.done}
            label="logic-agent"
          />
        </div>
      </section>
    </div>
  );
}
