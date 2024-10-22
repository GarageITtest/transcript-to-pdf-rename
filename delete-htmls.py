import os
import logging
from tqdm import tqdm  # Import tqdm for progress bar

# Set up logging
logging.basicConfig(
    filename='delete_html_files.log',
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

def delete_html_files(directory):
    """Recursively delete all .html files in the given directory."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    # Use tqdm for progress bar
    for html_file in tqdm(html_files, desc="Deleting HTML files", unit="file"):
        try:
            os.remove(html_file)
            logging.info(f"Deleted {html_file}")
        except Exception as e:
            logging.error(f"Error deleting {html_file}: {e}")

if __name__ == "__main__":
    directory = input("Enter the directory to scan for HTML files: ")
    if os.path.exists(directory) and os.path.isdir(directory):
        logging.info(f"Starting deletion in directory: {directory}")
        delete_html_files(directory)
        logging.info("HTML file deletion process completed.")
        print("HTML file deletion process completed. Check the log for details.")
    else:
        logging.error(f"Directory not found: {directory}")
        print(f"Error: Directory '{directory}' not found.")
