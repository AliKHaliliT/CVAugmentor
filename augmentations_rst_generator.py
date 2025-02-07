import os
from CVAugmentor.assets.utils.sort_alphanumerically import sorted_alphanumerically


def generate_rst_files(directory, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    rst_filenames = []

    # Iterate over all files in the directory
    for filename in sorted_alphanumerically(os.listdir(directory)):
        if filename.endswith(".py") and filename != "__init__.py":
            # Remove the .py extension to get the module name
            module_name = filename[:-3]
            
            # Generate title by removing underscores and capitalizing the first letter
            title = module_name.lstrip('_').replace("_", " ").title()
            
            # Create the .rst file content
            rst_content = f"""{title}
{'=' * len(title)}

.. automodule:: {directory.replace('/', '.')}.{module_name}
    :members:
    :private-members:
    :special-members: __init__
"""
            
            # Write the content to the .rst file
            rst_filename = os.path.join(output_dir, f"{module_name}.rst")
            with open(rst_filename, "w") as rst_file:
                rst_file.write(rst_content)
            rst_filenames.append(f"    {output_dir}/{module_name}")
            print(f"Generated {rst_filename}")
    
    return rst_filenames

def update_index_rst(output_dir, rst_filenames):
    index_content = """CVAugmentor
=======================================

.. automodule:: CVAugmentor
    :members:

.. toctree::
    :caption: Main
    :maxdepth: 1

    rsts/main/pipeline

    
.. toctree::
    :caption: Augmentations
    :maxdepth: 1

"""
    index_content += "\n".join(rst_filenames)
    
    index_filename = "index.rst"
    with open(index_filename, "w") as index_file:
        index_file.write(index_content)
    print(f"Updated {index_filename}")

# Example usage
directory = "CVAugmentor/assets/augmentations"
output_dir = "rsts/augmentations"
rst_files = generate_rst_files(directory, output_dir)
update_index_rst("rsts", rst_files)
