# Mahabharata RAG

A full-stack Retrieval-Augmented Generation (RAG) project for exploring and querying knowledge from the Mahabharata.

## Project Status

🚧 Currently in development.

### Day 1 — Project Setup
- Python virtual environment configured
- Project structure created
- Environment variables configured with `.env`
- `.gitignore` configured to protect secrets and the virtual environment
- Git repository initialized
- GitHub repository connected

## Planned Architecture

Data Collection → Cleaning → Chunking → Embeddings → Vector Database → RAG → FastAPI → React/TypeScript

## Tech Stack

- Python
- FastAPI
- React
- TypeScript
- PostgreSQL / pgvector
- Embeddings
- LLM
- RAG

## Project Structure

```text
Mahabharata-rag/
├── src/
│   ├── scrape.py
│   ├── clean.py
│   ├── chunk.py
│   └── embed.py
├── entities.csv
├── requirements.txt
├── .gitignore
└── README.md