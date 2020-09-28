from multiprocessing import Process, Pipe
from os import getpid


def local_time(counter):
    return '\tcounter = {}'.format(counter)


def calc_recv_timestamp(recv_time_stamp, counter):
    for id in range(len(counter)):
        counter[id] = max(recv_time_stamp[id], counter[id])
    return counter


# EVENTS
def event_a(pid, counter):
    counter[0] += 1
    print('Event {}'.format(pid) + local_time(counter))
    return counter


def event_b(pid, counter):
    counter[1] += 1
    print('Event {}'.format(pid) + local_time(counter))
    return counter


def event_c(pid, counter):
    counter[2] += 1
    print('Event {}'.format(pid) + local_time(counter))
    return counter


# SEND MESSAGE
def send_message_a(pipe, pid, counter):
    counter[0] += 1
    pipe.send(('', counter))
    print('Send ' + str(pid) + local_time(counter))
    return counter


def send_message_b(pipe, pid, counter):
    counter[1] += 1
    pipe.send(('', counter))
    print('Send ' + str(pid) + local_time(counter))
    return counter


def send_message_c(pipe, pid, counter):
    counter[2] += 1
    pipe.send(('', counter))
    print('Send ' + str(pid) + local_time(counter))
    return counter


def recv_message_a(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    counter[0] += 1
    print('Recv ' + str(pid) + local_time(counter))
    return counter


def recv_message_b(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    counter[1] += 1
    print('Recv ' + str(pid) + local_time(counter))
    return counter


def recv_message_c(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    counter[2] += 1
    print('Recv ' + str(pid) + local_time(counter))
    return counter


# PROCESSES
def process_a(pipe12):
    pid = getpid()
    counter = [0, 0, 0]
    counter = send_message_a(pipe12, pid, counter)  # a0
    counter = send_message_a(pipe12, pid, counter)  # a1
    counter = event_a(pid, counter)  # a2
    counter = recv_message_a(pipe12, pid, counter)  # a3
    counter = event_a(pid, counter)  # a4
    counter = event_a(pid, counter)  # a5
    counter = recv_message_a(pipe12, pid, counter)  # a6
    print(pid, counter)


def process_b(pipe21, pipe23):
    pid = getpid()
    counter = [0, 0, 0]
    counter = recv_message_b(pipe21, pid, counter)  # b0
    counter = recv_message_b(pipe21, pid, counter)  # b1
    counter = send_message_b(pipe21, pid, counter)  # b2
    counter = recv_message_b(pipe23, pid, counter)  # b3
    counter = event_b(pid, counter)  # b4
    counter = send_message_b(pipe21, pid, counter)  # b5
    counter = send_message_b(pipe23, pid, counter)  # b6
    counter = send_message_b(pipe23, pid, counter)  # b7
    print(pid, counter)


def process_c(pipe32):
    pid = getpid()
    counter = [0, 0, 0]
    counter = send_message_c(pipe32, pid, counter)  # c0
    counter = recv_message_c(pipe32, pid, counter)  # c1
    counter = event_c(pid, counter)  # c2
    counter = recv_message_c(pipe32, pid, counter)  # c3
    print(pid, counter)


if __name__ == '__main__':
    pipe12, pipe21 = Pipe()
    pipe23, pipe32 = Pipe()

    a = Process(target=process_a, args=(pipe12,))
    b = Process(target=process_b, args=(pipe21, pipe23))
    c = Process(target=process_c, args=(pipe32,))

    a.start()
    b.start()
    c.start()

    a.join()
    b.join()
    c.join()
