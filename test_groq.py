import sys

sys.path.append("src")

from groq_client import GroqClient

if __name__ == "__main__":
    print("Testing Groq API connection...\n")

    try:
        # Initialize Groq client
        groq = GroqClient()
        print()

        # Create a simple test message
        messages = [
            {"role": "user", "content": "What is osteosarcoma in one sentence?"}
        ]

        print("Sending test query to Groq...")
        response = groq.generate_response(messages)

        print()
        print("Response from Groq:")
        print("-" * 60)
        print(response)
        print("-" * 60)

        print("\n✓ Groq API is working!")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
