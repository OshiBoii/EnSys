# Importing Libraries
from flask import Flask, render_template, request, url_for  # Add url_for import
from Bot import EnSysBot

# Creating the Flask App
app = Flask(__name__)

# Importing Bot Definition
chatbot = EnSysBot("gpt-4")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat_1')
def chat_1():
    return render_template('chat_1.html')

@app.route('/chat_2')
def chat_2():
    return render_template('chat_2.html')

@app.route('/chat_3')
def chat_3():
    return render_template('chat_3.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Get Prompt from User
    prompt = request.form['prompt']

    # User can stop the chat by sending 'End Chat' as a Prompt
    if prompt.upper() == 'END CHAT':
        return 'END CHAT'

    # Generate and Print the Response from ChatBot
    response = chatbot.generate_response(prompt)
    return response

if __name__ == '__main__':
    app.run(debug=True)
