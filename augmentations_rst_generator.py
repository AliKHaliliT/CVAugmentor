import os

def generate_rst_files(directory, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            # Remove the .py extension to get the module name
            module_name = filename[:-3]
            
            # Create the .rst file content
            rst_content = f""".. automodule:: {directory.replace('/', '.')}.{module_name}
    :members:
    :private-members:
    :special-members: __init__
"""
            # Write the content to the .rst file
            rst_filename = os.path.join(output_dir, f"{module_name}.rst")
            with open(rst_filename, "w") as rst_file:
                rst_file.write(rst_content)
            print(f"Generated {rst_filename}")

# Example usage
directory = "CVAugmentor/assets/augmentations"
output_dir = "rsts/augmentations"
generate_rst_files(directory, output_dir)