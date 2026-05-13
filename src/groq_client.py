from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL


class GroqClient:
    """
    Client for interacting with Groq API
    Using Mixtral-8x7B model (fast and powerful, completely free)
    """

    def __init__(self):
        """Initialize Groq client with API key"""
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found in .env file!\n"
                "Please add: GROQ_API_KEY=your_key_here"
            )

        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

        print("✓ Groq client initialized")
        print(f"  Model: {self.model}")

    def generate_response(self, messages: list, temperature: float = 0.3) -> str:
        """
        Generate response from Groq LLM

        Args:
            messages: List of message dicts with 'role' and 'content'
                     Example: [{"role": "user", "content": "What is OS?"}]
            temperature: 0-1, higher = more creative, lower = more focused
                        0.3 is good for factual answers

        Returns:
            The LLM's response text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=1000,  # Limit response length
            )

            # Extract the answer from response
            return response.choices[0].message.content

        except Exception as e:
            return f"Error calling Groq API: {str(e)}"

    def create_prompt(self, question: str, context: list) -> str:
        """
        Create a well-structured prompt for the LLM

        Args:
            question: User's question
            context: List of relevant text chunks from vector DB

        Returns:
            Formatted prompt string
        """
        # Join context chunks
        context_text = "\n\n".join(context)

        prompt = f"""You are an expert on Osteosarcoma (bone cancer). 
Answer the following question ONLY based on the provided context from research papers.

If the answer is not in the context, say: "I don't have enough information to answer this question based on the provided papers."

Do NOT make up information or use knowledge outside the provided context.

CONTEXT FROM RESEARCH PAPERS:
{context_text}

QUESTION: {question}

ANSWER:"""

        return prompt
