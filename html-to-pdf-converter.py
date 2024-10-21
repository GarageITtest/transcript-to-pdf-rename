import os
import logging
from PIL import Image
import imgkit
from tqdm import tqdm  # Import tqdm for progress bar

# Set the path to wkhtmltoimage executable
WKHTMLTOIMAGE_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'  # Update this path

# Configure imgkit to use the specified wkhtmltoimage path
config = imgkit.config(wkhtmltoimage=WKHTMLTOIMAGE_PATH)

# Set the logging
logging.basicConfig(
    filename='html_to_pdf_conversion.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a StreamHandler to log to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logging.getLogger().addHandler(console_handler)

def convert_html_to_image(input_path, output_image_path):
    """Convert HTML file to an image."""
    try:
        imgkit.from_file(input_path, output_image_path, config=config)
        logging.info(f"Successfully converted {input_path} to image {output_image_path}")
        return True
    except Exception as e:
        logging.error(f"Error converting {input_path} to image: {e}")
        return False

def convert_image_to_pdf(image_path, pdf_path):
    """Convert image file to PDF."""
    try:
        with Image.open(image_path) as img:
            img.convert('RGB').save(pdf_path, "PDF", resolution=100.0)
        logging.info(f"Successfully converted {image_path} to PDF {pdf_path}")
    except Exception as e:
        logging.error(f"Error converting {image_path} to PDF: {e}")

def recursive_convert(directory):
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    # Use tqdm for progress bar
    for html_file in tqdm(html_files, desc="Converting HTML to PDF", unit="file"):
        # Generate output paths
        image_file = os.path.splitext(html_file)[0] + ".png"
        pdf_file = os.path.splitext(html_file)[0] + ".pdf"

        # Convert HTML to Image
        if convert_html_to_image(html_file, image_file):
            # Convert Image to PDF
            convert_image_to_pdf(image_file, pdf_file)
            # Optionally, remove the intermediate image file
            os.remove(image_file)

if __name__ == "__main__":
    directory = input("Enter the directory to scan for HTML files: ")
    if os.path.exists(directory) and os.path.isdir(directory):
        logging.info(f"Starting conversion in directory: {directory}")
        recursive_convert(directory)
        logging.info("Conversion process completed.")
        print("Conversion process completed. Check the log for details.")
    else:
        logging.error(f"Directory not found: {directory}")
        print(f"Error: Directory '{directory}' not found.")
