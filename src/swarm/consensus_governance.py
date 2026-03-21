import random

class ConsensusGovernance:
    def __init__(self, agents):
        self.agents = agents
        self.proposals = []
        self.votes = {}

    def propose(self, agent, proposal):
        self.proposals.append(proposal)
        self.votes[proposal] = {}
        for a in self.agents:
            self.votes[proposal][a] = 0

    def vote(self, agent, proposal, vote):
        if proposal in self.proposals:
            self.votes[proposal][agent] = vote

    def tally(self, proposal):
        if proposal in self.proposals:
            total_votes = sum(self.votes[proposal].values())
            if total_votes >= len(self.agents) * 0.51:
                return True
        return False

    def execute(self, proposal):
        if self.tally(proposal):
            # Execute the proposal
            print(f"Proposal '{proposal}' has been executed.")
        else:
            print(f"Proposal '{proposal}' did not reach consensus.")
