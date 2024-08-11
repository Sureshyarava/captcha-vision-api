from flask import Flask, jsonify, request
from services import DecodeService
import os

app = Flask(__name__)

# Ensure the image folder exists
IMAGE_FOLDER = "../Image_folder"
os.makedirs(IMAGE_FOLDER, exist_ok=True)


@app.route("/decode_captcha", methods=["POST"])
def decode_captcha():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    image = request.files["image"]

    image_path = os.path.join(IMAGE_FOLDER, "image.png")
    image.save(image_path)

    decode_service = DecodeService()
    message, status_code = decode_service.get_text_from_captcha(image_path)

    return jsonify({"message": message}), status_code


if __name__ == "__main__":
    app.run(debug=True)