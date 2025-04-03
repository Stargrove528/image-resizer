import os
from PIL import Image
import logging

# Set up logging
logging.basicConfig(filename='image_resizing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def resize_image(image_path, max_size=995, total_files=1, current_index=1):
    try:
        with Image.open(image_path) as img:
            original_size = img.size
            width, height = original_size

            # Check if resizing is needed (if either dimension is greater than the max_size)
            if max(width, height) > max_size:
                # Determine the scale factor
                scale_factor = max_size / max(width, height)
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)

                # Resize the image
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Save the resized image
                img.save(image_path)
                logging.info(f"Resized {image_path} from {original_size} to {img.size} successfully.")
            else:
                logging.info(f"No resizing needed for {image_path} (size {original_size}).")
        
        print(f"Progress: {current_index}/{total_files} complete", end='\r')
    except Exception as e:
        logging.error(f"Failed to resize {image_path} due to {e}.")

def process_directory(directory):
    # Collect all image files first
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                image_files.append(os.path.join(root, file))
    
    total_files = len(image_files)
    current_index = 1
    
    # Process each image
    for image_path in image_files:
        resize_image(image_path, total_files=total_files, current_index=current_index)
        current_index += 1

if __name__ == "__main__":
    # Start processing from the script's directory
    process_directory(os.getcwd())
