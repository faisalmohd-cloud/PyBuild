from enum import Enum


class ProjectType(str, Enum):
    EXECUTABLE = "exe"
    LIBRARY = "lib"