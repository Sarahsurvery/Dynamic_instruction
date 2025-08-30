import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
from hotels.hotels import hotels   # ✅ this now imports the dictionary

# Load .env
load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL_NAME")

genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel(model_name)

class HotelAgent:
    """Agent to store and retrieve multiple hotel details dynamically."""

    def __init__(self):
        self.context = []  # stores conversation history

    def query(self, user_input: str) -> str:
        self.context.append({"role": "user", "content": user_input})

        # Check if the query matches a hotel
        hotel_found = None
        for hotel_name, details in hotels.items():   # ✅ now works
            if hotel_name.lower() in user_input.lower() or details["location"].lower() in user_input.lower():
                hotel_found = (hotel_name, details)
                break

        if hotel_found:
            name, info = hotel_found
            hotel_info = (
                f"🏨 {name} Hotel in {info['location']}\n"
                f"Rooms Available: {info['rooms']}\n"
                f"Price per night: ${info['price_per_night']}\n"
                f"Amenities: {', '.join(info['amenities'])}"
            )
            response_text = f"Here are the details:\n{hotel_info}"
        else:
            response = gemini_model.generate_content(
                f"You are a hotel booking assistant. "
                f"Answer the query based on known hotels: {list(hotels.keys())}.\n"
                f"User: {user_input}"
            )
            response_text = response.text

        self.context.append({"role": "agent", "content": response_text})
        return response_text
