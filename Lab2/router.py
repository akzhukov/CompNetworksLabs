from message import Message, MsgType, Connection
from topology import Topology


class Router:
    def __init__(self, conn, index):
        self.owner_connection = conn
        self.topology = Topology()
        self.shortest_paths = None
        self.index = index
        self.neighbors = []

    def print_shortest_paths(self):
        print(f"{self.index}: {self.topology.get_shortest_ways(self.index)}\n", end="")

    def send_neighbors(self):
        msg = Message(MsgType.NEIGHBORS)
        msg.data = self.neighbors.copy()
        self.owner_connection.send_from_owner_message(msg)

    def get_topology(self):
        msg = Message(MsgType.GET_TOPOLOGY)
        self.owner_connection.send_from_owner_message(msg)

    def run(self):
        self.send_neighbors()
        self.get_topology()

    def off(self):
        msg = Message(MsgType.NODE_REMOVE)
        self.owner_connection.send_from_owner_message(msg)

    def add_node(self, index, neighbors):
        self.topology.add_node(index)
        for j in neighbors:
            self.topology.add_link(index, j)

        if index in self.neighbors:
            if index not in self.topology.topology[self.index]:
                msg = Message(MsgType.NEIGHBORS)
                msg.data = [index]
                self.owner_connection.send_from_owner_message(msg)

    def delete_node(self, index):
        self.topology.delete_node(index)

    def process_message(self):
        input_msg = self.owner_connection.get_from_owner_message()

        if input_msg is None:
            return

        print(f"router({self.index}) : {input_msg}\n", end="")

        if input_msg.type == MsgType.NEIGHBORS:
            self.add_node(input_msg.data["index"], input_msg.data["neighbors"])
        elif input_msg.type == MsgType.UPDATE_TOPOLOGY:
            self.topology = input_msg.data
        elif input_msg.type == MsgType.NODE_REMOVE:
            self.delete_node(input_msg.data)
        elif input_msg.type == MsgType.PRINT_PATHS:
            self.print_shortest_paths()
