from agents import HotelAgent

def main():
    print("🤖 Hotel Booking Agent (powered by Gemini)\n")
    agent = HotelAgent()

    while True:
        msg = input("You: ").strip()
        if msg.lower() in ["exit", "quit"]:
            print("Agent: Goodbye!")
            break

        reply = agent.query(msg)
        print(f"Agent: {reply}\n")

if __name__ == "__main__":
    main()
