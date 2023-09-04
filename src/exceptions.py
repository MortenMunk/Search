class InvalidGridDimension(Exception):
    message = "Grid dimension must be between 3x3 to 10x10"
    pass

class InvalidGridValue(Exception):
    message = "Grid dimension values must be integers"
    pass
