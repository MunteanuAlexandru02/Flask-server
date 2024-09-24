"""Tried to use enums to get rid of string constants, not as good as C enums :("""
from enum import Enum

class REPLIES(Enum):
    """Class used for enums"""
    STATES_MEAN = "states_mean"
    STATE_MEAN = "state_mean"
    BEST5 = "best5"
    WORST5 = "worst5"
