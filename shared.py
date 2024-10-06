import pandas as pd

def parse_to_int(value: str) -> int:
    if value == 'x':
        return 1
    elif value == 'o':
        return -1
    elif value == 'b':
        return 0
    elif value == 'x_win':
        return 2
    elif value == 'o_win':
        return -2
    elif value == 'in_progress':
        return 3  
    elif value == 'draw':
        return 4  
    else:
        raise ValueError(f"Invalid value: {value}")

def parse_to_str(value: int) -> str:
    if value == 1:
        return 'x'
    elif value == -1:
        return 'o'
    elif value == 0:
        return 'b'
    elif value == 2:
        return 'x_win'
    elif value == -2:
        return 'o_win'
    elif value == 3:
        return 'in_progress'
    elif value == 4:
        return 'draw'
    else:
        raise ValueError(f"Invalid value: {value}")
    
def parse_line(line:str) -> pd.Series:
    return pd.Series([parse_to_int(value) for value in line])