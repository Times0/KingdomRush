from assets import tower_imgs

towers_data = {
    'path': 'assets\\shop',
    'archers lvl 1': ['buy_archer.png', 500, tower_imgs[0], [1000, 2000]],
    'archers lvl 2': ['buy_archer_2.png', 750, tower_imgs[1], [1500, 2500]],
    'increase damage': ['buy_damage.png', 1000, tower_imgs[2], [2000]],
    'increase range': ['buy_range.png', 1500, tower_imgs[3], [3000]],
}

# waves are in form
# number of enemy
# (# ogre, # tbd, # tbd, # tbd)
wave_enemies = ['ogre']
waves = [
    [3],
    [50],
    [100],
    [0, 20],
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
