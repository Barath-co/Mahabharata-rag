import { useCallback, useEffect, useRef, useState } from "react";
import Header from "./components/mahabharata/Header";
import QuestionInput from "./components/mahabharata/QuestionInput";
import ExampleQuestions from "./components/mahabharata/ExampleQuestions";
import ConversationHistory from "./components/mahabharata/ConversationHistory";
import EmptyState from "./components/mahabharata/EmptyState";
import { askQuestion, checkHealth } from "./lib/api";
import { clearConversation, loadConversation, saveConversation } from "./lib/storage";
import type { BackendState, ConversationEntry } from "./types";

const HEALTH_POLL_MS = 15000;

function makeId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export default function App() {
  const [entries, setEntries] = useState<ConversationEntry[]>(() => loadConversation());
  const [backendState, setBackendState] = useState<BackendState>("checking");
  const inFlight = useRef(false);

  // Persist conversation to localStorage on every change.
  useEffect(() => {
    saveConversation(entries);
  }, [entries]);

  // Poll /health for the online/offline indicator.
  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();

    async function poll() {
      const ok = await checkHealth(controller.signal);
      if (!cancelled) setBackendState(ok ? "online" : "offline");
    }

    poll();
    const interval = setInterval(poll, HEALTH_POLL_MS);
    return () => {
      cancelled = true;
      controller.abort();
      clearInterval(interval);
    };
  }, []);

  const runQuestion = useCallback(async (id: string, question: string) => {
    inFlight.current = true;
    try {
      const result = await askQuestion(question);
      setEntries((prev) =>
        prev.map((e) =>
          e.id === id
            ? { ...e, status: "done", answer: result.answer, sources: result.sources, error: undefined }
            : e
        )
      );
      setBackendState("online");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error.";
      setEntries((prev) =>
        prev.map((e) => (e.id === id ? { ...e, status: "error", error: message } : e))
      );
    } finally {
      inFlight.current = false;
    }
  }, []);

  const handleAsk = useCallback(
    (question: string) => {
      const id = makeId();
      const entry: ConversationEntry = {
        id,
        question,
        status: "loading",
        timestamp: Date.now(),
      };
      setEntries((prev) => [...prev, entry]);
      runQuestion(id, question);
    },
    [runQuestion]
  );

  const handleRetry = useCallback(
    (id: string) => {
      const entry = entries.find((e) => e.id === id);
      if (!entry) return;
      setEntries((prev) =>
        prev.map((e) => (e.id === id ? { ...e, status: "loading", error: undefined } : e))
      );
      runQuestion(id, entry.question);
    },
    [entries, runQuestion]
  );

  const handleClear = useCallback(() => {
    setEntries([]);
    clearConversation();
  }, []);

  const asking = entries.some((e) => e.status === "loading");

  return (
    <div className="app-shell">
      <div className="app-scroll">
        <Header backendState={backendState} />

        <section className="mb-panel">
          <div className="mb-panel-body">
            <div className="mb-toolbar">
              <span className="mb-toolbar-label">Example questions</span>
              {entries.length > 0 && (
                <button type="button" className="mb-clear-btn" onClick={handleClear}>
                  Clear conversation
                </button>
              )}
            </div>
            <ExampleQuestions onSelect={handleAsk} disabled={asking} />

            {entries.length === 0 ? (
              <EmptyState />
            ) : (
              <ConversationHistory entries={entries} onRetry={handleRetry} />
            )}
          </div>

          <div className="mb-panel-footer">
            <QuestionInput onSubmit={handleAsk} disabled={asking} />
          </div>
        </section>
      </div>
    </div>
  );
}
