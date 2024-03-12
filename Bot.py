import openai
from textblob import TextBlob  # Import TextBlob for sentiment analysis

openai.api_key = "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"

class EnSysBot:
    def __init__(self, engine):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine

    def add_message(self, role, content):
        # Adds a message to the conversation.
        self.conversation.append({"role": role, "content": content})

    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)
        
        # Perform sentiment analysis using TextBlob
        sentiment = self.get_sentiment(prompt)
        
        # Set the appropriate initial response and engine based on sentiment
        initial_response = self.get_initial_response(sentiment)
        self.add_message("assistant", initial_response)
        self.engine = "gpt-4"
        
        try:
            # Make a request to the API using the chat-based endpoint with conversation context
            response = openai.ChatCompletion.create(model=self.engine, messages=self.conversation)
            # Extract the response
            assistant_response = response['choices'][0]['message']['content'].strip()
            # Add assistant response to conversation
            self.add_message("assistant", assistant_response)
            # Return the response
            return assistant_response
        except Exception as e:
            print('Error Generating Response:', e)
    
    def get_sentiment(self, prompt):
        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(prompt)
        # Get the polarity of the sentiment
        polarity = analysis.sentiment.polarity
        # Determine sentiment based on polarity
        if polarity > 0:
            return 'Positive'
        elif polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'
    
    def get_initial_response(self, sentiment):
        # Generate initial response based on sentiment
        if sentiment == 'Positive':
            return "Hello! We're glad to hear that you're feeling positive. How can we assist you today?"
        elif sentiment == 'Neutral':
            return "Hello! It seems you're feeling neutral. We're here to help. Please let us know what you need."
        elif sentiment == 'Negative':
            return "Hello! We're sorry to hear that you're feeling negative. We're here to address any concerns or issues you may have."
