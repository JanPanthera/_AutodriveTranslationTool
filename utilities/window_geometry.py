
def save_window_geometry(window_geometry):
    size_part, pos_x, pos_y = window_geometry.split('+')
    width, height = size_part.split('x')
    save_setting("WindowGeometry", "width", width)
    save_setting("WindowGeometry", "height", height)
    save_setting("WindowGeometry", "pos_x", pos_x)
    save_setting("WindowGeometry", "pos_y", pos_y)

def load_window_geometry():
    width = load_setting("WindowGeometry", "width", default_value="800")
    height = load_setting("WindowGeometry", "height", default_value="600")
    pos_x = load_setting("WindowGeometry", "pos_x", default_value="100")
    pos_y = load_setting("WindowGeometry", "pos_y", default_value="100")
    return f"{width}x{height}+{pos_x}+{pos_y}"
