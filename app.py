from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# Load environment variables including OPENAI_API_KEY
load_dotenv()

# Import all bots
from bots.knowledge_bot import get_knowledge_response  # uses OpenAI
from bots.emotional_bot import analyze_emotion         # your custom bot
from bots.data_bot import analyze_file                 # Updated for universal file handling

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/knowledge', methods=['GET', 'POST'])
def knowledge():
    answer = None
    if request.method == 'POST':
        query = request.form['query']
        answer = get_knowledge_response(query)  # 👉 OpenAI response
    return render_template('knowledge.html', answer=answer)

@app.route('/emotion', methods=['GET', 'POST'])
def emotion():
    result = None
    if request.method == 'POST':
        text = request.form['text']
        result = analyze_emotion(text)  # 👉 your emotion logic
    return render_template('emotion.html', result=result)

@app.route('/data', methods=['GET', 'POST'])
def data():
    summary = None
    if request.method == 'POST':
        file = request.files['file']
        summary = analyze_file(file)  # 👉 Updated to handle multiple file types
    return render_template('data.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
