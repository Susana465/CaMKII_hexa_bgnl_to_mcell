import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

# this one accesses .png_images/

def plot_image_grid(image_folder, columns=4):
    # Get a list of all PNG files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(".png")]
    image_files.sort()  # Sort for consistency

    if not image_files:
        print("No PNG files found in the specified folder.")
        return

    num_images = len(image_files)
    rows = math.ceil(num_images / columns)  # Determine number of rows

    # Create figure
    fig, axes = plt.subplots(rows, columns, figsize=(columns * 3, rows * 3))
    axes = axes.flatten()  # Flatten in case of a single row

    for i, img_file in enumerate(image_files):
        img_path = os.path.join(image_folder, img_file)
        img = mpimg.imread(img_path)
        axes[i].imshow(img)
        axes[i].axis("off")  # Hide axes
        axes[i].set_title(os.path.splitext(img_file)[0], fontsize=8)  # Use filename as title

    # Hide any unused subplots
    for i in range(num_images, len(axes)):
        axes[i].axis("off")

    plt.tight_layout()

    plt.show()

image_folder = "./png_images"  # Change this to your folder path
plot_image_grid(image_folder, columns=4)
