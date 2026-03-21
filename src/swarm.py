import numpy as np
from typing import List, Tuple, Optional

class SwarmAgent:
    def __init__(self, position: np.ndarray, velocity: np.ndarray):
        self.position = position
        self.velocity = velocity
        self.best_position = position.copy()
        self.best_fitness = float('-inf')

class AdaptiveSwarm:
    def __init__(self,
                 n_agents: int,
                 dimensions: int,
                 bounds: Tuple[float, float],
                 inertia_weight: float = 0.7,
                 cognitive_weight: float = 1.5,
                 social_weight: float = 1.5,
                 adaptive_params: bool = True):
        self.n_agents = n_agents
        self.dimensions = dimensions
        self.bounds = bounds
        self.w = inertia_weight
        self.c1 = cognitive_weight
        self.c2 = social_weight
        self.adaptive_params = adaptive_params
        
        # Initialize agents
        self.agents: List[SwarmAgent] = []
        self._initialize_swarm()
        
        self.global_best_position = None
        self.global_best_fitness = float('-inf')
        
    def _initialize_swarm(self) -> None:
        for _ in range(self.n_agents):
            position = np.random.uniform(self.bounds[0], self.bounds[1], self.dimensions)
            velocity = np.random.uniform(-1, 1, self.dimensions)
            self.agents.append(SwarmAgent(position, velocity))
            
    def _adapt_parameters(self, iteration: int, max_iterations: int) -> None:
        if self.adaptive_params:
            # Linearly decrease inertia weight
            self.w = 0.9 - 0.5 * (iteration / max_iterations)
            
            # Adjust cognitive and social weights
            progress = iteration / max_iterations
            self.c1 = 2.5 - 2 * progress  # Decrease cognitive weight
            self.c2 = 0.5 + 2 * progress  # Increase social weight
            
    def _update_agent(self, agent: SwarmAgent) -> None:
        r1, r2 = np.random.rand(2)
        
        # Update velocity
        cognitive_component = self.c1 * r1 * (agent.best_position - agent.position)
        social_component = self.c2 * r2 * (self.global_best_position - agent.position)
        
        agent.velocity = (self.w * agent.velocity + 
                         cognitive_component + 
                         social_component)
        
        # Update position
        agent.position += agent.velocity
        
        # Bound position
        agent.position = np.clip(agent.position, self.bounds[0], self.bounds[1])
        
    def optimize(self, fitness_func, max_iterations: int) -> Tuple[np.ndarray, float]:
        for iteration in range(max_iterations):
            self._adapt_parameters(iteration, max_iterations)
            
            for agent in self.agents:
                # Evaluate fitness
                current_fitness = fitness_func(agent.position)
                
                # Update personal best
                if current_fitness > agent.best_fitness:
                    agent.best_fitness = current_fitness
                    agent.best_position = agent.position.copy()
                    
                    # Update global best
                    if current_fitness > self.global_best_fitness:
                        self.global_best_fitness = current_fitness
                        self.global_best_position = agent.position.copy()
                        
                # Update agent's position and velocity
                self._update_agent(agent)
                
        return self.global_best_position, self.global_best_fitness
    
    def get_swarm_state(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Returns current positions and velocities of all agents"""
        return [(agent.position.copy(), agent.velocity.copy()) for agent in self.agents]
