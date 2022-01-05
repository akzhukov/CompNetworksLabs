import time
from message import Message, MessageStatus


def sender(window_size, max_number, timeout, send_queue, receive_queue):
    msgs = []
    curr_number = 0
    last_ans_number = -1
    begin_time = time.time()
    while last_ans_number < max_number:
        expected_number = (last_ans_number + 1) % window_size

        msg = receive_queue.next()
        if msg is not None:
            if msg.number == expected_number:
                last_ans_number += 1
                begin_time = time.time()
            else:
                curr_number = last_ans_number + 1

        if time.time() - begin_time > timeout:
            curr_number = last_ans_number + 1
            begin_time = time.time()

        if (curr_number < last_ans_number + window_size) and (curr_number <= max_number):
            k = curr_number % window_size
            msg = Message()
            msg.number = k
            msg.real_number = curr_number
            send_queue.send(msg)
            msgs.append(f"{curr_number}({k})")
            curr_number += 1
        pass

    msg = Message()
    msg.data = "STOP"
    send_queue.send(msg)
    return msgs


def receiver(window_size, send_queue, receive_queue):
    msgs = []
    expected_number = 0
    while True:
        msg = send_queue.next()
        if msg is not None:
            if msg.data == "STOP":
                break

            if msg.status == MessageStatus.LOST:
                continue

            if msg.number == expected_number:
                ans = Message()
                ans.number = msg.number
                receive_queue.send(ans)

                msgs.append(f"{msg.real_number}({msg.number})")
                expected_number = (expected_number + 1) % window_size
            else:
                continue
    return msgs
