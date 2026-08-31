interface ExampleQuestionsProps {
  onSelect: (question: string) => void;
  disabled: boolean;
}

const EXAMPLES = [
  "Who was Arjuna?",
  "Who was Draupadi?",
  "who is bhima?",
  "who is nakula?",
  "Who is duryodana?",
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
