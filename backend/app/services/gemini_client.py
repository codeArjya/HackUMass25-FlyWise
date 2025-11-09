import os

try:
    from google.genai import GoogleGenAI
    USE_GENAI = True
except ImportError:
    USE_GENAI = False

class GeminiAdvisor:
    def __init__(self):
        if USE_GENAI:
            self.ai = GoogleGenAI(apiKey=os.environ.get("API_KEY"))

    def generate_recommendation(
        self,
        decision: str,
        trend: float,
        confidence: float,
        origin: str,
        destination: str
    ) -> str:
        """
        Generate a friendly AI recommendation including airport names and tips.
        - decision: "Buy" or "Wait"
        - trend: predicted price change (positive for rise, negative for drop)
        - confidence: confidence percentage
        - origin: origin airport/city name
        - destination: destination airport/city name
        """

        direction = "rise" if trend >= 0 else "drop"
        abs_trend = abs(trend) * 100

        # Build the prompt for Gemini
        prompt = f"""
        You are a friendly AI travel assistant. Generate a concise 'Buy or Wait' recommendation for a flight from {origin} to {destination}.
        Include:
        - The predicted price change of {abs_trend:.1f}% ({direction})
        - Confidence level of {confidence:.1f}%
        - Practical travel tips (like booking early, day of week suggestions, etc.)
        - Use the airport names naturally in the text.
        
        Example outputs:
        - "Prices for flights from {origin} to {destination} are expected to rise 5% in the next few days — you should buy now. Try booking midweek for the best deals."
        - "Good news! Flights from {origin} to {destination} may drop by 4% soon. We recommend waiting a few days and checking alternate routes for cheaper fares."
        
        Generate a new recommendation following this style.
        """

        if USE_GENAI:
            try:
                resp = self.ai.models.generateContent(model="gemini-2.5-flash", contents=prompt)
                return resp.text.strip()
            except Exception as e:
                print("Gemini error:", e)

        # Fallback message if Gemini fails
        return (
            f"Our analysis suggests you should {decision.lower()} your flight from {origin} to {destination}. "
            f"Prices may {direction} by approximately {abs_trend:.1f}%. "
            f"Tip: booking earlier or midweek flights can sometimes save money."
        )