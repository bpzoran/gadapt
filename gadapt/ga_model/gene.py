"""
Gene
"""
import math
import sys

import numpy

import gadapt.ga_model.definitions as definitions


class Gene:
    def __init__(self, id: int) -> None:
        """
        Gene class defines variable to be optimized.
        Each allele has a reference to one gene.
        Gene contains common values for optimized variables and alleles: variable id, maximal\
            value, minimal value, step.
        Args:
            id (int): identifier of the gene
        """
        self._max_value = sys.float_info.min
        self._decimal_places = -1
        self._stacked = False
        self.variable_id = id
        self._standard_deviation = definitions.FLOAT_NAN
        self._initial_st_dev = -1.0
        self._step = None

    def __eq__(self, other):
        if not isinstance(other, Gene):
            return False
        return self.variable_id == other.variable_id

    def __hash__(self) -> int:
        return self.variable_id

    @property
    def variable_id(self) -> int:
        """
        Unique ID for the gene
        """
        return self._variable_id

    @variable_id.setter
    def variable_id(self, value: int):
        self._variable_id = value

    @property
    def max_value(self) -> float:
        """
        Max gene value
        """
        return self._max_value

    @max_value.setter
    def max_value(self, value: float):
        self._max_value = value

    @property
    def min_value(self) -> float:
        """
        Min gene value
        """
        return self._min_value

    @min_value.setter
    def min_value(self, value: float):
        self._min_value = value

    @property
    def step(self) -> float:
        """
        Optimization step
        """
        return self._step

    @step.setter
    def step(self, value: float):
        self._step = value
        if value is not None:
            self._decimal_places = self._get_decimal_places(value)

    def _get_decimal_places(self, num):
        num_str = str(num)
        if "e-" in num_str:
            num_str = num_str.split("e-")[-1]
            return int(num_str)
        if "." in num_str:
            _, fractional_part = num_str.split(".")
            return len(fractional_part)
        else:
            return 0

    @property
    def decimal_places(self) -> int:
        """
        Number of decimal places of the gene value
        """
        return self._decimal_places

    @property
    def stacked(self) -> bool:
        """
        Indicates if all alleles have the same value for the same gene
        """
        return self._stacked

    @stacked.setter
    def stacked(self, value: bool):
        self._stacked = value

    @property
    def columnar_diversity_coefficient(self) -> float:
        """
        Relative standard deviation of all alleles for the same gene
        """
        return self._standard_deviation

    @columnar_diversity_coefficient.setter
    def columnar_diversity_coefficient(self, value: float):
        self._standard_deviation = value

    def make_random_value(self):
        """
        Makes random value, based on min value, max value, and step.
        If step is None or <= 0, returns a continuous random float in [min_value, max_value].
        """
        if self.step is not None and self.step > 0 and (not math.isnan(self.step)):
            gene_range = self.max_value - self.min_value
            # Guard against extremely small steps that would create too many discrete values
            if gene_range / self.step > 1e9:
                # Step is too small relative to range — treat as continuous
                return numpy.random.uniform(low=self.min_value, high=self.max_value)
            # Discrete case: pick a random step multiple within bounds
            max_steps = int(gene_range / self.step)
            random_step = numpy.random.randint(0, max_steps + 1)
            value = self.min_value + random_step * self.step
            return round(min(value, self.max_value), self.decimal_places)
        else:
            # Continuous case: any float in [min_value, max_value]
            return numpy.random.uniform(low=self.min_value,
                                        high=self.max_value)

    @property
    def initial_st_dev(self) -> float:
        return self._initial_st_dev

    @initial_st_dev.setter
    def initial_st_dev(self, value: float):
        self._initial_st_dev = value
