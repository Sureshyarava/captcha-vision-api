## Overview

This project is a Flask-based REST API that decodes CAPTCHA images using image processing techniques and a pre-trained machine learning model. The API allows users to upload CAPTCHA images and receive the decoded text in response.

## Features

- Upload CAPTCHA images via a POST request.
- Decodes CAPTCHA text using a trained model. (Refer to https://github.com/Sureshyarava/Captcha-Vision repository for data set and training the model)
- Returns the decoded text in JSON format.

## Technologies Used

- Flask: A lightweight WSGI web application framework in Python.
- OpenCV: A library for computer vision tasks.
- NumPy: A library for numerical operations in Python.
- TensorFlow/Keras: For loading and using the machine learning model.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/captcha-decoder.git
   cd captcha-decoder
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the pre-trained model:**

   Place your `captcha_vision_model.keras` file in the project directory.

5. **Create an image folder:**

   Ensure there is a folder named `Image_folder` in the project directory to store uploaded images.

## Usage

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

   The application will start on `http://127.0.0.1:5000`.

2. **Send a POST request to decode a CAPTCHA:**

   You can use tools like `curl` or Postman to send a request. Here’s an example using `curl`:

   ```bash
   curl -X POST -F "image=@path_to_your_captcha_image.png" http://127.0.0.1:5000/decode_captcha
   ```

   Replace `path_to_your_captcha_image.png` with the path to your CAPTCHA image.

3. **Response:**

   The API will respond with the decoded text in JSON format:

   ```json
   {
       "message": "decoded_text_here"
   }
   ```
```

### Notes:

- Replace `https://github.com/yourusername/captcha-decoder.git` with the actual URL of your GitHub repository.
- Ensure that you have a `requirements.txt` file that lists all the dependencies of your project.
- You can customize the sections further based on your specific project details and requirements.

This README provides a comprehensive guide for users to understand, install, and use your Flask CAPTCHA decoder API. If you need any more specific sections or further customization, feel free to ask!
