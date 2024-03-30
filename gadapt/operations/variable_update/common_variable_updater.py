import statistics as stat
from gadapt.ga_model.genetic_variable import GeneticVariable
import gadapt.utils.ga_utils as ga_utils


class CommonVariableUpdater:
    """
    Common variable updater
    """

    def update_variables(self, population):
        def scale_values(gv: GeneticVariable, values):
            min_val = min(values)
            scaled_values = [(v - min_val) / (gv.max_value - gv.min_value) for v in values]
            return scaled_values

        # def scale_values(data):
        #     min_val = min(data)
        #     max_val = max(data)
        #     scaled_data = [(x - min_val) / (max_val - min_val) for x in data]
        #     return scaled_data
        

        unique_values_per_variables = {}
        values_per_variables = {}
        for c in population:
            if c.is_immigrant:
                continue
            for g in c:
                unique_var_values = unique_values_per_variables.get(
                    g.genetic_variable, None
                )
                var_values = values_per_variables.get(g.genetic_variable, None)
                if unique_var_values is None:
                    unique_var_values = set()
                    unique_values_per_variables[g.genetic_variable] = unique_var_values
                if var_values is None:
                    var_values = []
                    values_per_variables[g.genetic_variable] = var_values
                unique_var_values.add(g.variable_value)
                var_values.append(g.variable_value)
        for key in unique_values_per_variables:
            if len(unique_values_per_variables[key]) == 1:
                key.stacked = True
            else:
                key.stacked = False
        for key in values_per_variables:
            if key.stacked:
                key.cross_diversity_coefficient = 0.0
                continue
            scaled_values = scale_values(key, values_per_variables[key])
            range = max(scaled_values) - min(scaled_values)
            if range == 0:
                key.cross_diversity_coefficient = 0.0
            else:
                #!!!!! Obavezno proveriti koji od ovih nacina koristiti!!!!
                rel_st_dev = stat.stdev(scaled_values) / ga_utils.average(scaled_values)
                key.cross_diversity_coefficient = range / rel_st_dev
                
                # st_dev = stat.stdev(scaled_values)
                # key.cross_diversity_coefficient = range / st_dev

                #rel_st_dev = stat.stdev([v for v in values_per_variables[key]]) / ga_utils.average([v for v in values_per_variables[key]])
                #key.cross_diversity_coefficient = range / rel_st_dev