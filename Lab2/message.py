import enum


class MsgType(enum.Enum):
    NEIGHBORS = enum.auto()
    GET_TOPOLOGY = enum.auto()
    UPDATE_TOPOLOGY = enum.auto()
    NODE_REMOVE = enum.auto()
    PRINT_PATHS = enum.auto()


class Message:
    def __init__(self, type):
        self.data = None
        self.type = type

    def __str__(self):
        return f"({self.type}: {self.data})"


class Connection:
    def __init__(self):
        self.from_owner_queue = []
        self.to_owner_queue = []

    def __str__(self):
        return f"(->:{self.from_owner_queue}\n<-:{self.to_owner_queue})"

    @staticmethod
    def __get_message(queue, ):
        if len(queue) > 0:
            result = queue[0]
            queue.pop(0)
            return result
        return None

    def get_from_owner_message(self):
        return self.__get_message(self.from_owner_queue)

    def get_to_owner_message(self):
        return self.__get_message(self.to_owner_queue)

    def send_from_owner_message(self, msg):
        self.to_owner_queue.append(msg)

    def send_to_owner_message(self, msg):
        self.from_owner_queue.append(msg)
