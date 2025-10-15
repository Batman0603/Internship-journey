import random

def generate_mcq(context: str, num_questions: int = 5):
    """
    Simulates generating MCQs from context.
    In a real-world scenario, you would replace this with a call to an LLM
    (e.g., via HuggingFace, OpenAI, or Together AI) to generate meaningful questions.
    """
    questions = []
    # Simple text splitting to get "concepts"
    words = [word for word in context.replace(",", "").replace(".", "").split() if len(word) > 4]
    
    if len(words) < 4: # Not enough context to generate questions
        return [{"question": "Not enough context provided.", "options": [], "answer": ""}]

    for i in range(num_questions):
        # Select a random "concept" from the text
        concept = random.choice(words)
        correct_answer = f"Related to {concept}"
        options = [f"Not related to {concept}", "Irrelevant option", "Another choice", correct_answer]
        random.shuffle(options)
        questions.append({
            "question": f"Which of the following is true about '{concept}' based on the context?",
            "options": options,
            "answer": correct_answer
        })
    return questions

def generate_descriptive(context: str, num_questions: int = 3):
    questions = []
    for i in range(num_questions):
        questions.append({
            "question": f"Explain in detail: {context[:70]}?",
            "answer_format": "long_text"
        })
    return questions
