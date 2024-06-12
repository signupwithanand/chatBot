import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="gpt-3.5-turbo",
    )
    message = response.choices[0].message.content.strip()
    
    # Format response as HTML
    formatted_message = format_response_as_html(message)
    
    return jsonify({'response': formatted_message})

def format_response_as_html(message):
    # Split message into paragraphs and add HTML tags
    paragraphs = message.split('\n')
    formatted_message = ''.join([f'<p>{paragraph}</p>' for paragraph in paragraphs])
    return formatted_message

if __name__ == '__main__':
    app.run(debug=True)
