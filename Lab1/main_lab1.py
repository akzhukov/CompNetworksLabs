import numpy as np
import time
from multiprocessing.pool import ThreadPool
import matplotlib.pyplot as plt
from message import MsgQueue
from srp_protocol import receiver as srp_receiver, sender as srp_sender
from gbn_protocol import receiver as gbn_receiver, sender as gbn_sender

timeout = 0.2
max_number = 100
protocols = ["GBN", "SRP"]


def losing_data_test():
    global timeout
    global max_number
    global protocols

    loss_probabilities = np.linspace(0, 0.9, 15)
    window_size = 3

    gbn_time = []
    srp_time = []
    gbn_k = []
    srp_k = []

    for p in loss_probabilities:
        for protocol in protocols:
            pool_sender = ThreadPool(processes=1)
            pool_receiver = ThreadPool(processes=1)
            send_queue = MsgQueue(p)
            receive_queue = MsgQueue(p)
            if protocol == "GBN":
                sender_res = pool_sender.apply_async(gbn_sender, (window_size, max_number, timeout, send_queue, receive_queue))
                receiver_res = pool_receiver.apply_async(gbn_receiver, (window_size, send_queue, receive_queue))
            else:
                sender_res = pool_sender.apply_async(srp_sender, (window_size, max_number, timeout, send_queue, receive_queue))
                receiver_res = pool_receiver.apply_async(srp_receiver, (window_size, send_queue, receive_queue))

            begin_time = time.time()
            sent_msgs = sender_res.get()
            received_msgs = receiver_res.get()
            end_time = time.time()

            k = len(received_msgs) / len(sent_msgs)
            elapsed_time = end_time - begin_time

            if protocol == "GBN":
                gbn_time.append(elapsed_time)
                gbn_k.append(k)
            else:
                srp_time.append(elapsed_time)
                srp_k.append(k)

    fig, ax = plt.subplots()
    ax.plot(loss_probabilities, gbn_k, label="Go-Back-N")
    ax.plot(loss_probabilities, srp_k, label="Selective repeat")
    ax.set_xlabel('вероятность потери пакета')
    ax.set_ylabel('коэф. эффективности')
    ax.legend()
    fig.show()

    fig, ax = plt.subplots()
    ax.plot(loss_probabilities, gbn_time, label="Go-Back-N")
    ax.plot(loss_probabilities, srp_time, label="Selective repeat")
    ax.set_xlabel('вероятность потери пакета')
    ax.set_ylabel('время передачи, с')
    ax.legend()
    fig.show()


def window_size_test():
    global timeout
    global max_number
    global protocols

    window_sizes = range(2, 20)
    loss_probability = 0.1
    send_queue = MsgQueue(loss_probability)
    receive_queue = MsgQueue(loss_probability)

    gbn_time = []
    srp_time = []
    gbn_k = []
    srp_k = []

    for window_size in window_sizes:
        for protocol in protocols:
            pool_sender = ThreadPool(processes=1)
            pool_receiver = ThreadPool(processes=1)
            if protocol == "GBN":
                sender_res = pool_sender.apply_async(gbn_sender, (window_size, max_number, timeout, send_queue, receive_queue))
                receiver_res = pool_receiver.apply_async(gbn_receiver, (window_size, send_queue, receive_queue))
            else:
                sender_res = pool_sender.apply_async(srp_sender, (window_size, max_number, timeout, send_queue, receive_queue))
                receiver_res = pool_receiver.apply_async(srp_receiver, (window_size, send_queue, receive_queue))

            begin_time = time.time()
            sent_msgs = sender_res.get()
            received_msgs = receiver_res.get()
            end_time = time.time()

            k = len(received_msgs) / len(sent_msgs)
            elapsed_time = end_time - begin_time

            if protocol == "GBN":
                gbn_time.append(elapsed_time)
                gbn_k.append(k)
            else:
                srp_time.append(elapsed_time)
                srp_k.append(k)

    fig, ax = plt.subplots()
    ax.plot(window_sizes, gbn_k, label="Go-Back-N")
    ax.plot(window_sizes, srp_k, label="Selective repeat")
    ax.set_xlabel('размер окна')
    ax.set_ylabel('коэф. эффективности')
    ax.legend()
    fig.show()

    fig, ax = plt.subplots()
    ax.plot(window_sizes, gbn_time, label="Go-Back-N")
    ax.plot(window_sizes, srp_time, label="Selective repeat")
    ax.set_xlabel('размер окна')
    ax.set_ylabel('время передачи, с')
    ax.legend()
    fig.show()


if __name__ == '__main__':
    losing_data_test()
    window_size_test()



