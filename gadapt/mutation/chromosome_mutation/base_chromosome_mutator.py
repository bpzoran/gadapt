from typing import List
import gadapt.ga_model.definitions as definitions
class BaseChromosomeMutator:   

    """
    Base class for the mutation of chromosome.
    Mutates specific genes in the chromosome.
    """ 
    
    def mutate(self, c, number_of_mutation_genes: int):
        """
        Mutates genes in the chromosome.
        Args:
            number_of_mutation_genes (int): Number of mutated genes
        """
        self._before_mutated(c)
        self._mutate_chromosome(c, number_of_mutation_genes)
        self._chromosome_mutated(c)
    
    def _mutate_chromosome(self, c, number_of_mutation_genes: int):
        raise Exception(definitions.NOT_IMPLEMENTED)
    
    def _gene_mutated(self, g, c):
        c.mutated_variables_id_list.append(g.genetic_variable.variable_id)        
        
    def _chromosome_mutated(self, c):
        c.is_mutated = True
        if c.first_mutant_generation == 0:
            c.first_mutant_generation += 1
        c.last_mutant_generation = 1

    def _before_mutated(self, c):
        c.mutated_variables_id_list.clear()

