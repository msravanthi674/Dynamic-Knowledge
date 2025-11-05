def test_chatbot_response():
    from app.chatbot import get_chatbot_response
    resp = get_chatbot_response("What is Mistral AI?")
    assert isinstance(resp, str)
