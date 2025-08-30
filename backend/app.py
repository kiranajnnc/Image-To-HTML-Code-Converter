from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import openai

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

def image_to_html_css(image_base64):
    # This is a mock function.
    # In a real scenario, you would use a vision model or send the image to an AI that can interpret UI and generate code.
    # Here, we use OpenAI GPT to generate code from a prompt.

    prompt = f"""
    You are an expert front-end developer. Given the description of a UI image, generate HTML and CSS code.
    The image is base64 encoded: {image_base64[:100]}... (truncated)
    Generate a simple responsive webpage with HTML and CSS.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You generate HTML and CSS code from UI image descriptions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.2,
    )

    # Extract code from response
    code = response['choices'][0]['message']['content']
    return code

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    image_base64 = data.get('imageBase64')
    if not image_base64:
        return jsonify({"error": "No image provided"}), 400

    try:
        code = image_to_html_css(image_base64)
        return jsonify({"code": code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

