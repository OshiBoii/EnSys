import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
import nltk
from nltk.tokenize import word_tokenize

openai.api_key = "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"

class EnSysBot:
    def __init__(self, engine):
        self.engine = engine
        self.conversation = []
        self.nlp = spacy.load("en_core_web_sm")
        nltk.download('punkt')
        self.analyzer = SentimentIntensityAnalyzer()

    def add_system_message(self, content):
        self.conversation.append({"role": "system", "content": content})

    def add_user_message(self, content):
        self.conversation.append({"role": "user", "content": content})

    def get_sentiment(self, text):
        # Use Vader SentimentIntensityAnalyzer to get sentiment
        return self.analyzer.polarity_scores(text)

    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_user_message(prompt)

        # Read restaurant information from the file
        with open('conversation_data.txt', 'r') as file:
            restaurant_data = file.read()

        # Add restaurant information as system messages
        self.add_system_message(restaurant_data)

        # Analyze sentiment of the prompt
        sentiment = self.get_sentiment(prompt)
        empathy_statement = ""
        if sentiment['compound'] < -0.05:
            empathy_statement = "I'm sorry to hear that you're not satisfied with the menu offerings. "

        try:
            # Make a request to the OpenAI API using the chat-based endpoint with conversation context
            response = openai.ChatCompletion.create(
                model=self.engine,
                messages=self.conversation
            )
            # Extract the response
            assistant_response = response['choices'][0]['message']['content'].strip()
            # Return the empathetic response combined with the API response
            return empathy_statement + assistant_response
        except Exception as e:
            print('Error Generating Response:', e)
            return "I encountered an error while generating a response."

# Example usage:
if __name__ == "__main__":
    bot = EnSysBot("gpt-4")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Bot: Goodbye!")
            break
        print("Bot:", bot.generate_response(user_input))
