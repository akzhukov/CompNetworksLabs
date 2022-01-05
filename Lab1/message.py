import numpy as np
import enum


class MessageStatus(enum.Enum):
    OK = enum.auto()
    LOST = enum.auto()


class Message:
    number = -1
    real_number = -1
    data = ""
    status = MessageStatus.OK

    def __init__(self):
        pass

    def copy(self):
        msg = Message()
        msg.number = self.number
        msg.data = self.data
        msg.status = self.status

    def __str__(self):
        return f"({self.real_number}({self.number}), {self.data}, {self.status})"


class MsgQueue:
    def __init__(self, loss_probability):
        self.msg_queue = []
        self.loss_probability = loss_probability
        pass

    def is_empty(self):
        return len(self.msg_queue) == 0

    def next(self):
        result = None
        if not  self.is_empty():
            result = self.msg_queue[0]
            self.msg_queue.pop(0)
        return result

    def send(self, msg):
        self.msg_queue.append(self.emulate_loss(msg))

    def emulate_loss(self, msg):
        if np.random.rand() <= self.loss_probability:
            msg.status = MessageStatus.LOST
        return msg