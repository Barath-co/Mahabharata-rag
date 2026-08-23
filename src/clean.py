import re

input_path = "data/processed/mahabharata.txt"
output_path = "data/processed/mahabharata_clean.txt"

with open(input_path, "r", encoding="utf-8") as file:
    text = file.read()

# Remove unnecessary spaces at the beginning/end of lines
text = re.sub(r"[ \t]+", " ", text)

# Join lines that are broken in the middle of a sentence
text = re.sub(r"(?<![.!?])\n(?!\n)", " ", text)

# Reduce multiple blank lines to a single paragraph break
text = re.sub(r"\n{3,}", "\n\n", text)

# Remove spaces before punctuation
text = re.sub(r"\s+([,.!?;:])", r"\1", text)

with open(output_path, "w", encoding="utf-8") as file:
    file.write(text)

print("Cleaning completed!")