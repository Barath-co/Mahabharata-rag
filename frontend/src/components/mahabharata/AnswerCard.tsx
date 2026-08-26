import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import SourceCard from "./SourceCard";
import type { Source } from "../../types";

interface AnswerCardProps {
  answer: string;
  sources: Source[];
}

export default function AnswerCard({ answer, sources }: AnswerCardProps) {
  return (
    <div className="answer-card">
      <div className="answer-body">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{answer}</ReactMarkdown>
      </div>
      {sources.length > 0 && (
        <div className="sources-block">
          <p className="sources-label">Source passages ({sources.length})</p>
          {sources.map((s, i) => (
            <SourceCard key={`${s.section}-${i}`} source={s} />
          ))}
        </div>
      )}
    </div>
  );
}
