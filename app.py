from flask import Flask, render_template, request, send_file, jsonify
import google.generativeai as palm
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Configure the API key
palm.configure(api_key="AIzaSyDQegtx6ycbXTp7treDwhdzmba2V6WdSQ0")

# Define the model
model = "models/chat-bison-001"

app = Flask(__name__)

def generate_business_idea():
    response = palm.chat(model=model, messages=["Generate a business idea."])
    return response['candidates'][0]['message']['content']

def generate_catchphrase():
    response = palm.chat(model=model, messages=["Generate a catchphrase."])
    return response['candidates'][0]['message']['content']

def generate_logo(text="Logo"):
    # Create an image with white background
    img = Image.new('RGB', (200, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Define a font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Add text to the image
    d.text((10, 30), text, fill=(0, 0, 0), font=font)
    
    # Save the image to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/catchphrases")
def catchphrases():
    catchphrase = generate_catchphrase()
    return render_template("catchphrases.html", catchphrase=catchphrase)

@app.route("/logos")
def logos():
    logo_image = generate_logo("Your Logo")
    return send_file(logo_image, mimetype='image/png')

@app.route("/business_ideas")
def business_ideas():
    business_idea = generate_business_idea()
    return render_template("business_ideas.html", business_idea=business_idea)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
