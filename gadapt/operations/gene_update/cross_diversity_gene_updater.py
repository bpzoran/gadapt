import math
import statistics as stat

from gadapt.operations.gene_update.base_gene_updater import BaseGeneUpdater


class ColumnarDiversityGeneUpdater(BaseGeneUpdater):
    """
    Calculates columnar diversity using Logarithmic Scaling to preserve
    sensitivity throughout the convergence curve.
    """

    def _update_genes(self):
        # 1. Group values by Gene
        values_per_variables = {}
        for c in self.population:
            if c.is_immigrant:
                continue
            for g in c:
                if g.gene not in values_per_variables:
                    values_per_variables[g.gene] = []
                values_per_variables[g.gene].append(g.variable_value)

        # 2. Process each Gene
        for g, values in values_per_variables.items():
            # Check if population is identical for this gene
            if len(set(values)) <= 1:
                g.stacked = True
                g.columnar_diversity_coefficient = 0.0
                continue

            g.stacked = False

            # 3. Logarithmic Transformation
            # Shift values by min_value and add 1.0 to ensure values are > 0 for log
            # This measures variety relative to the gene's search space range
            log_values = []
            for v in values:
                # Distance from min_value + 1.0 (to avoid log(0))
                shifted_v = (v - g.min_value) + 1.0
                log_values.append(math.log(shifted_v))

            # 4. Calculate Logarithmic Standard Deviation
            current_log_stdev = stat.stdev(log_values)

            # 5. Capture Benchmark (Initial Log Diversity)
            if g.initial_st_dev < 0:
                # We reuse your existing attribute name for convenience
                g.initial_st_dev = current_log_stdev

            # 6. Normalize to 0-1 range
            if g.initial_st_dev == 0:
                g.columnar_diversity_coefficient = 0.0
            else:
                # Ratio of current log-spread to initial log-spread
                normalized_div = current_log_stdev / g.initial_st_dev
                g.columnar_diversity_coefficient = max(0.0, min(1.0, normalized_div))