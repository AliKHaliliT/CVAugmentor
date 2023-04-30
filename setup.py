# Importing the libraries
from setuptools import setup


# Defining the readme function
def readme():
    with open('README.md') as f:
        return f.read()
    

# Defining the setup function
setup(name='CVAugmentor',
        version='1.0.0',
        description='A package for augmenting images and videos for computer vision tasks',
        long_description=readme(),
        long_description_content_type='text/markdown',
        url='https://github.com/AliKHaliliT/CVAugmentor',
        author='Ali Khalili Tazehkandgheshlagh',
        author_email='ali.khalili.t98@gmail.com',
        license='MIT',
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
        ],
        packages=['CVAugmentor', 'CVAugmentor.assets', 'CVAugmentor.assets.utils', 'CVAugmentor.assets.main'],
        include_package_data=True,
)