# Parameter Optimization for the Traveling Salesman Problem Using a Heuristic Algorithm

Pamukkale University, Department of Industrial Engineering — IENG435 Heuristic Methods in Problem Solving term project.

**Prepared by:** Dilara Şahbaz
**Instructor:** Prof. Dr. Can Berk Kalaycı
**Term:** Spring, 2024-2025

## Project Summary

This project uses a full factorial experimental design to examine the effect of algorithm parameters (population size, number of iterations, elitism rate, crossover rate, mutation rate) on solution quality when solving the Traveling Salesman Problem (TSP) with a genetic algorithm. The study consists of two phases: a pilot study to determine the population size and number of iterations, followed by the main experiment in which the elitism, crossover, and mutation rates are tested.

## Folder Contents

- `kod.py` — Main genetic algorithm and full factorial experiment code. On the Berlin52 dataset, it tries all combinations of elitism, crossover, and mutation rates with 10 different seeds and writes the results to Excel.
- `pilot_calisma.py` — Pilot study code. It tries combinations of different population sizes (30, 40, 50) and numbers of iterations (10,000, 50,000, 100,000).
- `heuristic_project`.pdf` (Turkish: `Sezgisel_proje`) — Project report (method, experimental design, results).

## Method

The algorithm uses a standard genetic algorithm framework:

- **Initial population:** Random permutations
- **Crossover operators:** OX (order crossover), edge recombination, ANX (alternating/neighbor-based)
- **Mutation operators:** exchange, inversion, scramble, displacement, insert
- **Selection:** Ranking by fitness + elitism

The operator is chosen randomly in each generation; the type of crossover/mutation to be applied is determined by a random number.

### Tested Parameters (Main Experiment)

| Parameter | Values |
|---|---|
| Population size | 30 |
| Number of iterations | 1e5 |
| Elitism rate (ER) | 0.1, 0.2, 0.3 |
| Crossover rate (CR) | 0.5, 0.7, 0.9 |
| Mutation rate (MR) | 0.01, 0.05, 0.1 |
| Seed | 0-9 (10 replications) |
| Time limit | 60 seconds/run |

### Conclusion

Across the tested datasets, including Berlin52, with the population size fixed at 30 and the number of iterations fixed at 1e5, the combination of elitism rate 0.1, crossover rate 0.5, and mutation rate 0.01 generally gave the best results. Detailed tables and comparisons can be found in `heuristic_project.pdf` (Turkish: `Sezgisel_proje.pdf`).
