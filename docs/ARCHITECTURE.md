# CFAI Architecture Specification: Hybrid RAG & Financial Agent

## 1. Architectural Philosophy
Financial domain queries cannot tolerate fuzzy approximations. CFAI implements a deterministic-first hybrid architecture combining symbolic verification with semantic retrieval.

## 2. Ingestion & Indexing Pipeline
1. **Chunking**: Chunked via semantic boundary splits rather than arbitrary token character counts.
2. **Dense Embeddings**: High-density float32 vectors mapped to HNSW spatial indexes.
3. **Sparse Inverted Index**: Exact keyword tokens (tickers, revenue numbers, margins) indexed via BM25.
