import math
import random
from abc import ABC, abstractmethod
from typing import Tuple, List

from gadapt.ga_model.allele import Allele
from gadapt.ga_model.chromosome import Chromosome
from gadapt.operations.chromosome_update.base_chromosome_updater import (
    BaseChromosomeUpdater,
)
from gadapt.operations.crossover.base_crossover_probability_determinator import BaseCrossoverProbabilityDeterminator
from gadapt.operations.mutation.chromosome_mutation.base_gene_mutation_selector import BaseGeneMutationSelector


class BaseCrossover(ABC):
    """Base Crossover Class"""

    def __init__(self, chromosome_updater: BaseChromosomeUpdater, mutator: BaseGeneMutationSelector, crossover_rate_determinator: BaseCrossoverProbabilityDeterminator):
        self._current_gene_number = -1
        self._chromosome_updater = chromosome_updater
        self._mutator = mutator
        self.crossover_rate_determinator: BaseCrossoverProbabilityDeterminator = crossover_rate_determinator

    def _mate_pair_until_added(self, population, chromosome1, chromosome2 ) -> None:
        chromosomes_added = False
        number_of_added_chromosomes = 0

        new_offsprings = []
        number_of_attempts = 0
        while (not chromosomes_added) and number_of_attempts < 15:
            number_of_attempts += 1
            offsprings_to_add = []
            if len(new_offsprings) == 0:
                new_offsprings.extend(list(self._mate_pair(
                    chromosome1, chromosome2, population
                )))
            if number_of_added_chromosomes == 0:
                offsprings_to_add.extend(new_offsprings)
                new_offsprings.clear()
            elif number_of_added_chromosomes == 1:
                offsprings_to_add.append(new_offsprings.pop())
            else:
                return
            if number_of_attempts > 5:
                for c in offsprings_to_add:
                    self._mutator.mutate(c, number_of_attempts - 5)
            number_of_added_chromosomes += population.add_not_contained_chromosomes(offsprings_to_add)
            offsprings_to_add.clear()
            if number_of_added_chromosomes >= 2:
                chromosomes_added = True
        if number_of_added_chromosomes < 2:
            new_offsprings = self._mate_pair(
                chromosome1, chromosome2, population.population_generation
            )
            for i in range(number_of_added_chromosomes, 2):
                population.add_chromosome(new_offsprings[i])

    def mate(self, chromosome_pairs: List[Tuple[Chromosome, Chromosome]], population):
        """
        Returns list of chromosome pairs using parents' genetic material

        Args:
            chromosome_pairs (List[Tuple[Chromosome, Chromosome]]) : List of chromosome pairs for mating
            population: Population
        """
        for chromosome1, chromosome2 in chromosome_pairs:
            if population.options.ensure_unique_individuals:
                self._mate_pair_until_added(population, chromosome1, chromosome2)
            else:
                self._mate_pair(chromosome1, chromosome2, population)

        current_len = len(population)
        chromosome_surplus = current_len - population.options.population_size
        if chromosome_surplus > 0:
            sorted_by_cost_value = sorted(
                population, key=lambda chrom: chrom.cost_value, reverse=True
            )
            i = 0
            for c in sorted_by_cost_value:
                if i >= chromosome_surplus:
                    break
                if not math.isnan(c.cost_value):
                    population.chromosomes.remove(c)

    def _mate_pair(
        self, mother: Chromosome, father: Chromosome, population
    ):
        """Returns two offspring chromosomes using parents' genetic material

        Args:
            mother (Chromosome): The first chromosome for mating
            father (Chromosome): The second chromosome for mating
            population: Population

        Returns:
            Chromosome: the first offspring chromosome
            Chromosome: the second offspring chromosome
        """
        if len(mother) != len(father):
            raise Exception("Mother and father must have the same number of genes!")
        self._mother = mother
        self._father = father
        self._offspring1 = Chromosome(population.population_generation)
        self._offspring2 = Chromosome(population.population_generation)
        c_o_p = self._get_crossover_probability(population)
        crossed = self._cross_genetic_material(c_o_p)
        while not crossed:
            c_o_p += 0.1
            c_o_p = min(c_o_p, 1.0)
            self._offspring1 = Chromosome(population.population_generation)
            self._offspring2 = Chromosome(population.population_generation)
            crossed = self._cross_genetic_material(c_o_p)

        self._offspring1.mother_id = self._mother.chromosome_id
        self._offspring2.mother_id = self._mother.chromosome_id
        self._offspring1.father_id = self._father.chromosome_id
        self._offspring2.father_id = self._father.chromosome_id
        self._all_genes_crossed()
        self._increase_generation()

        return self._offspring1, self._offspring2

    def _cros_genetic_variables(self, crossover_probability: float):
        self._mother_allele, self._father_allele = self._get_mother_father_allele()
        gene_father = self._mother_allele.gene
        gene_mother = self._father_allele.gene
        if gene_father != gene_mother:
            gene_mother = next(
                (item.gene for item in self._mother if item.gene == gene_father),
                None,
            )
        if gene_mother is None:
            raise Exception(
                "chromosomes in crossover do not have the same structure!"
            )
        self._gene_crossed()
        random_value = random.random()
        are_variables_crossed = False
        if random_value <= crossover_probability:
            var1, var2 = self._combine()
            are_variables_crossed = True
        else:
            var1, var2 = self._mother_allele.variable_value, self._father_allele.variable_value,
        self._offspring1.add_gene(gene_father, var1)
        self._offspring2.add_gene(gene_father, var2)
        return are_variables_crossed

    def _cross_genetic_material(self, crossover_prob: float):
        self._chromosome_updater.chromosome_start_update()
        number_of_genes = len(self._father)
        are_variables_crossed = False
        for self._current_gene_number in range(number_of_genes):
            are_variables_crossed = self._cros_genetic_variables(crossover_prob) or are_variables_crossed
        return are_variables_crossed


    def _get_mother_father_allele(self) -> Tuple[Allele, Allele]:
        if self._current_gene_number == -1:
            raise Exception("_current_gene_number not set")
        father_allele = self._father[self._current_gene_number]
        mother_allele = self._mother[self._current_gene_number]
        return mother_allele, father_allele

    @abstractmethod
    def _combine(self):
        pass

    def _get_crossover_probability(self, population) -> float:
        return self.crossover_rate_determinator.get_crossover_probability(population)

    def _increase_generation(self):
        current_generation = self._mother.chromosome_generation
        if (
            current_generation == 0
            or current_generation < self._father.chromosome_generation
        ):
            current_generation = self._father.chromosome_generation
        current_generation += 1
        self._offspring1.chromosome_generation = current_generation
        self._offspring2.chromosome_generation = current_generation

        current_generation = 0
        if (
            self._mother.first_mutant_generation > 0
            or self._father.first_mutant_generation > 0
        ):
            current_generation = self._mother.first_mutant_generation
            if (
                current_generation == 0
                or self._father.first_mutant_generation > current_generation
            ):
                current_generation = self._father.first_mutant_generation
            current_generation += 1
        self._offspring1.first_mutant_generation = current_generation
        self._offspring2.first_mutant_generation = current_generation

        current_generation = 0
        if (
            self._mother.last_mutant_generation > 0
            or self._father.last_mutant_generation > 0
        ):
            current_generation = self._mother.last_mutant_generation
            if current_generation == 0 or (
                0 < self._father.last_mutant_generation < current_generation
            ):
                current_generation = self._father.last_mutant_generation
            current_generation += 1
        self._offspring1.last_mutant_generation = current_generation
        self._offspring2.last_mutant_generation = current_generation

        current_generation = 0
        if (
            self._mother.first_immigrant_generation > 0
            or self._father.first_immigrant_generation > 0
        ):
            current_generation = self._mother.first_immigrant_generation
            if (
                current_generation == 0
                or self._father.first_immigrant_generation > current_generation
            ):
                current_generation = self._father.first_immigrant_generation
            current_generation += 1
        self._offspring1.first_immigrant_generation = current_generation
        self._offspring2.first_immigrant_generation = current_generation

        current_generation = 0
        if (
            self._mother.last_immigrant_generation > 0
            or self._father.last_immigrant_generation > 0
        ):
            current_generation = self._mother.last_immigrant_generation
            if current_generation == 0 or (
                0 < self._father.last_immigrant_generation < current_generation
            ):
                current_generation = self._father.last_immigrant_generation
            current_generation += 1
        self._offspring1.last_immigrant_generation = current_generation
        self._offspring2.last_immigrant_generation = current_generation

    def _gene_crossed(self):
        self._chromosome_updater.chromosome_prepare_update(
            mother_gene=self._mother_allele, father_gene=self._father_allele
        )

    def _all_genes_crossed(self):
        self._chromosome_updater.chromosome_update(
            offspring1=self._offspring1, offspring2=self._offspring2, father=self._father, mother=self._mother
        )
