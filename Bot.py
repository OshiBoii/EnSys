from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import spacy
import openai
import nltk
from nltk.tokenize import word_tokenize

openai.api_key = "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"

class EnSysBot:
    def __init__(self, engine, conversations):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine
        self.conversations = conversations
        self.restaurant_name = None
        self.menu = None

        # Extract restaurant name and menu from conversations
        self.extract_restaurant_info()

        # Initialize spaCy NLP model
        self.nlp = spacy.load("en_core_web_sm")

        # Initialize NLTK for tokenization
        nltk.download('punkt')

        # Initialize Vader sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()

    def extract_restaurant_info(self):
        for conversation in self.conversations:
            for message in conversation:
                if message.startswith("Restaurant name:"):
                    self.restaurant_name = message.replace("Restaurant name:", "").strip()
                elif message.startswith("Restaurant menu:"):
                    self.menu = message.replace("Restaurant menu:", "").strip().split("\n")

    def add_message(self, role, content):
        # Adds a message to the conversation.
        self.conversation.append({"role": role, "content": content})

    def generate_response(self, prompt):
    # Add user prompt to conversation
        self.add_message("user", prompt)
    
    # Use NLTK for tokenization
    tokens = word_tokenize(prompt)
    
    # Check if the user's prompt contains any keywords related to the restaurant
    if any(word in tokens for word in ['name', 'called', 'menu']):
        # Check if the user is asking about the restaurant name
        if any(word in tokens for word in ['name', 'called']):
            return f"The restaurant name is {self.restaurant_name}."
        # Check if the user is asking about the restaurant menu
        elif 'menu' in tokens:
            menu_items = ", ".join(self.menu)
            return f"The restaurant menu includes: {menu_items}."

    # Use spaCy to process the user's prompt and extract intent and entities
    doc = self.nlp(prompt)
    intent = None
    entity = None
    for token in doc:
        if token.dep_ == "dobj" and token.text.lower() == "name":
            intent = "restaurant_name"
        elif token.dep_ == "dobj" and token.text.lower() == "menu":
            intent = "restaurant_menu"
        elif token.dep_ == "nsubj":
            entity = token.text

    # Handle different intents and entities
    if intent == "restaurant_name":
        return f"The restaurant name is {self.restaurant_name}."
    elif intent == "restaurant_menu":
        menu_items = ", ".join(self.menu)
        return f"The restaurant menu includes: {menu_items}."
    elif entity:
        return f"I'm sorry, I don't have information about {entity} at the moment."
    else:
        # Perform sentiment analysis using both TextBlob and Vader
        textblob_sentiment = self.get_textblob_sentiment(prompt)
        vader_sentiment = self.get_vader_sentiment(prompt)

        # Combine sentiments from both analyzers
        combined_sentiment = self.combine_sentiments(textblob_sentiment, vader_sentiment)

        # Set the appropriate initial response and engine based on sentiment
        initial_response = self.get_initial_response(combined_sentiment)
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


    def get_textblob_sentiment(self, prompt):
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
    
    def get_vader_sentiment(self, prompt):
        # Perform sentiment analysis using Vader
        scores = self.analyzer.polarity_scores(prompt)
        # Get the compound score
        compound_score = scores['compound']
        # Determine sentiment based on compound score
        if compound_score >= 0.05:
            return 'Positive'
        elif compound_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    def combine_sentiments(self, sentiment1, sentiment2):
        # Combine sentiments from both analyzers
        if sentiment1 == 'Positive' and sentiment2 == 'Positive':
            return 'Positive'
        elif sentiment1 == 'Negative' and sentiment2 == 'Negative':
            return 'Negative'
        else:
            return 'Neutral'
    
    def get_initial_response(self, sentiment):
        # Generate initial response based on sentiment
        if sentiment == 'Positive':
            return "Hello! We're glad to hear that you're feeling positive. How can we assist you today?"
        elif sentiment == 'Neutral':
            return "Hello! It seems you're feeling neutral. We're here to help. Please let us know what you need."
        elif sentiment == 'Negative':
            return "Hello! We're sorry to hear that you're feeling negative. We're here to address any concerns or issues you may have."
