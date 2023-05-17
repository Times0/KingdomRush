import os

import pygame


def import_folder(path):
    """returns a list of all the images in the folder"""

    surface_list = []

    for (dir_path, dir_names, filenames) in os.walk(path):
        for name in filenames:
            image_path = os.path.join(path, name)
            image_surface = pygame.image.load(os.path.join(image_path))
            surface_list.append(image_surface)

    return surface_list


def import_animations(path):
    """returns a dictionary of all the animation states and frames"""

    animations = {}

    for dir_name in os.listdir(path):
        animations[dir_name] = import_folder(os.path.join(path, dir_name))

    return animations
