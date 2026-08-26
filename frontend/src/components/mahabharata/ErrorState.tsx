interface ErrorStateProps {
  message: string;
  onRetry: () => void;
}

export default function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="error-state" role="alert">
      <div className="error-state-text">
        <strong>Could not get an answer</strong>
        {message}
      </div>
      <button type="button" className="retry-btn" onClick={onRetry}>
        Retry
      </button>
    </div>
  );
}
