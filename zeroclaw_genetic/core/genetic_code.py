# GeneticCode dataclass

from dataclasses import dataclass

@dataclass
class GeneticCode:
    tier: int
    traits: dict
    fitness: float
    mutation_rate: float
  
    def __post_init__(self):
        # Ensure tier is within valid range
        if self.tier < 0 or self.tier > 3:
            raise ValueError('Tier must be between 0 and 3')
        
    def mutate(self):
        # Logic for mutation
        pass

    def evaluate_fitness(self):
        # Fitness evaluation logic
        pass