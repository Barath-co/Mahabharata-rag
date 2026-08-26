import AnswerCard from "./AnswerCard";
import LoadingState from "./LoadingState";
import ErrorState from "./ErrorState";
import type { ConversationEntry } from "../../types";

interface ConversationHistoryProps {
  entries: ConversationEntry[];
  onRetry: (id: string) => void;
}

export default function ConversationHistory({ entries, onRetry }: ConversationHistoryProps) {
  return (
    <div className="conversation-thread">
      {entries.map((entry) => (
        <div className="thread-entry" data-status={entry.status} key={entry.id}>
          <span className="thread-hole" aria-hidden="true" />
          <p className="question-line">
            Asked {new Date(entry.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
          </p>
          <p className="question-text">{entry.question}</p>

          {entry.status === "loading" && <LoadingState />}

          {entry.status === "error" && (
            <ErrorState message={entry.error ?? "Something went wrong."} onRetry={() => onRetry(entry.id)} />
          )}

          {entry.status === "done" && entry.answer !== undefined && (
            <AnswerCard answer={entry.answer} sources={entry.sources ?? []} />
          )}
        </div>
      ))}
    </div>
  );
}
