def test_add_and_search():
    from app.vector_db import add_doc, search_relevant_chunks
    add_doc("Test document about Mistral AI.")
    results = search_relevant_chunks("Mistral AI")
    assert results, "Should return at least one result."
