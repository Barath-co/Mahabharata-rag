from pypdf import PdfReader

pdf_path = "data/raw/Mahabharata.pdf"
output_path = "data/processed/mahabharata.txt"

reader = PdfReader(pdf_path)

print(f"Total pages: {len(reader.pages)}")

with open(output_path, "w", encoding="utf-8") as file:
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            file.write(text)
            file.write("\n\n")

        print(f"Processed page {page_number}/{len(reader.pages)}")

print("Extraction completed!")