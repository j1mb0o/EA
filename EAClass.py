class EvolutionaryStrategy:
    def __init__(self, mu, dimension, upperbound=1.0, lowerbound=0.0):
        np.random.seed(42)
        self.mu = mu
        self.dimension = dimension
        self.upperbound = upperbound
        self.lowerbound = lowerbound

    def initialize(self):
        parent = []
        parent_sigma = []
        for i in range(self.mu):
            parent.append(
                np.random.uniform(low=self.lowerbound, high=self.upperbound, size=self.dimension)
            )
            parent_sigma.append(0.05 * (self.upperbound - self.lowerbound))

        return parent, parent_sigma

    def one_sigma_mutation(self, parent, parent_sigma, tau):
        for i in range(len(parent)):
            parent_sigma[i] = parent_sigma[i] * np.exp(np.random.normal(0, tau))
            for j in range(len(parent[i])):
                parent[i][j] = parent[i][j] + np.random.normal(0, parent_sigma[i])
                parent[i][j] = parent[i][j] if parent[i][j] < 1.0 else 1.0
                parent[i][j] = parent[i][j] if parent[i][j] > 0.0 else 0.0

    def individual_sigma_mutation(self, parent, parent_sigma, tau_globla, tau_local):
        g = np.random.normal(0, 1)
        for i in range(len(parent)):
            parent_sigma[i] = parent_sigma[i] * np.exp(
                tau_globla * g + tau_local * np.random.normal(0, 1)
            )
            for j in range(len(parent[i])):
                parent[i][j] = parent[i][j] + np.random.normal(0, parent_sigma[i])
                parent[i][j] = parent[i][j] if parent[i][j] < 1.0 else 1.0
                parent[i][j] = parent[i][j] if parent[i][j] > 0.0 else 0.0

    def encode(self, x):
        return [1 if i >= 0.5 else 0 for i in x]

    def recombination(self, parent, parent_sigma, recombination_type="discreet"):
        # Discreet recombination
        if recombination_type == "discreet":
            [p1, p2] = np.random.choice(len(parent), 2, replace=False)
            choice = np.random.randint(2, size=len(parent[0]))
            offspring = np.where(choice == 0, parent[p1], parent[p2])
            sigma = np.where(choice == 0, parent_sigma[p1], parent_sigma[p2])
            sigma = sigma.mean()

        elif recombination_type == "intermediate":
            [p1, p2] = np.random.choice(len(parent), 2, replace=False)
            offspring = (parent[p1] + parent[p2]) / 2
            sigma = (parent_sigma[p1] + parent_sigma[p2]) / 2

        elif recombination_type == "globlal_discrete":
            choice = np.random.randint(len(parent), size=len(parent[0]))
            offspring = np.array([parent[choice[i]][i] for i in range(len(parent[0]))])
            sigma = np.array(
                [parent_sigma[choice[i]] for i in range(len(parent[0]))]
            ).mean()

        # global intermediate recombination
        else:
            offspring = np.average(parent, axis=0)
            sigma = np.array(parent_sigma).mean()

        return offspring, sigma
