
import polars as pl
from typing import List


class Step:
    def __init__(self, name: str, position: str = None, **kwargs):
        self.name = name
        self.position = position
        self.params = kwargs



class Blueprint:
    _chart = None

    def __init__(self, data: pl.DataFrame, steps: List[Step]):
        pass

    
    def _assemble(step: Step):
        """
        Assemble Step according to position
        """
        if step.position == 'left':
            pass
        elif step.position == 'right':
            pass
        elif step.position == 'top':
            pass
        elif step.position == 'bottom':
            pass
        else:
            raise ValueError(f"Invalid position: {step.position}")
    

    def render(self):
        return