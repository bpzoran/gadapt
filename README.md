# GAdapt: Self-Adaptive Genetic Algorithm
**GAdapt** (https://gadapt.com) is an open-source Python library for Genetic Algorithm optimization. It implements innovative concepts for the adaptive mutation of genes and chromosomes.

# What innovations does GAdapt bring?
**GAdapt** introduces self-adaptive determination of how many and which chromosomes and genes will be mutated. This determination is based on the diversity of parents, diversity of cost and cross-diversity of genetic variables in the population. Less diversity increases the possibility of mutation. Consequently, it increases the accuracy and the performance of the optimization. Default settings provide a self-adaptive determination of mutation chromosomes and genes.


# Installation
To install [GAdapt], use pip with the following command:

```
pip install gadapt
```

# Source Code
The source code is stored on GitHub at the following address: https://github.com/bpzoran/gadapt

# Getting started
The following example optimizes variable values for a complex trigonometric function.
```python
from gadapt.ga import GA
import math

#trigonometric function definition
def trig_func(args):    
    return math.sqrt(abs(math.cos(args[0]))) + math.pow(math.cos(args[1]), 2) + math.sin(args[2]) + math.pow(args[3], 2) + math.sqrt(args[4]) + math.cos(args[5]) - (args[6]*math.sin(pow(args[6], 3)) + 1) + math.sin(args[0]) / (math.sqrt(args[0])/3 + (args[6]*math.sin(pow(args[6], 3)) + 1) ) / math.sqrt(args[4]) + math.cos(args[5])

#Instantiation of genetic algorithm for desired function
ga = GA(cost_function=trig_func)

#Adding variables (minimal value, maximal value and step)
ga.add(1.0, 4.0, 0.01)
ga.add(37.0, 40.0, 0.01)
ga.add(78.0, 88.0, 0.1)
ga.add(-5.0, 4.0, 0.1)
ga.add(1.0, 100.0, 1)
ga.add(1.0, 4.0, 0.01)
ga.add(-1, -0.01, 0.005)

#Execution of the genetic algorithm
results = ga.execute()

#Printing results
print(results)
```

The possible output:
```
Min cost: -3.370583074871819
Number of iterations: 286
Parameter values:
0: 1.57
1: 39.27
2: 86.4
3: 0.0
4: 1.0
5: 3.14
```

In this example, the genetic algorithm searches for the combination of six parameters, bringing the lowest value for the passed function. The only mandatory attribute to the genetic algorithm is cost_function, and other attributes in this example took default values. Parameters to be optimized are added by the "add" method. There are seven parameters to be optimized in this example.
# Parameter Settings
GAdapt genetic algorithm can receive parameters using constructor, properties, or combined.
Passing parameters through the class constructor:
```python
ga = GA(cost_function=trig_func,
    population_size=32,
    population_mutation="cost_diversity,parent_diversity",
    number_of_mutation_chromosomes=6,
    number_of_mutation_genes=2,
    exit_check="min_cost",
    max_attempt_no=20,
    logging=True,
    timeout=3600)
```
Passing parameters through the class properties:
```python
ga = GA()
ga.cost_function = trig_func
population_size=32
ga.population_mutation="cost_diversity,parent_diversity"
ga.number_of_mutation_chromosomes=6
ga.number_of_mutation_genes=2
ga.exit_check="min_cost"
ga.max_attempt_no=20
ga.logging=True
ga.timeout=3600
```
Passing parameters through the class constructor and properties:
```python
ga = GA(cost_function=trig_func, population_size=32)
ga.population_mutation="cost_diversity,parent_diversity"
ga.number_of_mutation_chromosomes=6
ga.number_of_mutation_genes=2
ga.exit_check="min_cost"
ga.max_attempt_no=20
ga.logging=True
ga.timeout=3600
```
# Parameters description
**cost_function** = *None* - Custom function for the fitness calculation (cost). The optimisation goal is minimising the output of the cost function. *cost_function* must be the function with one argument - a dictionary of values, where the key is an index (the ordinal of adding parameters) and the key is the parameter's value to be optimised. When adding parameters, there should be as many parameters as the function uses. The cost_function is the only mandatory parameter.

**population_size**=*64* - Number of chromosomes in the population.

**exit_check**=*"avg_cost"* - A criteria for the exit for the genetic algorithm.  
Supported values:  
*"avg_cost"* - the optimisation exit is triggered when the average cost of the upper half of the population is not improved in the specified number of generations  
*"min_cost"* - the optimisation exit is triggered when the minimal cost in the population is not improved in the specified number of generations  
*"requested"* - the optimisation exit is triggered when the requested value reached
    
**timeout** = *120* - a number of seconds after which the genetic algorithm optimisation will exit, regardless of whether *exit_check* criteria is reached.

**max_attempt_no**=*10* - this parameter only takes place when *exit_check* has value *"avg_cost"* or *"min_cost"*. It determines the number of generations in which there is no improvement in the average/minimal cost.

**requested_cost**=*sys.float_info.max* - this parameter only takes place when *exit_check* has value *"requested"*. It determines the requested value which causes the exit from the genetic algorithm

**parent_selection**=*"roulette_wheel"* - the algorithm for parent selection.  
Supported values:  
*"roulette_wheel"* - Roulette Wheel selection algorithm (also known as "Weighted random pairing"). The probabilities assigned to the chromosomes in the mating pool are inversely proportional to their cost. A chromosome with the lowest cost has the greatest probability of mating, while the chromosome with the highest cost has the lowest probability of mating.  
*"tournament"* - Tournament selection algorithm. It randomly picks small subsets (groups) of chromosomes from the mating pool, and chromosomes with the lowest cost in subsets become a parent. *"tournament"* can have an additional parameter separated from the *"tournament"* keyword by the comma. The other value represents a group size. For example, *"tournament,8"* means that the tournament parent selection algorithm is chosen, and each group contains up to 8 members. The default group size is 4.  
*"from_top_to_bottom"* - From Top To Bottom selection algorithm starts at the top of the list and pairs the chromosomes two at a time until the top kept chromosomes are selected for mating. Thus, the algorithm pairs odd rows with even rows.  
*"random"* - Random selection algorithm uses a uniform random number generator to select chromosomes.  
    
**percentage_of_mutation_chromosomes** = *10.0* - the percentage of mutated chromosomes in the population. This value is applied to the *population_size* value and rounded to an integer value, giving the number of mutation chromosomes. For example, if *population_size* has a value of 32, and *percentage_of_mutation_chromosomes* has a value of 10, the number of mutation chromosomes will be 3. The calculated value is the upper bound - the actual number of mutated chromosomes can vary from 1 to the calculated value. *percentage_of_mutation_chromosomes* only occurs if *number_of_mutation_chromosomes* does not have a valid integer value equal to or higher than 0.

**number_of_mutation_chromosomes**=*-1* - number of mutation chromosomes in the population. It overrides *percentage_of_mutation_chromosomes*. This value is the upper bound - the actual number of mutated chromosomes can vary from 1 to *number_of_mutation_chromosomes*.

**percentage_of_mutations_genes**=*10* - the percentage of mutated genes in each chromosome. It applies to the chromosome size (number of genes in each chromosome). It rounds to an integer value. This value is an upper bound - the actual number of mutated genes can vary from 1 to the calculated number of mutated genes. *percentage_of_mutations_genes* only occurs if *number_of_mutations_genes* does not have a valid integer value equal to or higher than 0.

**number_of_mutation_genes**=*-1* - number of mutated genes in each chromosome. It overrides *percentage_of_mutations_genes*. This value is an upper bound - the number of mutated genes can vary from 1 to *number_of_mutation_genes*.

**population_mutation**=*"cost_diversity"* - a type of mutation for the entire population. Based on the value of this parameter, the number of mutation chromosomes can be determined, along with how chromosomes for the mutation will be selected.  
Supported values:  
*"cost_diversity"* - the number of mutated chromosomes is determined adaptively by the diversity of costs in the population. Lower cost diversity means a higher number of mutated chromosomes. The minimal value of mutated chromosomes is 0, and the maximal value is determined by the value of *number_of_mutation_chromosomes* or *percentage_of_mutation_chromosomes* parameters. If *population_mutation* has a value other than *"cost_diversity"*, the number of mutation chromosomes is a random value from 1 to *number_of_mutation_chromosomes* value (or to value determined by *percentage_of_mutation_chromosomes* value). *"cost_diversity"* means that the *"parents_diversity"* method is selected to select chromosomes to be mutated. This method only determines the number of mutated chromosomes, but not how chromosomes are selected for the mutation.  
*"parents_diversity"* - chromosomes to be mutated are selected by the diversity of their parents. The more similar parents (lower parents diversity) mean a higher probability of mutation for the child. Based on the calculated parent diversity, chromosomes may be selected by one of the selection methods, which is determined by the value of the *parent_diversity_mutation_chromosome_selection* parameter.  
*random* - chromosomes to be mutated are selected randomly.  

Population_mutation may have more values, separated by a comma. It means that more than one method can be chosen for the mutation of chromosomes in the population. For example, *"cost_diversity,parents_diversity"* means that number of mutation chromosomes will be determined by the cost diversity and the selection of chromosomes to be mutated will be defined by parent diversity. *"cost_diversity,parents_diversity"* and *"cost_diversity"* return the same logic for the determination of mutation number and the way how chromosomes are to be selected. *"cost_diversity,random"* means that the cost diversity will determine the number of mutation chromosomes, and the selection of chromosomes to be mutated will be chosen randomly.
    
**parent_diversity_mutation_chromosome_selection**=*"roulette_wheel"* - the selection algorithm for mutating chromosomes when *population_mutation* contains value *"parents_diversity"*. It only applies when *population_mutation* has value *"cost_diversity"*. It determines the way how chromosomes are to be selected based on the diversity of their parents.  
Supported values:  
*"roulette_wheel"* - Roulette Wheel selection algorithm (also known as "Weighted random pairing"). The probabilities assigned to the chromosomes to be mutated are proportional to their similarity (inversely proportional to their diversity). A chromosome with the lowest parent diversity has the greatest probability of mutation, while the chromosome with the highest parent diversity has the lowest probability of mutation.  
*"tournament"* - Tournament selection algorithm. It randomly picks small subsets (groups) of chromosomes, and chromosomes with the lowest parent diversity (highest parent similarity) in subsets are chosen to be mutated. *"tournament"* can have an additional parameter separated from the *"tournament"* keyword by the comma. The other value represents a group size. For example, *"tournament,8"* means that the tournament mutation selection algorithm is chosen, and each group contains up to 8 members. The default group size is 4.  
*"from_top_to_bottom"* - From Top To Bottom selection algorithm starts at the top of the list and selects chromosomes for mutation.  
*"random"* - Random selection algorithm uses a uniform random number generator to select chromosomes for mutation. In this case, selection for mutation will not depend on parent diversity.  
    
**must_mutate_for_same_parents**=*True* - indicates if completely the same parents must influence mutation for their children. In other words, each child will be mutated if it has parents with a diversity value of 0. If *must_mutate_for_same_parents* has the value True, the number of mutated chromosomes can outreach value determined by *number_of_mutation_chromosomes* or *percentage_of_mutation_chromosomes*

**chromosome_mutation**=*"cross_diversity"* - the type of mutation of genes in chromosomes.  
Supported values:  
*"cross_diversity"* - considers the diversity of genes of the same type in the population. Lower diversity can mean that this genetic variable approaches some local minimums, and therefore such genes increase the chance for mutation. Based on the calculated cross-diversity, chromosomes may be selected by one of the selection methods, which is determined by the value of the *cross_diversity_mutation_gene_selection* parameter.  
*"random"* - genes are randomly selected for the mutation  
**cross_diversity_mutation_gene_selection**=*"roulette_wheel"* - the selection algorithm for mutating chromosomes when *chromosome_mutation* has value *"cross_diversity"*. It only applies when *chromosome_mutation* has value *"cross_diversity"* . It determines the way how genes are to be selected based on the cross-diversity.  
Supported values:  
*"roulette_wheel"* - Roulette Wheel selection algorithm (also known as "Weighted random pairing"). The probabilities assigned to the genes to be mutated are inversely proportional to their cross-diversity. A gene with the lowest cross-diversity has the greatest probability of mutation, while the gene with the highest cross-diversity has the lowest probability of mutation.  
*"tournament"* - Tournament selection algorithm. It randomly picks small subsets (groups) of genes, and genes with the lowest cross-diversity in subsets are chosen to be mutated. *"tournament"* can have an additional parameter separated from the *"tournament"* keyword by the comma. The other value represents a group size. For example, *"tournament,3"* means that the tournament mutation selection algorithm is chosen, and each group contains up to 3 members. The default group size is 4.  
*"from_top_to_bottom"* - From Top To Bottom selection algorithm starts at the top of the list and selects genes for mutation.  
*"random"* - Random selection algorithm uses a uniform random number generator to select genes for mutation. In this case, selection for the mutation will not depend on gene cross-diversity.  
    
**immigration_number**=*0* - Refers to the "Random Immigrants" concepts. This strategy introduces a certain number of individuals into the population during the evolution process. These new individuals are generated randomly and injected into the population.

**logging** = *False* - if this parameter has a True value, the log file will be created in the current working directory. The log file contains the flow of genetic algorithm execution, along with values of chromosomes, genes and cost functions in each generation