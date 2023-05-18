import os
import pygame
from load_assets import import_animations, import_folder

assets_folder = 'assets'

# General assets
star_img = pygame.image.load(os.path.join(assets_folder, 'ui\\star.png'))

# Buttons:
pause_img = pygame.image.load(os.path.join(assets_folder, 'ui\\button_pause.png'))
start_img = pygame.image.load(os.path.join(assets_folder, 'ui\\button_start.png'))
sound_on = pygame.image.load(os.path.join(assets_folder, 'ui\\button_sound.png'))
sound_off = pygame.image.load(os.path.join(assets_folder, 'ui\\button_sound_off.png'))

# Enemies
scorpion_animations = import_animations(os.path.join(assets_folder, 'enemies\\enemy_1'), .5)
wizard_animations = import_animations(os.path.join(assets_folder, 'enemies\\enemy_2'), .3)
ogre_animations = import_animations(os.path.join(assets_folder, 'enemies\\enemy_3'), .5)
armored_ogre_animations = import_animations(os.path.join(assets_folder, 'enemies\\enemy_5'), .5)
pekka_animations = import_animations(os.path.join(assets_folder, 'enemies\\enemy_8'), .5)

# Towers
# Tower images
archer_1_imgs = import_folder(os.path.join(assets_folder, 'towers\\archer_1'))
archer_2_imgs = import_folder(os.path.join(assets_folder, 'towers\\archer_2'))
damage_imgs = import_folder(os.path.join(assets_folder, 'towers\\damage'))
range_imgs = import_folder(os.path.join(assets_folder, 'towers\\range'))
tower_imgs = [archer_1_imgs, archer_2_imgs, damage_imgs, range_imgs]

# Tower icons:
archer_icon = pygame.image.load(os.path.join(assets_folder, 'shop\\buy_archer.png'))
archer_2_icon = pygame.image.load(os.path.join(assets_folder, 'shop\\buy_archer_2.png'))
damage_icon = pygame.image.load(os.path.join(assets_folder, 'shop\\buy_damage.png'))
range_icon = pygame.image.load(os.path.join(assets_folder, 'shop\\buy_range.png'))
tower_icons = [archer_icon, archer_2_icon, damage_icon, range_icon]

# Tower top animation
archer_animations = import_animations(os.path.join(assets_folder, 'towers\\archer_top'))
