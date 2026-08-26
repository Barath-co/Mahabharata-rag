interface ExampleQuestionsProps {
  onSelect: (question: string) => void;
  disabled: boolean;
}

const EXAMPLES = [
  "Who was Arjuna?",
  "Why did Draupadi have five husbands?",
  "What is the significance of the Bhagavad Gita?",
  "How did the Kurukshetra war begin?",
  "Who was Karna and why is he a tragic figure?",
];

export default function ExampleQuestions({ onSelect, disabled }: ExampleQuestionsProps) {
  return (
    <div className="example-questions">
      {EXAMPLES.map((q) => (
        <button
          key={q}
          type="button"
          className="example-chip"
          onClick={() => onSelect(q)}
          disabled={disabled}
        >
          {q}
        </button>
      ))}
    </div>
  );
}
