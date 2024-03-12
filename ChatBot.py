from Bot import EnSysBot

class ChatBot:
    def __init__(self):
        self.bot = EnSysBot("gpt-4")

    def start_chat(self):
        print("Bot: You can start chatting now. Type 'quit' to end the conversation.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Bot: Goodbye!")
                break
            response = self.bot.generate_response(user_input)
            print("Bot:", response)

if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.start_chat()
