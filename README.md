---
title: Lumo
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Lumo

Lumo is an AI-powered Docker assistant designed to help users learn Docker concepts, generate commands and configurations, and troubleshoot common Docker issues through a structured RAG system.

Live demo: [Lumo on Hugging Face Spaces](https://huggingface.co/spaces/mubarakk-dev/Lumo)

## Project Overview

Lumo began as a simple chatbot and evolved into a retrieval-based assistant built around a modular Docker knowledge base. Instead of relying on hardcoded responses, Lumo retrieves relevant knowledge chunks from Markdown files, ranks them against the user's query, and can generate grounded answers from the retrieved context.

The project explores the foundations of retrieval systems, semantic search, vector databases, prompt design, and Retrieval-Augmented Generation (RAG).

## Features

### Learn Docker Concepts

Example questions:

- What is Docker?
- What are Docker volumes?
- What is the difference between images and containers?
- What are multi-stage builds?

### Generate Docker Solutions

Example requests:

- Build a Docker image
- Run a container
- Create a Docker Compose setup
- Generate a FastAPI Dockerfile

### Troubleshoot Docker Issues

Example problems:

- Docker daemon not running
- Port already in use
- Container exits immediately
- Docker image build failures
- Network connectivity issues

### Docker Cheat Sheets

Example requests:

- Docker commands
- Docker cleanup commands
- Dockerfile instructions

## Architecture

```text
User Query
  -> Topic Detection
  -> Intent Detection
  -> Knowledge Retrieval
  -> Relevance Ranking
  -> Top-K Filtering
  -> Prompt Assembly
  -> Answer Generation
```

## Knowledge Base Structure

```text
knowledge/
`-- docker/
    |-- learn/
    |-- generate/
    |-- troubleshoot/
    `-- cheatsheets/
```

Each Docker concept is stored as a separate Markdown file to improve maintainability, retrieval quality, and scalability.

## Tech Stack

- Backend: FastAPI
- Frontend: Streamlit
- Language: Python
- Knowledge storage: Markdown
- Retrieval: keyword search, local semantic search, and ChromaDB vector search
- Embeddings: deterministic local embeddings or SentenceTransformers
- Answer generation: extractive grounded answers with optional local Ollama generation

## Running The App

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

Optional local LLM configuration:

```bash
cp .env.example .env
```

The default Ollama settings are:

```bash
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:0.5b
OLLAMA_TIMEOUT_SECONDS=60
OLLAMA_NUM_CTX=1024
OLLAMA_NUM_PREDICT=180
```

To use local LLM generation, install Ollama and pull the configured model:

```bash
ollama pull qwen2.5:0.5b
```

Start the Streamlit frontend:

```bash
streamlit run frontend/streamlit_app.py
```

By default, Streamlit calls the chat service directly. This makes the demo easier to run on free Streamlit-style hosting because it does not require a separate FastAPI process.

Optional API mode for local development:

```bash
set LUMO_CHAT_BACKEND=api
```

Start the API in one terminal:

```bash
uvicorn app.main:app --reload
```

Then start Streamlit in another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

## Running Tests

```bash
python -m unittest discover -s tests
```

The tests cover retrieval behavior, semantic search, ChromaDB retrieval, prompt construction, answer generation fallback behavior, and API request handling.

## Deploying The Public Demo

The public demo is designed to run as a Streamlit app without a separate FastAPI server. It uses deployment-safe defaults:

```text
retrieval_mode = chroma
embedding_provider = local_hashing
response_mode = answer
generation_provider = extractive
```

To deploy on Hugging Face Spaces:

1. Create a new Space.
2. Choose `Docker` as the SDK.
3. Connect this repository or push the repository files to the Space.
4. Keep `sdk: docker` and `app_port: 7860` in the README metadata.
5. Wait for Hugging Face Spaces to build the Dockerfile and start the app.

The Docker container runs:

```bash
streamlit run frontend/streamlit_app.py --server.port=7860 --server.address=0.0.0.0
```

The deployed app uses extractive grounded answers by default. Local Ollama generation remains available for local demos through Advanced settings, but Ollama must be running on the machine serving the app.

## Retrieval Evaluation

Run the retrieval baseline:

```bash
python scripts/evaluate_retrieval.py
```

Compare retrieval modes:

```bash
python scripts/evaluate_retrieval.py --retriever keyword
python scripts/evaluate_retrieval.py --retriever semantic
python scripts/evaluate_retrieval.py --compare
```

The evaluation cases live in `eval/retrieval_cases.json`. Each case defines a query, expected intent, preferred category, and expected source file. This gives the project a measurable baseline before and after adding embeddings, vector search, and hybrid retrieval.

## RAG Answer Evaluation

Run the answer-quality evaluation:

```bash
python scripts/evaluate_rag.py
```

Run one case by id:

```bash
python scripts/evaluate_rag.py --case-id daemon_troubleshooting_answer
```

The RAG evaluation cases live in `eval/rag_cases.json`. Each case checks the full answer path: expected source retrieval, required answer terms, source citations, and whether the answer avoids unsupported fallback language when the knowledge base contains enough context.

## Semantic Retrieval

Build the local vector index:

```bash
python scripts/build_vector_index.py
```

Build a Chroma index with SentenceTransformers:

```bash
python scripts/build_vector_index.py --embedding-provider sentence_transformers
```

Evaluate the Chroma retriever with SentenceTransformers:

```bash
python scripts/evaluate_retrieval.py --retriever chroma --embedding-provider sentence_transformers
python scripts/evaluate_retrieval.py --compare --embedding-provider sentence_transformers
```

The generated local index is stored under `.lumo_index/` and is ignored by Git. ChromaDB stores its generated database under `.chroma/`, which is also ignored by Git.

The app supports `retrieval_mode="keyword"`, `retrieval_mode="semantic"`, and `retrieval_mode="chroma"`. Chroma retrieval can use `embedding_provider="local_hashing"` or `embedding_provider="sentence_transformers"`.

## Grounded Answer Generation

The chat API supports two response modes:

- `answer`: returns a grounded answer assembled from retrieved context and sources.
- `retrieval`: returns the raw retrieved Markdown context for debugging.

Example request:

```json
{
  "message": "Docker daemon is not running",
  "retrieval_mode": "chroma",
  "embedding_provider": "sentence_transformers",
  "response_mode": "answer",
  "generation_provider": "extractive"
}
```

The extractive answer generator only uses retrieved knowledge chunks, which keeps the behavior testable and available without external credentials.

When vector search returns a small section chunk, the chat service expands that match from the original source document before answer generation. This keeps generation grounded in the retrieved source while giving the prompt or extractive answer builder enough context to produce useful answers.

## Local LLM Answer Generation

The API supports a configurable generation provider:

- `generation_provider="extractive"` uses the local source-grounded answer builder.
- `generation_provider="ollama"` sends the retrieved context through a guarded RAG prompt and asks the configured local Ollama model to answer with source citations.

If Ollama is not running or the configured model is unavailable, the app falls back to the extractive answer path. This keeps the app usable in local development, CI, and demos while still supporting free local LLM generation.

The default local model is `qwen2.5:0.5b` because it is small enough for reliable laptop demos while still showing the full RAG flow.

Example request:

```json
{
  "message": "Docker daemon is not running",
  "retrieval_mode": "chroma",
  "embedding_provider": "sentence_transformers",
  "response_mode": "answer",
  "generation_provider": "ollama"
}
```

This gives the project a practical local-first RAG path: SentenceTransformers creates embeddings, ChromaDB retrieves relevant chunks, the prompt builder packages context with source IDs, and Ollama generates a cited answer from that retrieved context.

## Current Status

Completed:

- FastAPI backend
- Streamlit frontend
- Docker knowledge base
- Topic detection
- Intent detection
- Keyword retrieval engine
- Ranking system
- Top-K retrieval
- Retrieval baseline tests
- Retrieval evaluation script
- Local semantic retrieval mode
- ChromaDB retrieval mode
- SentenceTransformers embedding provider
- Local vector index build script
- Grounded answer response mode
- Prompt builder for source-grounded RAG answers
- Optional local Ollama answer-generation provider
- Deterministic RAG answer evaluation script

In progress:

- Local LLM answer-quality tuning

Planned:

- Conversation memory
- Additional domains such as Git, FastAPI, Kubernetes, CI/CD, and cloud platforms

## Example Questions

```text
What is Docker?
How do I build a Docker image?
Docker daemon is not running.
How do Docker volumes work?
Why can't my containers communicate with each other?
Give me a FastAPI Dockerfile template.
```

## Vision

Lumo aims to become a practical AI engineering assistant that helps developers learn, build, deploy, and troubleshoot modern engineering tools.

The first phase focuses on Docker. Future phases can expand into Git, FastAPI, Kubernetes, CI/CD, cloud platforms, and AI engineering workflows.
