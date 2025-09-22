# app/models/__init__.py
from .student import student
from .time import time
from .course import course

# Optional: expose them in __all__ for cleaner imports
__all__ = ["student", "time", "course"]
