# visuals.py

import pygame

_BLACK = (0, 0, 0)
_GRAY = (200, 200, 200)

class ImageAsset():

    def __init__(self, image: 'pygames image', width: float, height: float, location: tuple[float,float]):

        self._image = image
        self._width = width
        self._height = height
        self._location = location


    def get_image(self)->'pygames image':
        return self._image

    def get_width(self)->float:
        return self._width

    def get_heigth(self)->float:
        return self._height

    def get_location(self)->tuple[float,float]:
        return self._location

    def set_location(self, new_location: tuple[float,float])->None:
        self._location = new_location

   
