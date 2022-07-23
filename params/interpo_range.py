"""
----

Interpolation Range
===================

``InterpoRange``
----------------

Provides interpolated values in a given year range.

----
"""
from abc import ABC, abstractmethod

from pydantic import PositiveInt

from dash_models import DashListable
from .interpo import Constant, InterpoSelect


class ABCInterpoRange(ABC):
    """
    Allow an object to provide a value at given year.
    """

    @abstractmethod
    def at(self, year: int) -> float:
        """ Get value at given year. """
        ...


class InterpoRange(DashListable, ABCInterpoRange):
    start_year: PositiveInt = 2020
    end_year: PositiveInt = 2050
    interpo: InterpoSelect = InterpoSelect(__root__=Constant(value=0.0))

    @property
    def title(self) -> str:
        return f'{self.start_year}-{self.end_year} ({self.interpo.selected})'

    def at(self, year: int) -> float:
        return self.interpo.__root__.at(self.start_year, self.end_year, year)