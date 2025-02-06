from enum import Enum

class GPU(str, Enum):
    T4 = "t4"
    L4 = "l4"
    A100 = "a100"
    A100_80GB = "a100-80gb"
    H100 = "h100"
    A10G = "a10g"
    L40S = "l40s"

    