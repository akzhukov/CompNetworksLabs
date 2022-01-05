import enum
import time
from message import Message, MessageStatus


class WindowMsgStatus(enum.Enum):
    BUSY = enum.auto()
    NEED_REPEAT = enum.auto()
    CAN_BE_USED = enum.auto()


class WindowNode:
    def __init__(self, number):
        self.status = WindowMsgStatus.NEED_REPEAT
        self.time = 0
        self.number = number
        pass

    def __str__(self):
        return f"( {self.number}, {self.status}, {self.time})"


def sender(window_size, max_number, timeout, send_queue, receive_queue):
    msgs = []
    wnd_nodes = [WindowNode(i) for i in range(window_size)]

    msg_count = 0

    while msg_count < max_number:

        res_str = "["
        for i in range(window_size):
            res_str += wnd_nodes[i].__str__()
        res_str += "]"

        msg = receive_queue.next()
        if msg is not None:
            msg_count += 1
            wnd_nodes[msg.number].status = WindowMsgStatus.CAN_BE_USED

        curr_time = time.time()
        for i in range(window_size):
            if wnd_nodes[i].number > max_number:
                continue

            send_time = wnd_nodes[i].time
            if curr_time - send_time > timeout:
                wnd_nodes[i].status = WindowMsgStatus.NEED_REPEAT

        for i in range(window_size):
            if wnd_nodes[i].number > max_number:
                continue

            if wnd_nodes[i].status == WindowMsgStatus.BUSY:
                continue

            elif wnd_nodes[i].status == WindowMsgStatus.NEED_REPEAT:

                wnd_nodes[i].status = WindowMsgStatus.BUSY
                wnd_nodes[i].time = time.time()

                msg = Message()
                msg.number = i
                msg.real_number = wnd_nodes[i].number
                send_queue.send(msg)
                msgs.append(f"{msg.real_number}({msg.number})")

            elif wnd_nodes[i].status == WindowMsgStatus.CAN_BE_USED:
                wnd_nodes[i].status = WindowMsgStatus.BUSY
                wnd_nodes[i].time = time.time()
                wnd_nodes[i].number = wnd_nodes[i].number + window_size

                if wnd_nodes[i].number > max_number:
                    continue

                msg = Message()
                msg.number = i
                msg.real_number = wnd_nodes[i].number
                send_queue.send(msg)
                msgs.append(f"{msg.real_number}({msg.number})")

    msg = Message()
    msg.data = "STOP"
    send_queue.send(msg)
    return msgs


def receiver(window_size, send_queue, receive_queue):
    msgs = []
    while True:
        curr_msg = send_queue.next()
        if curr_msg is not None:
            if curr_msg.data == "STOP":
                break

            if curr_msg.status == MessageStatus.LOST:
                continue

            ans = Message()
            ans.number = curr_msg.number
            receive_queue.send(ans)
            msgs.append(f"{curr_msg.real_number}({curr_msg.number})")
    return msgs
