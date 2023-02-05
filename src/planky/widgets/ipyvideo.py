from ipywidgets import HBox, Image
from io import BytesIO
import PIL

import numpy as np

class Video(HBox):
    def __init__(self, arr=None):
        """
        Initialize an ArrayImage widget for displaying numpy arrays as images.
        To load a new image use the ``show_frame`` function
        Parameters
        ----------
        (Optional) arr: numpy.array()
            Must be of type np.uint8 and suitable shape for a PIL Image
        
        Joel Stansbury
        7/17/2022
        """
        super().__init__()
        self.out = Image()
        self.children = [self.out]
        if arr is not None:
            self.show_frame(arr)
    
    def show_frame(self, arr):
        """
        Load a new image
        Parameters
        ----------
        arr: numpy.array()
            Must be of type np.uint8 and suitable shape for a PIL Image
        """
        h, w, *_ = arr.shape
        arr = arr.copy()
        arr -= arr.min()
        arr *= 255 / arr.max()
        arr = arr.astype("uint8")

        
        self.layout = {"width":f"{w+20}px", "height":f"{h+20}px"}

        pil = PIL.Image.fromarray(arr)
        f = BytesIO()
        pil.save(f, "png")

        self.out.value=f.getvalue()
        self.out.width=w
        self.out.height=h
        self.out.format="png"