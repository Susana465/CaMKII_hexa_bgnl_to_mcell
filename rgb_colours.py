import matplotlib.colors as mcolors
import numpy as np

def rgb_to_name(r, g, b):
    # Normalize input RGB values from 0-255 to 0-1 range
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    # List of all named colors in matplotlib
    named_colors = mcolors.CSS4_COLORS
    
    # Function to calculate Euclidean distance between two RGB values
    def distance(c1, c2):
        return np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)
    
    # Find the closest color
    closest_color_name = min(named_colors, key=lambda name: distance(mcolors.hex2color(named_colors[name]), (r, g, b)))
    
    return closest_color_name

# Example RGB values
r, g, b = 116, 40, 129  # Your input color
color_name = rgb_to_name(r, g, b)
print(f"The closest named color is: {color_name}")
