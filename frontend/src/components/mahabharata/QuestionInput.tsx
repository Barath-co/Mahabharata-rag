import { useRef, useState, type KeyboardEvent } from "react";

interface QuestionInputProps {
  onSubmit: (question: string) => void;
  disabled: boolean;
}

export default function QuestionInput({ onSubmit, disabled }: QuestionInputProps) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function submit() {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSubmit(trimmed);
    setValue("");
    requestAnimationFrame(() => {
      if (textareaRef.current) textareaRef.current.style.height = "auto";
    });
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
    // Shift+Enter falls through and inserts a newline as normal.
  }

  function handleChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setValue(e.target.value);
    const el = e.target;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
  }

  return (
    <div>
      <div className="question-input-row">
        <div className="question-input-wrap">
          <textarea
            ref={textareaRef}
            className="question-textarea"
            placeholder="Ask about the Mahabharata — its people, events, or teachings…"
            rows={1}
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            aria-label="Your question about the Mahabharata"
          />
        </div>
        <button
          type="button"
          className="ask-btn"
          onClick={submit}
          disabled={disabled || !value.trim()}
        >
          {disabled ? "Asking…" : "Ask"}
        </button>
      </div>
      <p className="input-hint">
        <kbd>Enter</kbd> to ask · <kbd>Shift</kbd>+<kbd>Enter</kbd> for a new line
      </p>
    </div>
  );
}
