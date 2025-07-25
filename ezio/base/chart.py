

import altair as alt
import polars as pl
from typing import Dict

from abc import abstractmethod

class BaseChart:
    _chart: alt.Chart = None
    _components: Dict = {}

    def __init__(self, *args, **kargs):
        self._components =  self._build_components()


    @property
    def components(self):
        return self._components
    
    @abstractmethod
    def _build_components(self) -> alt.Chart:
        """
        Abstract method to be implemented by subclasses to define the core rendering logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def assemble(self, components: Dict, width: int, height: int) -> alt.Chart:
        raise NotImplementedError('assemble method not implemented')

    def render(self, width: int = 500, height: int = 300) -> alt.Chart:
        self._chart =  self.assemble(components=self._components, height=height, width=width)
        return self._chart
    