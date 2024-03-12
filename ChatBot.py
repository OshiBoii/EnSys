from Bot import EnSysBot

class ChatBot:
    def __init__(self):
        self.bot = EnSysBot("gpt-4", [])  # Initialize with empty conversation history

    def load_conversations_from_txt(self, file_path):
        conversations = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            conversation = []
            for line in lines:
                line = line.strip()
                if line:
                    conversation.append(line)
                else:
                    if conversation:
                        conversations.append(conversation)
                    conversation = []
            if conversation:
                conversations.append(conversation)
        return conversations

    def start_chat(self):
        print("Bot: You can start chatting now. Type 'quit' to end the conversation.")
        # Load conversations from the .txt file
        conversations = self.load_conversations_from_txt("conversation_data.txt")
        # Initialize the chatbot with the conversation data
        self.bot = EnSysBot("gpt-4", conversations)
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Bot: Goodbye!")
                break
            response = self.bot.generate_response(user_input)
            print("Bot:", response)

# Testing the ChatBot
if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.start_chat()