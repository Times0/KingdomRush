import ctypes

ctypes.windll.user32.SetProcessDPIAware()  # Make sure the window is not scaled by windows (DPI) happens on laptops
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

FPS = 60
