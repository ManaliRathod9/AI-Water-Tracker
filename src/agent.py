import ollama

class WaterIntakeAgent:
    def __init__(self):
        self.history = []

    def analyze_intake(self, intake_ml):
        prompt = f"""
You are a hydration assistant.
The user has consumed {intake_ml} ml of water today.
Provide hydration status and suggest if they need to drink more water.
Keep it short and practical (3-5 lines).
"""

        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"]


if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1500
    feedback = agent.analyze_intake(intake)
    print(f"Hydration Analysis:\n{feedback}")