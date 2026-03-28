"""
Compile Images for Projector Screen
Copyright (C) 2026 Nitish Kapur
GitHub: [github.com/nitish-kapur](https://github.com/nitish-kapur)
Licensed under GNU GPLv3
"""

"""
    1.  Runs automatically in the directory where the script is located —
        no file dialog is required.
    2.  Calculates the projector screen's width and height in inches from
        the specified diagonal size and aspect ratio (default: 201 inches,
        16:9).
    3.  Determines the optimal grid layout (rows and columns) to fit all
        images onto the screen, based on each image's dimensions in inches.
    4.  Calculates a scaling factor to resize each image so that the grid
        fills the screen as closely as possible while maintaining aspect ratio.
    5.  Creates a blank white canvas representing the full projector screen
        at 100 DPI.
    6.  Scans the current directory for all supported image files:
            .jpg, .jpeg, .png, .bmp, .gif
    7.  Resizes each image using the Lanczos resampling filter and places
        it onto the canvas in grid order (left to right, top to bottom).
    8.  Stops placing images once NUM_IMAGES (default: 110) have been
        placed or all available images have been used.
    9.  Saves the final composite image as 'projector_screen.png' inside
        an 'output/' subfolder in the working directory.
"""

import math
import os
from PIL import Image

# Constants
PROJECTOR_DIAGONAL = 201  # Inches (diagonal size of the projector screen)
ASPECT_RATIO_WIDTH = 16
ASPECT_RATIO_HEIGHT = 9
IMAGE_WIDTH_INCHES = 14  # Image size in inches
IMAGE_HEIGHT_INCHES = 10  # Image size in inches
NUM_IMAGES = 110

# Calculate projector screen width and height using the aspect ratio
def calculate_projector_dimensions(diagonal, width_ratio, height_ratio):
    aspect_ratio = math.sqrt(width_ratio ** 2 + height_ratio ** 2)
    width = (width_ratio / aspect_ratio) * diagonal
    height = (height_ratio / aspect_ratio) * diagonal
    return width, height


# Calculate the scaling factor to fit all images on the projector screen
def calculate_resize_factor(screen_width, screen_height, image_width, image_height, num_images):
    # Determine how many images will fit in each row and column
    images_per_row = screen_width // image_width
    images_per_column = screen_height // image_height

    # Calculate the new image size based on the grid arrangement
    new_image_width = screen_width / images_per_row
    new_image_height = screen_height / images_per_column

    # Calculate the scaling factor based on new size vs. original size
    resize_factor_width = new_image_width / image_width
    resize_factor_height = new_image_height / image_height

    # Use the smaller of the two to maintain aspect ratio
    resize_factor = min(resize_factor_width, resize_factor_height)

    return resize_factor, images_per_row, images_per_column


# Arrange and save the images on the projector screen
def arrange_images_on_screen(input_dir, output_dir, image_files, resize_factor, images_per_row, images_per_column):
    # Calculate the new image size
    new_image_width = int(IMAGE_WIDTH_INCHES * resize_factor)  # Convert to integer immediately
    new_image_height = int(IMAGE_HEIGHT_INCHES * resize_factor)  # Convert to integer immediately

    # Calculate the total screen width and height in pixels (assuming 100 DPI for image placement)
    screen_width_pixels = int(PROJECTOR_WIDTH * 100)
    screen_height_pixels = int(PROJECTOR_HEIGHT * 100)

    # Create a blank image (white background) for the projector screen
    screen = Image.new('RGB', (screen_width_pixels, screen_height_pixels), (255, 255, 255))

    # Loop through the images and place them on the screen
    for idx, image_file in enumerate(image_files):
        if idx >= NUM_IMAGES:
            break

        try:
            img_path = os.path.join(input_dir, image_file)
            with Image.open(img_path) as img:
                # Resize the image (convert to integer for dimensions)
                img_resized = img.resize((new_image_width * 100, new_image_height * 100), Image.LANCZOS)

                # Calculate the position on the screen (grid layout)
                row = idx // images_per_row
                col = idx % images_per_row
                x_offset = int(col * new_image_width * 100)  # Ensure this is an integer
                y_offset = int(row * new_image_height * 100)  # Ensure this is an integer

                # Paste the resized image onto the screen
                screen.paste(img_resized, (x_offset, y_offset))

        except Exception as e:
            print(f"Error processing {image_file}: {e}")

    # Save the final screen image
    output_path = os.path.join(output_dir, 'projector_screen.png')
    screen.save(output_path)
    print(f"Projector screen created and saved to: {output_path}")


# Main function
if __name__ == "__main__":
    # Screen dimensions in inches
    PROJECTOR_WIDTH, PROJECTOR_HEIGHT = calculate_projector_dimensions(PROJECTOR_DIAGONAL, ASPECT_RATIO_WIDTH,
                                                                       ASPECT_RATIO_HEIGHT)

    # Calculate the resize factor for each image
    resize_factor, images_per_row, images_per_column = calculate_resize_factor(PROJECTOR_WIDTH, PROJECTOR_HEIGHT,
                                                                               IMAGE_WIDTH_INCHES, IMAGE_HEIGHT_INCHES,
                                                                               NUM_IMAGES)

    # Directory paths
    input_dir = '.'  # Current directory where images are located
    output_dir = './output'  # Directory to save the final screen image

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get image files from the current directory
    image_files = [f for f in os.listdir(input_dir) if
                   any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif'])]
    print(f"Found {len(image_files)} image(s).")

    # Arrange and save the images on the projector screen
    arrange_images_on_screen(input_dir, output_dir, image_files, resize_factor, images_per_row, images_per_column)
