class MutationValidator:
    TIER_CONSTRAINTS = {
        0: {"type": "parameter", "difficulty": "Easy"},
        1: {"type": "skill", "difficulty": "Medium"},
        2: {"type": "architecture", "difficulty": "Medium"},
        3: {"type": "architecture", "difficulty": "Hard"}
    }

    def __init__(self, tier):
        if tier not in self.TIER_CONSTRAINTS:
            raise ValueError("Invalid tier: {}. Valid tiers are 0-3.".format(tier))
        self.tier = tier
        self.constraints = self.TIER_CONSTRAINTS[tier]

    def validate_mutation(self, mutation_type, difficulty_level):
        if (mutation_type != self.constraints["type"] or 
            difficulty_level != self.constraints["difficulty"]):
            raise ValueError(
                "Mutation type '{}' with difficulty '{}' is not allowed for tier {}.".format(
                    mutation_type, difficulty_level, self.tier
                )
            )
        return True

    def get_constraints(self):
        return self.constraints
