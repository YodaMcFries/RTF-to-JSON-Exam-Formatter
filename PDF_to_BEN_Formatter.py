import pdfplumber
from pdf2image import convert_from_path
import os


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


def extract_images_from_pdf(pdf_path, output_folder):
    # Convert each page of PDF to an image using pdf2image
    images = convert_from_path(pdf_path, 300)  # 300 dpi

    # Save images as PNG files
    image_paths = []
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for idx, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{idx + 1}.png")
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    return image_paths


# Example usage
pdf_path = '350-401 V41.65.pdf'
output_folder = 'extracted_images'

# Extract text
text = extract_text_from_pdf(pdf_path)
print(text[:500])  # Print first 500 characters of extracted text

# Extract images
images = extract_images_from_pdf(pdf_path, output_folder)
print(f"Images saved to: {images}")
