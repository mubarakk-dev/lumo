# Lumo

Lumo is an AI-powered Docker assistant designed to help users learn Docker concepts, generate commands and configurations, and troubleshoot common Docker issues through a structured knowledge retrieval system.

## Project Overview

Lumo began as a simple chatbot and evolved into a retrieval-based assistant built around a modular Docker knowledge base. Instead of relying on hardcoded responses, Lumo retrieves relevant knowledge chunks from Markdown files and ranks them based on the user's query.

The project explores the foundations of retrieval systems, knowledge architecture, and Retrieval-Augmented Generation (RAG).

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
  -> Response Assembly
```

## Knowledge Base Structure

```text
knowledge/
└── docker/
    ├── learn/
    ├── generate/
    ├── troubleshoot/
    └── cheatsheets/
```

Each Docker concept is stored as a separate Markdown file to improve maintainability, retrieval quality, and scalability.

## Tech Stack

- Backend: FastAPI
- Frontend: Streamlit
- Language: Python
- Knowledge storage: Markdown
- Retrieval: custom keyword-based retrieval engine with intent-aware scoring

## Running The App

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Start the Streamlit frontend in another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

## Running Tests

```bash
python -m unittest discover -s tests
```

The current tests pin representative retrieval behavior before the project moves to embeddings and semantic search.

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

The evaluation cases live in `eval/retrieval_cases.json`. Each case defines a query, expected intent, preferred category, and expected source file. This gives the project a measurable baseline before adding embeddings, vector search, and hybrid retrieval.

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

The generated index is stored under `.lumo_index/` and is ignored by Git. The current semantic retrieval layer uses local deterministic embeddings and cosine similarity so the vector-search architecture is easy to inspect and test. This creates the retrieval interface needed to later plug in model-backed embeddings and a production vector store such as ChromaDB or pgvector.

The vector index stores metadata such as schema version, topic, embedding provider, embedding dimensions, and chunk count. This makes the generated index easier to inspect and safer to evolve as retrieval changes.

ChromaDB stores its generated database under `.chroma/`, which is also ignored by Git. The app supports `retrieval_mode="chroma"` and lets the caller choose `embedding_provider="local_hashing"` or `embedding_provider="sentence_transformers"`.

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
- Local vector index build script

In progress:

- Model-backed embeddings
- Vector database integration
- Hybrid retrieval

Planned:

- Embedding-based retrieval
- Production vector search
- Source-grounded answer generation
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
