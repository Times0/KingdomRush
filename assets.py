import os
import pygame
from load_assets import import_animations, import_folder

assets_folder = 'assets'

# General assets
star_img = pygame.image.load(os.path.join(assets_folder, 'shop\\star.png'))

# Enemies
ogre_animations = import_animations(os.path.join(assets_folder, 'enemies\\enemy_1'))

# Towers
# Tower images
archer_1_imgs = import_folder(os.path.join(assets_folder, 'towers\\archer_1'))
archer_2_imgs = import_folder(os.path.join(assets_folder, 'towers\\archer_2'))
damage_imgs = import_folder(os.path.join(assets_folder, 'towers\\damage'))
range_imgs = import_folder(os.path.join(assets_folder, 'towers\\range'))
tower_imgs = [archer_1_imgs, archer_2_imgs, damage_imgs, range_imgs]
# Tower top animation
archer_animations = import_animations(os.path.join(assets_folder, 'towers\\archer_top'))
