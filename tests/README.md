# Tests

Run the current test suite from the project root:

```bash
python -m unittest discover -s tests
```

These tests pin the current keyword retrieval behavior before the project moves to embeddings and semantic search.

Run the retrieval evaluation report:

```bash
python scripts/evaluate_retrieval.py
```
