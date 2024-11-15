from flask import Flask, render_template, request
from Bot import EnSysBot

app = Flask(__name__)
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
    prompt = request.form['prompt']
    if prompt.upper() == 'END CHAT':
        return 'END CHAT'
    response = chatbot.generate_response(prompt)
    return response

if __name__ == '__main__':
    app.run(debug=True)
