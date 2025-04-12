import os
from utils.masker import mask_aadhaar_number

def main():
    input_image = 'images/aadhar card.webp'  # change this to your input image path
    output_image = 'images/masked_aadhaar.jpg'

    print("Masking Aadhaar number...")
    try:
          result_path = mask_aadhaar_number(input_image, output_image)
          print(f"Masked image saved to: {result_path}")
    except FileNotFoundError as fnf:
        print(f"File error: {fnf}")
    except Exception as e:
        print(f"Unexpected error: {e}")
if __name__ == '__main__':
    main()