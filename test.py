from multiprocessing import Process
from threading import Thread
import time


def counter(c=360, start=0):
    while start < c:
        start += 1
        time.sleep(1)


def run_script():
    c = 0
    while True:
        c += 1
        if c == 5:
            print('exit!!!')
            exit(1)
        print("Running!")
        time.sleep(0.5)


def main():
    thr = Thread(target=counter)
    main_thr = Thread(target=run_script)
    thr.start()
    main_thr.start()
    while True:
        if not thr.is_alive() or not main_thr.is_alive():
            print("restarting!")
            thr = Thread(target=counter)
            main_thr = Process(target=run_script)
            thr.start()
            main_thr.start()
        time.sleep(4)


if __name__ == '__main__':
    main()