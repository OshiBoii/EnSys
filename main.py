from flask import Flask, render_template, request
from Bot import EnSysBot

app = Flask(__name__)
chatbot = EnSysBot("gpt-4")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.form['prompt']
    if prompt.upper() == 'END CHAT':
        return 'END CHAT'
    response = chatbot.generate_response(prompt)
    return response

if __name__ == '__main__':
    app.run(debug=True)
