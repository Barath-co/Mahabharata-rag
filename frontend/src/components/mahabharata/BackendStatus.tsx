import type { BackendState } from "../../types";

interface BackendStatusProps {
  state: BackendState;
}

const LABEL: Record<BackendState, string> = {
  checking: "Checking",
  online: "Backend online",
  offline: "Backend offline",
};

export default function BackendStatus({ state }: BackendStatusProps) {
  return (
    <div className="backend-status" data-state={state} role="status">
      <span className="dot" aria-hidden="true" />
      <span>{LABEL[state]}</span>
    </div>
  );
}
