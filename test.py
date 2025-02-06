zoom_size = ("10", "10")


if (not isinstance(zoom_size, tuple) or len(zoom_size) != 2) or not all(isinstance(v, (int, float)) and v >= 0 for v in zoom_size):
    raise ValueError(f"zoom_size must be a tuple of length two with positive numbers. Received: {zoom_size} with type {type(zoom_size)}")