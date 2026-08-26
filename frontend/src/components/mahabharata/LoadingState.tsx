export default function LoadingState() {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <span className="ink-spinner" aria-hidden="true" />
      <span>Consulting the epic…</span>
    </div>
  );
}
