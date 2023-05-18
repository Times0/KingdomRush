from assets import tower_imgs, tower_icons

items_data = {
    'path': 'assets\\shop',
    'archers long': {'icon': tower_icons[0], 'cost': 500, 'images': tower_imgs[0]},
    'archers short': {'icon': tower_icons[1], 'cost': 750, 'images': tower_imgs[1]},
    'increase speed': {'icon': tower_icons[2], 'cost': 1000, 'images': tower_imgs[2]},
    'increase range': {'icon': tower_icons[3], 'cost': 1500, 'images': tower_imgs[3]},
}

# waves are in form
# number of enemy
# (# ogre, # tbd, # tbd, # tbd)
wave_enemies = ['ogre']
waves = [
    [3],
    [5],
    [7],
    [10, 20],
    [0, 50, 0, 1],
    [0, 100, 0],
    [20, 100, 0],
    [50, 100, 0],
    [100, 100, 0],
    [0, 0, 50, 3],
    [20, 0, 100],
    [20, 0, 150],
    [200, 100, 200],
]
