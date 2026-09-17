# AI/ML Technical Interview Defense Guide

### Q1: Why use Hybrid Search (Dense + Sparse) instead of pure Vector Search?
> **Answer**: Vector embeddings excel at semantic concepts ("earnings performance") but struggle with specific identifiers ("SEC Form 10-Q Section 4.2" or stock tickers like "ON"). BM25 provides exact string matching while dense vectors capture semantic intent.

### Q2: How do you prevent context poisoning and Prompt Injection in institutional RAG?
> **Answer**: Document text is isolated from instruction text using delimiter tags. Input prompts are evaluated by a classification model and regex guardrail before vector injection.

### Q3: How do you measure RAG quality systematically?
> **Answer**: Through the RAG Triad framework: Context Relevance (precision of retrieved chunks), Groundedness (zero non-context numbers), and Answer Relevance.
