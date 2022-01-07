from message import Message, MsgType, Connection
from topology import Topology


class Owner:
    def __init__(self):
        self.connections = []
        self.topology = Topology()

    def add_connection(self):
        new_connection = Connection()
        new_index = len(self.connections)
        self.connections.append(new_connection)
        return new_connection, new_index

    def add_node(self, index, neighbors):
        self.topology.add_node(index)
        for j in neighbors:
            self.topology.add_link(index, j)

    def delete_node(self, index):
        self.topology.delete_node(index)

    def send_all_exclude_one(self, exclude_index,  msg):
        for conn_ind in range(len(self.connections)):
            conn = self.connections[conn_ind]
            if conn is None:
                continue
            if conn_ind == exclude_index:
                continue
            conn.send_to_owner_message(msg)

    def process_msg_neighbors(self, conn_ind, input_msg):
        self.add_node(conn_ind, input_msg.data)

        msg = Message(MsgType.NEIGHBORS)
        msg.data = {
            "index": conn_ind,
            "neighbors": input_msg.data
            }

        self.send_all_exclude_one(conn_ind, msg)

    def process_msg_node_remove(self, conn_ind):
        self.delete_node(conn_ind)

        msg = Message(MsgType.NODE_REMOVE)
        msg.data = conn_ind

        self.send_all_exclude_one(conn_ind, msg)

    def print_shortest_paths(self):
        msg = Message(MsgType.PRINT_PATHS)
        for conn in self.connections:
            conn.send_to_owner_message(msg)

    def process_message(self):
        for conn_ind in range(len(self.connections)):
            conn = self.connections[conn_ind]
            if conn is None:
                continue

            input_msg = conn.get_to_owner_message()

            if input_msg is None:
                continue

            print(f"Owner received message from router({conn_ind}): {input_msg}\n", end="")

            if input_msg.type == MsgType.NEIGHBORS:
                self.process_msg_neighbors(conn_ind, input_msg)
            elif input_msg.type == MsgType.GET_TOPOLOGY:
                msg = Message(MsgType.UPDATE_TOPOLOGY)
                msg.data = self.topology.copy()
                conn.send_to_owner_message(msg)
            elif input_msg.type == MsgType.NODE_REMOVE:
                self.process_msg_node_remove(conn_ind)

