import { useState } from "react";
import type { Source } from "../../types";

interface SourceCardProps {
  source: Source;
}

export default function SourceCard({ source }: SourceCardProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="source-leaf" data-open={open}>
      <button
        type="button"
        className="source-leaf-trigger"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
      >
        <span className="source-leaf-section">{source.section}</span>
        <span className="source-leaf-caret" aria-hidden="true">▸</span>
      </button>
      {open && <p className="source-leaf-text">{source.text}</p>}
    </div>
  );
}
