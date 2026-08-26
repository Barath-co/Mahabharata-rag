export default function EmptyState() {
  return (
    <div className="empty-state">
      <svg className="emblem" width="40" height="40" viewBox="0 0 100 100" aria-hidden="true">
        <path
          d="M50 12 L58 40 L88 40 L64 58 L72 88 L50 70 L28 88 L36 58 L12 40 L42 40 Z"
          fill="none"
          stroke="#a9832f"
          strokeWidth="2.5"
        />
      </svg>
      <h2>No question asked yet</h2>
      <p>Ask something about the Mahabharata below, or pick one of the examples to begin.</p>
    </div>
  );
}
