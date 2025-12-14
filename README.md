The solution is implemented as an Agentic RAG system using a LangGraph-based architecture, where the overall workflow is decomposed into specialized agents for intake processing, knowledge retrieval, diet planning, and safety validation.

A Retrieval-Augmented Generation (RAG) approach is used by storing domain-specific nutrition documents in ChromaDB, where text chunks are converted into vector embeddings using sentence-transformers (all-MiniLM-L6-v2). Relevant nutrition context is retrieved via similarity search and provided to the planning agent.

The diet plan is generated using a Groq-hosted LLaMA 3.1 large language model, while a dedicated safety agent enforces calorie limits, allergy constraints, and health risk checks. This design ensures the system produces personalized, grounded, and safe dietary recommendations.
