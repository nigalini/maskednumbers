import cv2
import pytesseract
import re
from pathlib import Path

# Set path to tesseract executable (for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def mask_aadhaar_number(image_path, output_path='masked_output.png', method='blackout'):
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read image file: {image_path}")

    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    aadhaar_regex = re.compile(r'\d{4}\s\d{4}\s\d{4}')

    n_boxes = len(data['text'])
    found = False

    # Sliding window of 3 words to check Aadhaar format
    for i in range(n_boxes - 2):
        words = [data['text'][i], data['text'][i+1], data['text'][i+2]]
        if all(word.strip().isdigit() and len(word.strip()) == 4 for word in words):
            aadhaar_candidate = ' '.join(words)
            if aadhaar_regex.fullmatch(aadhaar_candidate):
                # Mask only first two blocks (8 digits)
                for j in range(2):
                    x = data['left'][i + j]
                    y = data['top'][i + j]
                    w = data['width'][i + j]
                    h = data['height'][i + j]

                    if method == 'blur':
                        roi = image[y:y+h, x:x+w]
                        blur = cv2.GaussianBlur(roi, (25, 25), 30)
                        image[y:y+h, x:x+w] = blur
                    else:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)
                found = True

    if not found:
        print("Warning: No Aadhaar number found in the image.")

    cv2.imwrite(output_path, image)
    return output_path

