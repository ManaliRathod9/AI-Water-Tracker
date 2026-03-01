import os

class WaterIntakeAgent:

    def analyze_intake(self, intake_ml: int) -> str:
        """
        If running locally with Ollama installed, you can extend this.
        On Streamlit Cloud, we use safe fallback logic.
        """

        try:
            # Try importing ollama (only works locally)
            import ollama

            response = ollama.chat(
                model="llama3",
                messages=[
                    {
                        "role": "user",
                        "content": f"I drank {intake_ml} ml of water. Give short hydration advice."
                    }
                ]
            )

            return response["message"]["content"]

        except Exception:
            # ✅ Safe fallback (Cloud Compatible)
            if intake_ml < 200:
                return "Try drinking slightly more water each time 💧"
            elif intake_ml < 500:
                return "Good hydration habit! Keep it consistent 👍"
            else:
                return "Excellent intake! You're doing great 💪"
