from gadapt.ga import GA
import math

#trigonometric function definition
def trig_func(args):
    return math.sqrt(abs(math.cos(args[0]))) + math.pow(math.cos(args[1]), 2) + math.sin(args[2]) + math.pow(args[3], 2) + math.sqrt(args[4]) + math.cos(args[5]) - (args[6]*math.sin(pow(args[6], 3)) + 1) + math.sin(args[0]) / (math.sqrt(args[0])/3 + (args[6]*math.sin(pow(args[6], 3)) + 1) ) / math.sqrt(args[4]) + math.cos(args[5])

#Instantiation of genetic algorithm for desired function
ga = GA(cost_function=trig_func,
        population_size=64,
                    population_mutation="cost_diversity, cross_diversity, parent_diversity, random",
                    chromosome_mutation="cross_diversity",
                    gene_mutation="cross_diversity,cost_diversity,random",
                    percentage_of_mutation_chromosomes=60,
                    percentage_of_mutation_genes=20,
                    exit_check="min_cost",
                    keep_elitism_percentage=50,
                    max_attempt_no=20,
                    number_of_generations=600,
                    parent_selection="roulette_wheel",
                    immigration_number=1,
                    crossover_probability=0.5,
                    crossover="blending",
                    ensure_unique_individuals=False,
                    logging=False)

#Adding variables (minimal value, maximal value and step)
ga.add(1.0, 4.0)
ga.add(37.0, 40.0)
ga.add(78.0, 88.0)
ga.add(-5.0, 4.0)
ga.add(1.0, 100.0)
ga.add(1.0, 4.0)
ga.add(-1, -0.01)

#Execution of the genetic algorithm
results = ga.execute()

#Printing results
print(results)