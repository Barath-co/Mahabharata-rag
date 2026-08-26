import BackendStatus from "./BackendStatus";
import type { BackendState } from "../../types";

interface HeaderProps {
  backendState: BackendState;
}

export default function Header({ backendState }: HeaderProps) {
  return (
    <header className="mb-header">
      <div className="mb-header-row">
        <div className="mb-header-titles">
          <svg
            className="mb-emblem"
            width="34"
            height="34"
            viewBox="0 0 100 100"
            aria-hidden="true"
          >
            <circle cx="50" cy="50" r="46" fill="none" stroke="#d4b76a" strokeWidth="2" opacity="0.5" />
            <circle cx="50" cy="50" r="34" fill="none" stroke="#d4b76a" strokeWidth="2" />
            {Array.from({ length: 16 }).map((_, i) => {
              const angle = (i / 16) * Math.PI * 2;
              const x1 = 50 + Math.cos(angle) * 34;
              const y1 = 50 + Math.sin(angle) * 34;
              const x2 = 50 + Math.cos(angle) * 44;
              const y2 = 50 + Math.sin(angle) * 44;
              return (
                <line
                  key={i}
                  x1={x1}
                  y1={y1}
                  x2={x2}
                  y2={y2}
                  stroke="#d4b76a"
                  strokeWidth="2"
                  opacity={i % 2 === 0 ? 0.9 : 0.4}
                />
              );
            })}
            <circle cx="50" cy="50" r="8" fill="#d4b76a" />
          </svg>
          <div>
            <h1 className="mb-title">Mahabharata RAG</h1>
            <p className="mb-subtitle">Ask the epic — answers drawn from the text itself</p>
          </div>
        </div>
        <BackendStatus state={backendState} />
      </div>
    </header>
  );
}
