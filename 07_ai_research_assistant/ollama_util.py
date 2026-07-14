import ollama

# We will use 'llama3.2', but you can change this to any model you have pulled
MODEL_NAME = "llama3.2"

def ask_local_model(question):
    """Sends a prompt to the locally running Ollama instance."""
    if not question.strip():
        return "Please enter a valid prompt."
    
    try:
        # We use ollama.generate for simple, direct one-off prompts
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=question
        )
        # Extract and return the generated text
        return response['response']
        
    except Exception as e:
        return (
            f"Ollama Error: {str(e)}\n\n"
            "Make sure Ollama is actively running in the background of your computer, "
            f"and you have downloaded the model using 'ollama pull {MODEL_NAME}' in your terminal."
        )