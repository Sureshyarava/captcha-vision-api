from utility import Captcha_Vision


class DecodeService:
    def __init__(self):
        self.decoder = Captcha_Vision()

    def get_text_from_captcha(self, name):
        try:
            captcha_text = self.decoder.get_captcha_text(name)
            return captcha_text, 200
        except Exception as e:
            print(f"Error occurred while decoding CAPTCHA: {e}")
            return {"error": "An error occurred while processing the CAPTCHA."}, 400
