# RAG Data Flow & Grounded Inference Pipeline

~~~text
[User Prompt: "Compare Q2 Gross Margins"]
                      │
                      ▼
         [PII & Injection Sanitizer]
                      │
                      ▼
         [Parallel Hybrid Retrieval]
         ├── Dense Cosine Similarity
         └── Sparse BM25 Keyword Match
                      │
                      ▼
      [Reciprocal Rank Fusion: Top-K Extraction]
                      │
                      ▼
         [Context-Augmented Inference]
                      │
                      ▼
         [Deterministic Numeric Cross-Check]
                      │
                      ▼
      [Emit Verified Answer with Citations]
~~~
