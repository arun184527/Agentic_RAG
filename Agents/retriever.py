from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "../chroma_db"

def retrieve_knowledge(intake_output, k=4):
    """
    intake_output: output from Agent-1
    k: number of relevant chunks to retrieve
    """

    # Build a simple search query from intake data
    query = (
        f"Goal: {intake_output['user_profile']['goal']}, "
        f"Diet: {intake_output['user_profile']['preference']}, "
        f"Calories: {intake_output['calculations']['target_calories']}, "
        f"Allergies: {', '.join(intake_output['user_profile']['allergies'])}"
    )

    # Load embeddings (same as ingestion)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load Chroma DB
    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    # Perform similarity search
    results = db.similarity_search(query, k=k)

    return results


# Test the retriever independently
if __name__ == "__main__":
    sample_intake = {
        "user_profile": {
            "goal": "weight_loss",
            "preference": "vegetarian",
            "allergies": ["peanut"]
        },
        "calculations": {
            "target_calories": 1800
        }
    }

    docs = retrieve_knowledge(sample_intake)

    print("\n=== Retrieved Knowledge ===\n")
    for i, doc in enumerate(docs, 1):
        print(f"Result {i}:")
        print(doc.page_content)
        print("-" * 40)
