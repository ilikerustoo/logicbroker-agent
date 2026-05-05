// Two variations of the Logicbroker Agent site.

// Dracula theme — https://draculatheme.com
const DRAC = {
  bg:        "#282A36",
  bgAlt:     "#21222C",
  line:      "#44475A",
  fg:        "#F8F8F2",
  comment:   "#6272A4",
  pink:      "#FF79C6",
  purple:    "#BD93F9",
  cyan:      "#8BE9FD",
  green:     "#50FA7B",
  yellow:    "#F1FA8C",
  orange:    "#FFB86C",
  red:       "#FF5555",
};

const PALETTE_A = {
  bg: DRAC.bg,
  border: "rgba(248,248,242,0.08)",
  fg: DRAC.fg,
  dim: DRAC.comment,
  accent: DRAC.green,
  cyan: DRAC.cyan,
  yellow: DRAC.yellow,
};

const PALETTE_B = {
  // Variation B: light terminal — ink-on-paper (unchanged)
  bg: "#F4F2EC",
  border: "rgba(20,20,15,0.10)",
  fg: "#14140F",
  dim: "rgba(20,20,15,0.45)",
  accent: "#3B7A2E",
  cyan: "#2C6B7A",
  yellow: "#8A6A12",
};

function Chip({ children, onClick }) {
  return (
    <button onClick={onClick} style={{
      fontFamily: "inherit",
      fontSize: 12,
      color: "#14140F",
      background: "transparent",
      border: "1px solid rgba(20,20,15,0.15)",
      borderRadius: 999,
      padding: "5px 12px",
      cursor: "pointer",
      whiteSpace: "nowrap",
    }}
    onMouseEnter={(e) => e.currentTarget.style.background = "rgba(20,20,15,0.04)"}
    onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
    >
      {children}
    </button>
  );
}

function HistoryItem({ entry, active, onClick }) {
  return (
    <button onClick={onClick} style={{
      display: "block",
      width: "100%",
      textAlign: "left",
      background: active ? "rgba(20,20,15,0.06)" : "transparent",
      border: "none",
      borderLeft: active ? "2px solid #14140F" : "2px solid transparent",
      padding: "8px 10px 8px 12px",
      fontFamily: "inherit",
      fontSize: 12.5,
      color: "#14140F",
      cursor: "pointer",
      lineHeight: 1.4,
    }}>
      <div style={{
        whiteSpace: "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
        opacity: active ? 1 : 0.75,
      }}>{entry.query}</div>
      <div style={{ fontSize: 10.5, color: "rgba(20,20,15,0.45)", marginTop: 2 }}>
        {entry.done ? `${entry.trace.length} steps` : `${entry.trace.length} step${entry.trace.length === 1 ? "" : "s"} · streaming…`}
      </div>
    </button>
  );
}

function AnswerBlock({ answer, dark }) {
  if (!answer) return null;
  const fg = dark ? "#EDEAE0" : "#14140F";
  const dim = dark ? "rgba(237,234,224,0.55)" : "rgba(20,20,15,0.55)";
  const border = dark ? "rgba(255,255,255,0.10)" : "rgba(20,20,15,0.10)";
  return (
    <div style={{ color: fg, fontSize: 14.5 }}>
      {renderMd(answer.md)}
      <div style={{
        marginTop: 22,
        paddingTop: 14,
        borderTop: `1px solid ${border}`,
      }}>
        <div style={{ fontSize: 10.5, letterSpacing: 0.6, textTransform: "uppercase", color: dim, marginBottom: 8 }}>
          Sources
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {answer.sources.map((s, i) => (
            <a key={i} href="#" onClick={(e) => e.preventDefault()} style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 12,
              color: fg,
              textDecoration: "none",
              borderBottom: `1px dashed ${border}`,
              paddingBottom: 4,
            }}>
              <span style={{ color: dim }}>↗</span> {s.path}
              <span style={{ color: dim }}> · {s.section}</span>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

// Dracula chip and history item — used only by Variation A
function DracChip({ children, onClick }) {
  return (
    <button onClick={onClick} style={{
      fontFamily: "inherit",
      fontSize: 12,
      color: DRAC.fg,
      background: "rgba(98,114,164,0.18)",
      border: `1px solid ${DRAC.line}`,
      borderRadius: 999,
      padding: "5px 12px",
      cursor: "pointer",
      whiteSpace: "nowrap",
    }}
    onMouseEnter={(e) => { e.currentTarget.style.background = "rgba(189,147,249,0.18)"; e.currentTarget.style.borderColor = DRAC.purple; }}
    onMouseLeave={(e) => { e.currentTarget.style.background = "rgba(98,114,164,0.18)"; e.currentTarget.style.borderColor = DRAC.line; }}
    >
      {children}
    </button>
  );
}

function DracHistoryItem({ entry, active, onClick }) {
  return (
    <button onClick={onClick} style={{
      display: "block",
      width: "100%",
      textAlign: "left",
      background: active ? "rgba(189,147,249,0.14)" : "transparent",
      border: "none",
      borderLeft: active ? `2px solid ${DRAC.purple}` : "2px solid transparent",
      padding: "8px 10px 8px 12px",
      fontFamily: "inherit",
      fontSize: 12.5,
      color: DRAC.fg,
      cursor: "pointer",
      lineHeight: 1.4,
    }}>
      <div style={{
        whiteSpace: "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
        opacity: active ? 1 : 0.78,
      }}>{entry.query}</div>
      <div style={{ fontSize: 10.5, color: DRAC.comment, marginTop: 2 }}>
        {entry.done ? `${entry.trace.length} steps` : `${entry.trace.length} step${entry.trace.length === 1 ? "" : "s"} · streaming…`}
      </div>
    </button>
  );
}

function DracAnswer({ answer }) {
  if (!answer) return null;
  const fg = DRAC.fg, dim = DRAC.comment, border = "rgba(248,248,242,0.10)";
  return (
    <div style={{ color: fg, fontSize: 14.5 }}>
      {renderMd(answer.md)}
      <div style={{ marginTop: 22, paddingTop: 14, borderTop: `1px solid ${border}` }}>
        <div style={{ fontSize: 10.5, letterSpacing: 0.6, textTransform: "uppercase", color: dim, marginBottom: 8 }}>Sources</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {answer.sources.map((s, i) => (
            <a key={i} href="#" onClick={(e) => e.preventDefault()} style={{
              fontFamily: "'JetBrains Mono', monospace", fontSize: 12,
              color: DRAC.cyan, textDecoration: "none",
              borderBottom: `1px dashed ${border}`, paddingBottom: 4,
            }}>
              <span style={{ color: DRAC.pink }}>↗</span> {s.path}
              <span style={{ color: dim }}> · {s.section}</span>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

// ───────────────────────────── Variation A (Dracula) ─────────────────────────────
function VariationA() {
  const { history, active, ask, select } = useAgent();
  const [q, setQ] = React.useState("");
  const inputRef = React.useRef(null);

  const submit = (text) => {
    const v = (text ?? q).trim();
    if (!v) return;
    ask(v);
    setQ("");
  };

  return (
    <div style={{
      width: 1200, height: 760,
      background: DRAC.bg,
      color: DRAC.fg,
      fontFamily: "'Inter', system-ui, sans-serif",
      display: "grid",
      gridTemplateColumns: "200px 1fr 460px",
      overflow: "hidden",
    }}>
      {/* History rail */}
      <aside style={{
        borderRight: `1px solid ${DRAC.line}`,
        padding: "22px 0 22px 0",
        display: "flex", flexDirection: "column",
        background: DRAC.bgAlt,
      }}>
        <div style={{ padding: "0 18px 18px", display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ width: 9, height: 9, borderRadius: 2, background: DRAC.pink }} />
          <div style={{ fontSize: 13, fontWeight: 600, letterSpacing: -0.1, color: DRAC.fg }}>Logicbroker Agent</div>
        </div>
        <button onClick={() => { setQ(""); setTimeout(() => inputRef.current?.focus(), 0); }} style={{
          margin: "0 14px 14px", padding: "8px 10px",
          border: `1px solid ${DRAC.line}`, borderRadius: 4,
          background: "transparent", cursor: "pointer",
          fontFamily: "inherit", fontSize: 12, color: DRAC.fg,
          textAlign: "left",
        }}>+ New query</button>
        <div style={{ fontSize: 10.5, letterSpacing: 0.6, textTransform: "uppercase", color: DRAC.comment, padding: "6px 18px 4px" }}>
          History
        </div>
        <div style={{ flex: 1, overflowY: "auto" }}>
          {history.length === 0 && (
            <div style={{ padding: "10px 18px", fontSize: 12, color: DRAC.comment }}>
              Nothing yet.
            </div>
          )}
          {history.map((e) => (
            <DracHistoryItem key={e.id} entry={e} active={active?.id === e.id} onClick={() => select(e.id)} />
          ))}
        </div>
      </aside>

      {/* Q & A column */}
      <main style={{ padding: "44px 60px 28px", display: "flex", flexDirection: "column", overflow: "hidden" }}>
        {!active && (
          <div style={{ marginBottom: 18 }}>
            <div style={{ fontSize: 11, letterSpacing: 1.2, textTransform: "uppercase", color: DRAC.comment, marginBottom: 12 }}>
              <span style={{ color: DRAC.pink }}>●</span> Knowledge base · 14,832 docs
            </div>
            <h1 style={{
              fontFamily: "'Inter', sans-serif",
              fontSize: 38, lineHeight: 1.05, fontWeight: 500,
              letterSpacing: -0.8, margin: 0,
              textWrap: "balance", color: DRAC.fg,
            }}>
              Ask the <span style={{ color: DRAC.purple }}>Logicbroker</span><br/>knowledge base.
            </h1>
            <p style={{ marginTop: 14, fontSize: 14.5, color: DRAC.comment, maxWidth: 480, lineHeight: 1.55 }}>
              The agent searches docs, reads sources, and composes a cited answer. Watch its loop on the right.
            </p>
          </div>
        )}

        {active && (
          <div style={{ flex: 1, overflowY: "auto", paddingRight: 8, marginBottom: 18 }}>
            <div style={{ fontSize: 11, letterSpacing: 1.2, textTransform: "uppercase", color: DRAC.comment, marginBottom: 8 }}>
              Query
            </div>
            <div style={{ fontSize: 22, fontWeight: 500, letterSpacing: -0.3, lineHeight: 1.25, marginBottom: 28, textWrap: "balance", color: DRAC.fg }}>
              {active.query}
            </div>
            {active.answer ? (
              <DracAnswer answer={active.answer} />
            ) : (
              <div style={{ display: "flex", alignItems: "center", gap: 10, color: DRAC.comment, fontSize: 13 }}>
                <span style={{
                  width: 10, height: 10, borderRadius: "50%",
                  background: DRAC.green,
                  animation: "pulse 1.4s ease-in-out infinite",
                }} />
                Thinking — {active.trace.length} step{active.trace.length === 1 ? "" : "s"} so far
              </div>
            )}
          </div>
        )}

        {/* Input */}
        <div>
          <div style={{
            display: "flex", alignItems: "center",
            border: `1px solid ${DRAC.line}`,
            borderRadius: 6,
            background: DRAC.bgAlt,
            padding: "0 4px 0 14px",
            transition: "border 0.15s",
          }}>
            <span style={{ color: DRAC.green, fontFamily: "'JetBrains Mono', monospace", fontSize: 13, marginRight: 10 }}>›</span>
            <input
              ref={inputRef}
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") submit(); }}
              placeholder="Ask anything in the knowledge base…"
              style={{
                flex: 1, border: "none", outline: "none",
                fontFamily: "inherit", fontSize: 14,
                padding: "12px 0", background: "transparent", color: DRAC.fg,
              }}
            />
            <button onClick={() => submit()} disabled={!q.trim()} style={{
              padding: "7px 14px",
              background: q.trim() ? DRAC.purple : DRAC.line,
              color: q.trim() ? DRAC.bg : DRAC.comment,
              border: "none", borderRadius: 4,
              fontFamily: "inherit", fontSize: 12.5, fontWeight: 600,
              cursor: q.trim() ? "pointer" : "default",
              margin: "4px",
            }}>
              Run ↵
            </button>
          </div>
          <div style={{ display: "flex", gap: 6, marginTop: 12, flexWrap: "wrap" }}>
            {SAMPLE_QUERIES.map((s) => (
              <DracChip key={s} onClick={() => submit(s)}>{s}</DracChip>
            ))}
          </div>
        </div>
      </main>

      {/* Live terminal */}
      <section style={{
        background: DRAC.bgAlt,
        borderLeft: `1px solid ${DRAC.line}`,
        padding: "22px 22px 22px",
        display: "flex", flexDirection: "column",
      }}>
        <div style={{
          fontSize: 10.5, letterSpacing: 0.6, textTransform: "uppercase",
          color: DRAC.comment, marginBottom: 12,
          display: "flex", justifyContent: "space-between", alignItems: "center",
        }}>
          <span>Agent loop</span>
          <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span style={{
              width: 7, height: 7, borderRadius: "50%",
              background: active && !active.done ? DRAC.green : DRAC.line,
              animation: active && !active.done ? "pulse 1.4s ease-in-out infinite" : "none",
            }} />
            <span style={{ color: active && !active.done ? DRAC.green : DRAC.comment }}>
              {active && !active.done ? "running" : "idle"}
            </span>
          </span>
        </div>
        <div style={{ flex: 1, minHeight: 0 }}>
          <Terminal
            trace={active?.trace || []}
            palette={PALETTE_A}
            height="100%"
            blink={active && !active.done}
            label="logic-agent"
          />
        </div>
      </section>
    </div>
  );
}

// ───────────────────────────── Variation B ─────────────────────────────
// Stacked: top bar with history dropdown · big input · inline terminal · answer below
function VariationB() {
  const { history, active, ask, select } = useAgent();
  const [q, setQ] = React.useState("");
  const [showHist, setShowHist] = React.useState(false);

  const submit = (text) => {
    const v = (text ?? q).trim();
    if (!v) return;
    ask(v);
    setQ("");
  };

  return (
    <div style={{
      width: 1200, height: 760,
      background: "#FFFFFF",
      color: "#14140F",
      fontFamily: "'Inter', system-ui, sans-serif",
      display: "flex", flexDirection: "column",
      overflow: "hidden",
    }}>
      {/* Top bar */}
      <header style={{
        height: 52,
        borderBottom: "1px solid rgba(20,20,15,0.08)",
        padding: "0 32px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        flexShrink: 0,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 9, height: 9, borderRadius: 2, background: "#14140F" }} />
          <div style={{ fontSize: 13, fontWeight: 600, letterSpacing: -0.1 }}>Logicbroker Agent</div>
          <div style={{ fontSize: 11.5, color: "rgba(20,20,15,0.45)", marginLeft: 4 }}>
            · knowledge base
          </div>
        </div>
        <div style={{ position: "relative" }}>
          <button onClick={() => setShowHist((v) => !v)} style={{
            background: "transparent",
            border: "1px solid rgba(20,20,15,0.15)",
            borderRadius: 4,
            padding: "5px 12px",
            fontFamily: "inherit", fontSize: 12,
            cursor: "pointer", color: "#14140F",
          }}>
            History · {history.length} ▾
          </button>
          {showHist && (
            <div style={{
              position: "absolute", top: 36, right: 0,
              width: 320, maxHeight: 360, overflowY: "auto",
              background: "#FFFFFF",
              border: "1px solid rgba(20,20,15,0.12)",
              borderRadius: 6,
              boxShadow: "0 12px 30px rgba(20,20,15,0.08)",
              zIndex: 5,
            }}>
              {history.length === 0 ? (
                <div style={{ padding: 16, fontSize: 12.5, color: "rgba(20,20,15,0.45)" }}>
                  No queries yet.
                </div>
              ) : history.map((e) => (
                <HistoryItem key={e.id} entry={e} active={active?.id === e.id}
                  onClick={() => { select(e.id); setShowHist(false); }} />
              ))}
            </div>
          )}
        </div>
      </header>

      <div style={{ flex: 1, overflowY: "auto", padding: "36px 64px 40px" }}>
        {!active && (
          <div style={{ maxWidth: 720, margin: "16px auto 0" }}>
            <h1 style={{
              fontSize: 44, lineHeight: 1.05, fontWeight: 500, letterSpacing: -1,
              margin: 0, textWrap: "balance",
            }}>
              What can I help you find in the docs?
            </h1>
            <p style={{ marginTop: 14, fontSize: 15, color: "rgba(20,20,15,0.6)", lineHeight: 1.55, maxWidth: 540 }}>
              Type a question. The agent searches Logicbroker's knowledge base, reads relevant docs, and answers with citations. Its loop runs in the open.
            </p>
          </div>
        )}

        {/* Big input */}
        <div style={{ maxWidth: 720, margin: !active ? "32px auto 0" : "0 auto 0" }}>
          <div style={{
            border: "1.5px solid rgba(20,20,15,0.18)",
            borderRadius: 8,
            background: "#FFFFFF",
            display: "flex", alignItems: "stretch",
            transition: "border 0.15s",
          }}>
            <div style={{
              padding: "14px 4px 14px 18px",
              color: "rgba(20,20,15,0.4)",
              fontFamily: "'JetBrains Mono', monospace", fontSize: 14,
              alignSelf: "flex-start", lineHeight: 1.3,
            }}>›</div>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") submit(); }}
              placeholder="Ask anything in the knowledge base…"
              style={{
                flex: 1, border: "none", outline: "none",
                fontFamily: "inherit", fontSize: 16,
                padding: "13px 12px", background: "transparent", color: "#14140F",
              }}
            />
            <button onClick={() => submit()} disabled={!q.trim()} style={{
              padding: "0 22px",
              background: q.trim() ? "#14140F" : "rgba(20,20,15,0.08)",
              color: q.trim() ? "#FAFAF7" : "rgba(20,20,15,0.4)",
              border: "none",
              fontFamily: "inherit", fontSize: 13, fontWeight: 500,
              cursor: q.trim() ? "pointer" : "default",
              borderRadius: "0 6px 6px 0",
              margin: "1.5px",
            }}>Run ↵</button>
          </div>
          <div style={{ display: "flex", gap: 6, marginTop: 14, flexWrap: "wrap" }}>
            {SAMPLE_QUERIES.map((s) => (
              <Chip key={s} onClick={() => submit(s)}>{s}</Chip>
            ))}
          </div>
        </div>

        {active && (
          <div style={{ maxWidth: 720, margin: "36px auto 0" }}>
            {/* Loop trace */}
            <div style={{
              marginBottom: 22,
            }}>
              <div style={{
                fontSize: 10.5, letterSpacing: 0.6, textTransform: "uppercase",
                color: "rgba(20,20,15,0.45)", marginBottom: 8,
                display: "flex", alignItems: "center", gap: 8,
              }}>
                <span>Agent loop</span>
                <span style={{
                  width: 6, height: 6, borderRadius: "50%",
                  background: active && !active.done ? "#3B7A2E" : "rgba(20,20,15,0.25)",
                  animation: active && !active.done ? "pulse 1.4s ease-in-out infinite" : "none",
                }} />
                <span style={{ color: active && !active.done ? "#3B7A2E" : "rgba(20,20,15,0.45)" }}>
                  {active && !active.done ? "running" : "complete"}
                </span>
              </div>
              <Terminal
                trace={active.trace}
                palette={PALETTE_B}
                height={Math.min(280, 64 + active.trace.length * 22)}
                blink={!active.done}
                label="logic-agent · stdout"
              />
            </div>

            {/* Answer */}
            {active.answer ? (
              <div style={{
                background: "#FAFAF7",
                border: "1px solid rgba(20,20,15,0.08)",
                borderRadius: 8,
                padding: "26px 30px",
              }}>
                <div style={{ fontSize: 10.5, letterSpacing: 0.6, textTransform: "uppercase", color: "rgba(20,20,15,0.45)", marginBottom: 10 }}>
                  Answer · {active.query}
                </div>
                <AnswerBlock answer={active.answer} />
              </div>
            ) : (
              <div style={{
                fontSize: 13, color: "rgba(20,20,15,0.5)",
                padding: "18px 0",
              }}>
                Composing answer…
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

Object.assign(window, { VariationA, VariationB });
