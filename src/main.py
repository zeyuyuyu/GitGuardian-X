!import random!
!import time!
!import networkx as nx!

class AgentNode:
    def __init__(self, id):
        self.id = id
        self.neighbors = set()
        self.state = 'UNDECIDED'
        self.decision = None

    def connect(self, other_node):
        self.neighbors.add(other_node)
        other_node.neighbors.add(self)

    def broadcast(self, message):
        for neighbor in self.neighbors:
            neighbor.receive(message)

    def receive(self, message):
        if message['type'] == 'PROPOSE':
            self.state = 'PROPOSED'
            self.decision = message['value']
            self.broadcast({'type': 'PROPOSE', 'value': self.decision})
        elif message['type'] == 'ACCEPT':
            if self.state == 'PROPOSED' and self.decision == message['value']:
                self.state = 'ACCEPTED'
                self.broadcast({'type': 'ACCEPT', 'value': self.decision})
        elif message['type'] == 'REJECT':
            if self.state == 'PROPOSED' and self.decision == message['value']:
                self.state = 'REJECTED'
                self.broadcast({'type': 'REJECT', 'value': self.decision})

class DistributedConsensus:
    def __init__(self, num_agents):
        self.agents = [AgentNode(i) for i in range(num_agents)]
        self.create_connections()

    def create_connections(self):
        for i in range(len(self.agents)):
            for j in range(i+1, len(self.agents)):
                if random.random() < 0.5:
                    self.agents[i].connect(self.agents[j])

    def run(self):
        for agent in self.agents:
            if agent.state == 'UNDECIDED':
                agent.broadcast({'type': 'PROPOSE', 'value': random.randint(0, 100)})

        while True:
            time.sleep(0.1)
            all_accepted = True
            for agent in self.agents:
                if agent.state != 'ACCEPTED':
                    all_accepted = False
                    break
            if all_accepted:
                break

        print(f'Consensus reached on value: {agent.decision}')

if __name__ == '__main__':
    consensus = DistributedConsensus(10)
    consensus.run()