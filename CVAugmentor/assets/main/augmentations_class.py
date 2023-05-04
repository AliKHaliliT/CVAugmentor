# Importing the libraries
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
from typing import Optional, Tuple, Union, Callable
import warnings


# Defining the Augmentations class
class Augmentations():

    """
    
    Class containing the image augmentations.
        The augmentations include:
            no_augmentation,
            flip,
            zoom,
            rotate,
            shear,
            grayscale,
            hue,
            saturation,
            brightness,
            exposure,
            blur,
            noise,
            cutout,
            negative.
    
    """
    
    # Defining the constructor
    def __init__(self) -> None:
        
        """

        Constructor of the Augmentations class.
        
        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.
        
        """

        pass


    # Defining the no_augmentation method
    @staticmethod
    def no_augmentation() -> Callable[[Image.Image], Image.Image]:
            
        """

        No augmentation. 
        This can be used when you want to copy the image to the output folder without augmenting it.


        Parameters
        ----------
        None.


        Returns
        -------
        no_augmentation_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def no_augmentation_wrapper(image: Image.Image) -> Image.Image:

            # Return the image
            return image


        # Return the wrapper function
        return no_augmentation_wrapper
    

    # Defining the flip method
    @staticmethod
    def flip(flip_type: Optional[str] = "vertical") -> Callable[[Image.Image], Image.Image]:

        """

        Flip the image horizontally or vertically.


        Parameters
        ----------
        flip_type : str, optional
            Type of flip. The default is "vertical".
                The options are:
                    "horizontal"
                        Flip the image horizontally
                    "vertical"
                        Flip the image vertically


        Returns
        -------
        flip_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def flip_wrapper(image: Image.Image) -> Image.Image:

            # Check if the flip_type is valid
            if flip_type != "horizontal" and flip_type != "vertical":
                raise ValueError("flip_type must be either 'horizontal' or 'vertical'")
            

            # Convert the image to a numpy array
            img = np.array(image)
            
            # Flip the image
            if flip_type == "horizontal":
                img = np.fliplr(img)
            elif flip_type == "vertical":
                img = np.flipud(img)

            # Convert the image back to a PIL image
            img_flipped = Image.fromarray(img)


            # Return the flipped image
            return img_flipped
    

        # Return the wrapper function
        return flip_wrapper


    # Defining the zoom method
    @staticmethod
    def zoom(zoom_size: Optional[Tuple[Union[int, float], Union[int, float]]] = None) -> Callable[[Image.Image], Image.Image]:

        """

        Zoom the image.


        Parameters
        ----------
        zoom_size : tuple, optional
            Size of the zoom. The default is None. If None, a random zoom size is generated.


        Returns
        -------
        zoom_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def zoom_wrapper(image: Image.Image) -> Image.Image:

            # Get the width and height of the image
            width = image.size[0]
            height = image.size[1]

            # If zoom_size is None, generate a random zoom size
            nonlocal zoom_size

            if zoom_size is None:

                zoom_width = np.random.randint(min(width, height) // 2.5, min(width, height) // 1.5)
                zoom_height = np.random.randint(min(width, height) // 2.5, min(width, height) // 1.5)
                zoom_size = (zoom_width, zoom_height)


            # Check if the zoom_size is valid
            if not isinstance(zoom_size, tuple):
                raise ValueError("zoom_size must be a tuple of positive decimal values (width, height)")

            # Check if the zoom_size is valid
            if zoom_size[0] < 0 or zoom_size[1] < 0:
                raise ValueError("zoom_size must be a tuple of positive decimal values (width, height)")
            

            # Generate a random x-position and y-position for the zoom
            x = np.random.RandomState(42).randint(0, width - zoom_size[0])
            y = np.random.RandomState(42).randint(0, height - zoom_size[1])

            # Zoom the image using the random position and zoom size
            zoom = image.crop((x, y, x + zoom_size[0], y + zoom_size[1]))

            # Resize the zoomed image to the original size
            img_zoomed = zoom.resize((width, height))


            # Return the zoomed image
            return img_zoomed
        

        # Return the wrapper function
        return zoom_wrapper
    

    # Defining the rotate method
    @staticmethod
    def rotate(rotate_type: Optional[str] = "definite", angle: Optional[Union[int, float]] = 90) -> Callable[[Image.Image], Image.Image]:

        """

        Rotate the image by a definite angle or a random angle.


        Parameters
        ----------
        rotate_type : str, optional
            Type of rotation. The default is "definite".
                The options are:
                    "definite"
                        Rotate the image by a definite angle
                    "random"
                        Rotate the image by a random angle
                        
        angle : int or float, optional if rotate_type is "random"
            Angle of rotation. The default is 90.
        
            
        Returns
        -------
        rotate_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def rotate_wrapper(image: Image.Image) -> Image.Image:

            # Check if the rotate_type is valid
            if rotate_type != "definite" and rotate_type != "random":
                raise ValueError("rotate_type must be either 'definite' or 'random'")
            
            # Check if the angle is valid
            nonlocal angle

            if not isinstance(angle, (int, float)):
                raise ValueError("angle must be either int or float")
            

            # Self-explanatory
            if rotate_type == "definite":
                pass
            elif rotate_type == "random":
                angle = np.random.randint(-angle, angle)

            # Rotate the image
            img_rotated = image.rotate(angle)


            # Return the rotated image
            return img_rotated
        

        # Return the wrapper function
        return rotate_wrapper
    

    # Defining the shear method
    @staticmethod
    def shear(shear: Optional[Tuple[Union[int, float], Union[int, float]]] = None) -> Callable[[Image.Image], Image.Image]:

        """

        Shear the image. The shearing means that the image is slanted along the x-axis and/or y-axis.


        Parameters
        ----------
        shear : tuple, optional
            Shear values. The default is None. If None, a random shear value is generated.
        
            
        Returns
        -------
        shear_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def shear_wrapper(image: Image.Image) -> Image.Image:

            # If shear is None, generate a random shear value
            nonlocal shear

            if shear is None:

                shear_x = np.random.uniform(-0.5, 0.5)
                shear_y = np.random.uniform(-0.5, 0.5)
                shear = (shear_x, shear_y)
                

            # Check if the shear is valid
            if not isinstance(shear, tuple):
                raise ValueError("shear must be a tuple of decimal values (x, y)")
            
            # Check if the shear is valid
            if shear[0] < -1 or shear[0] > 1 or shear[1] < -1 or shear[1] > 1:
                raise ValueError("shear must be a tuple of decimal values (x, y) between -1 and 1")
            
            # Check if the shear is reasonable
            if shear[0] < -0.5 or shear[0] > 0.5 or shear[1] < -0.5 or shear[1] > 0.5:
                warnings.warn("The optimal value for shear is between -0.5 and 0.5.")


            # Shear the image
            img_sheared = image.transform(image.size, Image.AFFINE, (1, shear[0], 0, shear[1], 1, 0))


            # Return the sheared image
            return img_sheared
        

        # Return the wrapper function
        return shear_wrapper

    
    # Defining the grayscale method
    @staticmethod
    def grayscale() -> Callable[[Image.Image], Image.Image]:

        """

        Convert the image to grayscale. The grayscale conversion is done using the formula:
            gray_value = 0.2989 * r + 0.5870 * g + 0.1140 * b
        Note that the grayscale conversion is keeping the image in RGB format in order to be consistent with the other methods.


        Parameters
        ----------
        None.
            
        
        Returns
        -------
        grayscale_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def grayscale_wrapper(image: Image.Image) -> Image.Image:

            # Convert the image to grayscale using the RGB weighted method
            gray_image = image.convert("L")
            
            # Create a new image with 3 channels by copying the grayscale image
            img_grayed = Image.new("RGB", gray_image.size)
            img_grayed.paste(gray_image)


            # Return the grayscaled image
            return img_grayed
    

        # Return the wrapper function
        return grayscale_wrapper
    

    # Defining the hue method
    @staticmethod
    def hue(hue_shift: Optional[Union[int, float]] = None) -> Callable[[Image.Image], Image.Image]:

        """

        Shift the hue of the image. Hue is the color of the image.
        

        Parameters
        ----------
        hue_shift : int or float, optional
            Hue shift value. The default is None. If None, a random hue shift value is generated.

            
        Returns
        -------
        hue_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def hue_wrapper(image: Image.Image) -> Image.Image:

            # If hue_shift is None, generate a random hue shift value
            nonlocal hue_shift

            if hue_shift is None:
                hue_shift = np.random.uniform(-360, 360)


            # Check if the hue_shift is valid
            if not isinstance(hue_shift, (int, float)):
                raise ValueError("hue_shift must be either int or float")
            
            # Check if the hue_shift is valid
            if hue_shift < -360 or hue_shift > 360:
                raise ValueError("hue_shift must be a value between -360 and 360")


            # Convert the image to the HSV color space
            hsv_image = image.convert('HSV')

            # Split the channels into separate arrays
            h, s, v = hsv_image.split()

            # Apply the hue shift to the hue channel
            h_data = np.array(h)
            h_data = (h_data + hue_shift) % 256
            h = Image.fromarray(h_data.astype('uint8'), mode='L')

            # Combine the channels back into an RGB image
            hsv_image = Image.merge('HSV', (h, s, v))
            img_hued = hsv_image.convert('RGB')


            # Return the hue shifted image
            return img_hued
        

        # Return the wrapper function
        return hue_wrapper
    

    # Defining the saturation method
    @staticmethod
    def saturation(saturation_factor: Optional[Union[int, float]] = None) -> Callable[[Image.Image], Image.Image]:

        """

        Adjust the saturation of the image. The stauration means the intensity of the colors.


        Parameters
        ----------
        saturation_factor : int or float, optional
            Saturation factor. The default is None. If None, a random saturation factor is generated.


        Returns
        -------
        saturation_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def saturation_wrapper(image: Image.Image) -> Image.Image:

            # If saturation_factor is None, generate a random saturation factor
            nonlocal saturation_factor

            if saturation_factor is None:
                saturation_factor = np.random.uniform(0, 0.5)


            # Check if the saturation_factor is valid
            if not isinstance(saturation_factor, (int, float)):
                raise ValueError("saturation_factor must be either int or float")
            

            # Convert the image to the HSV color space
            img_saturated = ImageEnhance.Color(image).enhance(1 + saturation_factor)


            # Return the saturation adjusted image
            return img_saturated
        

        # Return the wrapper function
        return saturation_wrapper
    

    # Defining the brightness method
    @staticmethod
    def brightness(brightness_factor: Optional[Union[int, float]] = None) -> Callable[[Image.Image], Image.Image]:

        """

        Adjust the brightness of the image.


        Parameters
        ----------
        brightness_factor : int or float, optional
            Brightness factor. The default is None. If None, a random brightness factor is generated.


        Returns
        -------
        brightness_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def brightness_wrapper(image: Image.Image) -> Image.Image:

            # If brightness_factor is None, generate a random brightness factor
            nonlocal brightness_factor

            if brightness_factor is None:
                brightness_factor = np.random.uniform(0, 0.5)


            # Check if the brightness_factor is valid
            if not isinstance(brightness_factor, (int, float)):
                raise ValueError("brightness_factor must be either int or float")
            

            # Adjust the brightness of the image
            img_brightened = ImageEnhance.Brightness(image).enhance(1 + brightness_factor)


            # Return the brightness adjusted image
            return img_brightened
    

        # Return the wrapper function
        return brightness_wrapper
    

    # Defining the exposure method
    @staticmethod
    def exposure(exposure_factor: Optional[Union[int, float]] = None) -> Callable[[Image.Image], Image.Image]:

        """

        Adjust the exposure of the image. The exposure means the amount of light that reaches the image sensor.


        Parameters
        ----------
        exposure_factor : int or float, optional
            Exposure factor. The default is None. If None, a random exposure factor is generated.


        Returns
        -------
        exposure_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """
        
        # Defining the wrapper function
        def exposure_wrapper(image: Image.Image) -> Image.Image:

            # If exposure_factor is None, generate a random exposure factor
            nonlocal exposure_factor

            if exposure_factor is None:
                exposure_factor = np.random.uniform(0.3, 1.7)


            # Check if the exposure_factor is valid
            if not isinstance(exposure_factor, (int, float)):
                raise ValueError("exposure_factor must be either int or float")
            
            # Check if the exposure_factor is reasonable
            if exposure_factor < 0.3 or exposure_factor > 1.7:
                warnings.warn("The optimal value for exposure_factor is between 0.3 and 1.7.")


            # Convert PIL image to numpy array
            img_array = np.array(image)

            # Multiply pixel values by the exposure factor
            img_output = img_array * exposure_factor

            # Clip the pixel values to ensure they are within the valid range [0, 255]
            img_output = np.clip(img_output, 0, 255).astype(np.uint8)

            # Convert numpy array back to PIL image
            img_exposed = Image.fromarray(img_output)


            # Return the exposure adjusted image
            return img_exposed
        

        # Return the wrapper function
        return exposure_wrapper

    
    # Defining the blur method
    @staticmethod
    def blur(radius: Optional[Union[int, float]] = None) -> Callable[[Image.Image], Image.Image]:

        """

        Blur the image. The blur radius is the standard deviation of the Gaussian blur.


        Parameters
        ----------
        radius : int or float, optional
            Blur radius. The default is None. If None, a random blur radius is generated.


        Returns
        -------
        blur_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def blur_wrapper(image: Image.Image) -> Image.Image:

            # If radius is None, generate a random radius
            nonlocal radius

            if radius is None:
                radius = np.random.randint(0, 5)
                
            
            # Check if the radius is valid
            if not isinstance(radius, (int, float)):
                raise ValueError("radius must be either int or float")
            
            # Check if the radius is valid
            if radius < 0:
                raise ValueError("radius must be a positive value")
            
            # Check if the radius is reasonable
            if radius > 5:
                warnings.warn("The optimal value for radius is between 0 and 5.")


            # Blur the image
            img_blurred = image.filter(ImageFilter.GaussianBlur(radius))


            # Return the blurred image
            return img_blurred
        

        # Return the wrapper function
        return blur_wrapper
    

    # Defining the noise method
    @staticmethod
    def noise(intensity: Optional[Union[int, float]] = None) -> Callable[[Image.Image], Image.Image]:

        """

        Add noise to the image. This method adds noise to the image by multiplying the pixel values by a random number between -1 and 1.
        It creates a noisy image that looks like the output from an analog TV with bad reception.


        Parameters
        ----------
        intensity : int or float, optional
            Noise intensity. The default is None. If None, a random noise intensity is generated.


        Returns
        -------
        noise_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def noise_wrapper(image: Image.Image) -> Image.Image:

            # If intensity is None, generate a random intensity
            nonlocal intensity

            if intensity is None:
                intensity = np.random.uniform(-1, 1)


            # Check if the intensity is valid
            if not isinstance(intensity, (int, float)):
                raise ValueError("intensity must be either int or float")
            
            # Check if the intensity is reasonable
            if intensity < -1 or intensity > 1:
                warnings.warn("The optimal value for intensity is between -1 and 1.")
        
        
            # Convert the image to a numpy array
            img_array = np.array(image)

            # Generate a noise array with the same dimensions as the image
            noise = np.random.RandomState(42).rand(*img_array.shape) * intensity

            # Add the noise to the pixel values of the image
            noisy_img = np.clip(img_array + noise * 255, 0, 255).astype(np.uint8)

            # Convert the numpy array back to an image
            img_noised = Image.fromarray(noisy_img)


            # Return the noisy image
            return img_noised
        

        # Return the wrapper function
        return noise_wrapper

    
    # Defining the cutout method
    @staticmethod
    def cutout(max_count: Optional[int] = None, max_size: Optional[Union[int, float]] = None) -> Callable[[Image.Image], Image.Image]:

        """

        Cutout a random part of the image. This method cuts out a random part of the image and replaces it with a black rectangle.


        Parameters
        ----------
        max_size : int or float, optional
            Maximum size of the cutout. The default is None. If None, a random maximum size is generated.

        max_count : int, optional
            Maximum number of cutouts. The default is None. If None, a random maximum count is generated.


        Returns
        -------
        cutout_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def cutout_wrapper(image: Image.Image) -> Image.Image:

            # Get the width and height of the image
            width = image.size[0]
            height = image.size[1]

            # If max_count is None, generate a random max_count
            nonlocal max_count

            if max_count is None:
                max_count = np.random.randint(1, 6)

            # If max_size is None, generate a random max_size
            nonlocal max_size

            if max_size is None:
                max_size = np.random.randint(1, min(width, height) // 4)


            # Check if the max_count is valid
            if not isinstance(max_count, int):
                raise ValueError("max_count must be an integer")
            
            # Check if the max_size is valid
            if not isinstance(max_size, (int, float)):
                raise ValueError("max_size must be either int or float")


            # Convert the image to a numpy array
            img = np.array(image)

            # Generate random cutouts
            for _ in range(max_count):

                # Generate random coordinates
                y = np.random.randint(0, width - max_size + 1)
                x = np.random.randint(0, height - max_size + 1)

                # Cutout the image
                img[x:x + max_size, y:y + max_size, :] = 0

            # Convert the numpy array back to an image
            img_cuttedout = Image.fromarray(img)


            # Return the cutout image
            return img_cuttedout
        

        # Return the wrapper function
        return cutout_wrapper
    

    # Defining the negative method
    @staticmethod
    def negative() -> Callable[[Image.Image], Image.Image]:

        """

        Convert the image to negative. This method converts the image to negative by inverting the pixel values.


        Parameters
        ----------
        None.

        
        Returns
        -------
        negative_wrapper : function
            Args:
                image : Image.Image
                    The image to be augmented.

        """

        # Defining the wrapper function
        def negative_wrapper(image: Image.Image) -> Image.Image:

            # Invert the image using the ImageOps.invert() method
            image = image.convert("RGB")
            img_negatived = ImageOps.invert(image)
            

            # Return the negatived image
            return img_negatived
    

        # Return the wrapper function
        return negative_wrapper