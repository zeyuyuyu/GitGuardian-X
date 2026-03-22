import random

class ConsensusGovernance:
    def __init__(self, swarm_size):
        self.swarm_size = swarm_size
        self.voter_pool = [i for i in range(swarm_size)]
        self.proposals = []
        self.vote_tallies = {}

    def submit_proposal(self, proposal):
        self.proposals.append(proposal)
        self.vote_tallies[proposal] = [0, 0] # [for, against]

    def cast_vote(self, agent_id, proposal, is_affirmative):
        if agent_id not in self.voter_pool:
            return False
        if proposal not in self.proposals:
            return False
        if is_affirmative:
            self.vote_tallies[proposal][0] += 1
        else:
            self.vote_tallies[proposal][1] += 1
        self.voter_pool.remove(agent_id)
        return True

    def tally_votes(self, proposal):
        if proposal not in self.proposals:
            return None
        for_votes, against_votes = self.vote_tallies[proposal]
        total_votes = for_votes + against_votes
        if total_votes >= self.swarm_size * 0.51:  # Majority rule
            return for_votes > against_votes
        else:
            return None # Quorum not reached

    def select_random_voters(self, num_voters):
        return random.sample(self.voter_pool, num_voters)
