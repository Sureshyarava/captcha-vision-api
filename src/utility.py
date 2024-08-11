import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model


class Captcha_Vision:
    IMAGE_FOLDER = "../Image_folder"  # Ensure the image is uploaded to this folder

    def __init__(self):
        self.model = load_model("captcha_vision_model.keras")
        self.unique_characters = ['2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',
                                  'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',
                                  'U', 'V', 'W', 'X', 'Y', 'Z']

    def pad_array_to_size(self, array, target_size):
        """Pads the input array to the target size with white pixels."""
        current_shape = array.shape
        padding = [(max((target_size[i] - current_shape[i]) // 2, 0),
                    max((target_size[i] - current_shape[i] + 1) // 2, 0)) for i in range(len(current_shape))]
        return np.pad(array, padding, mode='constant', constant_values=255)

    def split_images_and_get_text(self, grps, average_character_width, binary_image):
        """Splits the binary image into characters and predicts their text."""
        height = binary_image.shape[0]
        res = ""

        for start, end in grps:
            left = start
            right = max(end, start + average_character_width)
            character = binary_image[0:height, left:right + 1]
            character = self.pad_array_to_size(character, (50, 50))
            character = cv2.cvtColor(character, cv2.COLOR_GRAY2RGB)
            character = character.reshape((1, 50, 50, 3))
            res += self.unique_characters[np.argmax(self.model.predict(character, verbose=False))]

        return res

    def find_large_zero_groups(self, data, threshold=1):
        """Finds groups of zeros in the input data."""
        zero_groups = []
        count = 0
        start_index = -1

        for i in range(len(data)):
            if data[i] == 0:
                if count == 0:
                    start_index = i
                count += 1
            else:
                if count > threshold:
                    zero_groups.append((start_index, count))
                count = 0

        if count > threshold:
            zero_groups.append((start_index, count))

        return zero_groups

    def segment_characters_from_binary_image(self, binary_image):
        """Segments characters from the binary image based on vertical projection."""
        binImage_cpy = binary_image.copy()
        binImage_cpy[binImage_cpy == 0] = 1
        binImage_cpy[binImage_cpy == 255] = 0
        vertical_projection = np.sum(binImage_cpy, axis=0)
        zero_grps = self.find_large_zero_groups(vertical_projection)

        non_zero_grps = []
        for i in range(len(zero_grps) - 1):
            start = zero_grps[i][0] + zero_grps[i][1]
            end = zero_grps[i + 1][0]
            non_zero_grps.append((start, end - 1))

        average_character_width = sum(y - x + 1 for x, y in non_zero_grps) // len(non_zero_grps) if non_zero_grps else 0

        if len(non_zero_grps) == 4:
            return self.split_images_and_get_text(non_zero_grps, average_character_width, binary_image)
        else:
            grps = []
            threshold = average_character_width // 2
            for start, end in non_zero_grps:
                if abs(average_character_width - (end - start)) > threshold:
                    grps.append((start, start + average_character_width + 2))
                    if end > start + average_character_width + 2:
                        grps.append((start + average_character_width, end))
                else:
                    grps.append((start, end))
            return self.split_images_and_get_text(grps, average_character_width, binary_image)

    def get_captcha_text(self, image_name):
        """Reads an image, preprocesses it, and extracts the CAPTCHA text."""
        path = os.path.join(self.IMAGE_FOLDER, image_name)
        image = cv2.imread(path)

        if image is None:
            raise FileNotFoundError(f"Image {image_name} not found in {self.IMAGE_FOLDER}.")

        if image.shape[0] >= 50:
            image = cv2.resize(image, (35, 35))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        binary_image = 255 - binary_image

        return self.segment_characters_from_binary_image(binary_image)