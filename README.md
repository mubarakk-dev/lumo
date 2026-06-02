# Lumo 💡

**Lumo** is an AI-powered Docker assistant designed to help users learn Docker concepts, generate commands and configurations, and troubleshoot common Docker issues through a structured knowledge retrieval system.

## Project Overview

Lumo began as a simple chatbot but evolved into a retrieval-based AI assistant built around a modular Docker knowledge base. Instead of relying on hardcoded responses, Lumo retrieves relevant knowledge chunks from a structured collection of Markdown files and ranks them based on the user's query.

The project was built to explore the foundations of AI retrieval systems, knowledge architecture, and Retrieval-Augmented Generation (RAG).

---

## Features

### Learn Docker Concepts

Examples:

* What is Docker?
* What are Docker volumes?
* What is the difference between images and containers?
* What are multi-stage builds?

### Generate Docker Solutions

Examples:

* Build a Docker image
* Run a container
* Create a Docker Compose setup
* Generate a FastAPI Dockerfile

### Troubleshoot Docker Issues

Examples:

* Docker daemon not running
* Port already in use
* Container exits immediately
* Docker image build failures
* Network connectivity issues

### Docker Cheat Sheets

Examples:

* Docker commands
* Docker cleanup commands
* Dockerfile instructions

---

## Architecture

```text
User Query
     ↓
Topic Detection
     ↓
Knowledge Retrieval
     ↓
Relevance Ranking
     ↓
Top-K Filtering
     ↓
Response Generation
```

---

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

---

## Tech Stack

### Backend

* FastAPI

### Frontend

* Streamlit

### Language

* Python

### Knowledge Storage

* Markdown-based knowledge chunks

### Retrieval

* Custom keyword-based retrieval engine
* Intent-aware scoring
* Top-K retrieval
* Relevance filtering

---

## Key Concepts Explored

* Knowledge Chunking
* Information Retrieval
* Relevance Ranking
* Precision vs Recall
* Top-K Retrieval
* Intent Detection
* AI System Design
* Foundations of Retrieval-Augmented Generation (RAG)

---

## Current Status

### Completed

* FastAPI backend
* Streamlit frontend
* Docker knowledge base
* Topic detection
* Retrieval engine
* Ranking system
* Top-K retrieval
* Troubleshooting knowledge modules

### In Progress

* Retrieval quality improvements
* Knowledge base expansion

### Planned

* Embedding-based retrieval
* Semantic search
* Conversation memory
* Source attribution
* Additional domains (Git, FastAPI, Kubernetes, CI/CD)

---

## Example Questions

```text
What is Docker?

How do I build a Docker image?

Docker daemon is not running.

How do Docker volumes work?

Why can't my containers communicate with each other?

Give me a FastAPI Dockerfile template.
```

---

## Vision

Lumo aims to become a practical AI engineering assistant capable of helping developers learn, build, deploy, and troubleshoot modern engineering tools.

The first phase focuses exclusively on Docker, with future support planned for Git, FastAPI, Kubernetes, CI/CD, cloud platforms, and AI engineering workflows.
