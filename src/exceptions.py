class InvalidGridDimension(Exception):
    message = "Grid dimension must be between 3x3 to 10x10"
    pass

class InvalidGridValue(Exception):
    message = "Grid dimension values must be integers"
    pass

class MazeNeedsStartAndGoal(Exception):
    message = "Maze must contain a start and a goal"
    pass

class MazeIllegalChar(Exception):
    message = "Maze can only contain A, B, 1's, and 0's"
    pass

class TooManyLinesInFile(Exception):
    message = "Your file has too many lines"
    pass

class NotEnoughLinesInFile(Exception):
    message = "Not enough lines in file"
    pass