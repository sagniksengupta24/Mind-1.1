export function ErrorBanner({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="error-banner mb-4">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 8v4M12 16h.01" />
      </svg>
      <div className="content">
        <b>Connection Error</b>
        <p>{message}</p>
        {onRetry && (
          <button onClick={onRetry}>Try Again</button>
        )}
      </div>
    </div>
  );
}
