import numpy as np
import time
from threading import Thread
from router import Router
from owner import Owner


owner: Owner = None

cancellation = False
printer_flag = False
blink_conn_arr = []


def router_run(neighbors):
    global owner
    global blink_conn_arr

    conn, index = owner.add_connection()
    router = Router(conn, index)
    router.neighbors = neighbors.copy()
    router.run()

    while True:
        router.process_message()
        if blink_conn_arr[router.index]:
            router.off()
            time.sleep(2)
            router.run()
            blink_conn_arr[router.index] = False
        if cancellation:
            break


def owner_run():
    global owner
    global printer_flag
    owner = Owner()

    while True:
        owner.process_message()
        if printer_flag:
            owner.print_shortest_paths()
            printer_flag = False
        if cancellation:
            break


def stopper():
    global cancellation
    time.sleep(10)
    cancellation = True


def printer():
    global printer_flag
    while True:
        time.sleep(1)
        printer_flag = True
        if cancellation:
            break


def connections_breaker():
    global blink_conn_arr
    time.sleep(2)
    threshold = 0.5
    while True:
        time.sleep(0.01)
        val = np.random.rand()
        if val >= threshold:
            index = np.random.randint(0, len(blink_conn_arr))
            blink_conn_arr[index] = True
            time.sleep(2)
        if cancellation:
            break


def simulate(topology):
    global blink_conn_arr

    nodes = topology["nodes"]
    neighbors = topology["neighbors"]

    owner_thread = Thread(target=owner_run, args=())

    node_threads = [Thread(target=router_run, args=(neighbors[i],)) for i in range(len(nodes))]
    blink_conn_arr = [False for i in range(len(nodes))]

    owner_thread.start()
    for i in range(len(nodes)):
        node_threads[i].start()

    printer_thread = Thread(target=printer, args=())
    conn_breaker_thread = Thread(target=connections_breaker, args=())
    conn_breaker_thread.start()
    printer_thread.start()

    time.sleep(5)
    global cancellation
    cancellation = True
    for i in range(len(nodes)):
        node_threads[i].join()

    owner_thread.join()


def main():
    linear = {
        "nodes": [0, 1, 2, 3, 4],
        "neighbors": [[1], [0, 2], [1, 3], [2, 4], [3]]
    }
    star = {
        "nodes": [0, 1, 2, 3, 4],
        "neighbors": [[2], [2], [0, 1, 3, 4], [2], [2]]
    }
    circle = {
        "nodes": [0, 1, 2, 3, 4],
        "neighbors": [[1], [2], [3], [4], [0]]
    }
    simulate(linear)


if __name__ == '__main__':
    main()

