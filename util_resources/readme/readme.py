import os
import re
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib as mpl
import numpy as np

# Set the style for the plot
plt.style.use('seaborn-v0_8-darkgrid')

# Customize font and colors for a consistent professional style
mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'text.color': '#333333',
    'axes.labelcolor': '#333333',
    'xtick.color': '#333333',
    'ytick.color': '#333333'
})

# Directory containing the images
image_dir = "local_util_resources/readme"

# Get the list of image files
image_files = [f for f in os.listdir(image_dir) if f.endswith(("png", "jpg", "jpeg", "bmp", "gif"))]

# Set grid parameters
num_cols = 4
num_rows = len(image_files) // num_cols

# Create a function for adding captions
def add_caption(ax, caption):
    ax.text(0.5, -0.1, caption, fontsize=14, ha="center", va="top", transform=ax.transAxes,
            color='#333333', fontweight='bold', fontstyle='italic')

# Create the main image grid
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
axes = axes.flatten()

for i, image_file in enumerate(image_files[:num_rows * num_cols]):
    image_path = os.path.join(image_dir, image_file)
    image = Image.open(image_path)
    base_name = os.path.splitext(image_file)[0]
    caption = re.sub(r"[^a-zA-Z]", ' ', base_name).title()
    
    ax = axes[i]
    ax.imshow(image)
    ax.axis("off")
    add_caption(ax, caption)

# Turn off unused subplots
for i in range(len(image_files[:num_rows * num_cols]), len(axes)):
    axes[i].axis("off")

plt.tight_layout(pad=3.0)
fig.suptitle('Augmentations', fontsize=24, fontweight='bold', color='#333333', y=0.98)

# Save the main figure
output_file = os.path.join(os.path.dirname(__file__), "readme_main.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')

# Handle the remaining images
remaining_images = image_files[num_rows * num_cols:]
if remaining_images:
    fig_remain, axes_remain = plt.subplots(1, len(remaining_images), figsize=(15, 5))
    
    for i, image_file in enumerate(remaining_images):
        image_path = os.path.join(image_dir, image_file)
        image = Image.open(image_path)
        base_name = os.path.splitext(image_file)[0]
        caption = re.sub(r"[^a-zA-Z]", ' ', base_name).title()

        ax = axes_remain[i]
        ax.imshow(image)
        ax.axis("off")
        add_caption(ax, caption)

    plt.tight_layout(pad=3.0)
    output_file_remain = os.path.join(os.path.dirname(__file__), "readme_remain.png")
    plt.savefig(output_file_remain, dpi=300, bbox_inches='tight')

# Load both saved images
main_image = Image.open(output_file)
remain_image = Image.open(output_file_remain)

# Function to add padding to images
def add_padding(image, max_width):
    width, height = image.size
    padding_left = (max_width - width) // 2
    padding_right = max_width - width - padding_left
    padded_image = Image.new('RGB', (max_width, height), (255, 255, 255))
    padded_image.paste(image, (padding_left, 0))
    return padded_image

# Pad the images and combine them
max_width = max(main_image.width, remain_image.width)
main_image_padded = add_padding(main_image, max_width)
remain_image_padded = add_padding(remain_image, max_width)

# Concatenate the images vertically
final_image = np.vstack([np.array(main_image_padded), np.array(remain_image_padded)])
final_image = Image.fromarray(final_image)

# Save and display the final image
final_output_file = os.path.join(os.path.dirname(__file__), "readme.png")
final_image.save(final_output_file)
final_image.show()
