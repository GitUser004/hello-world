from time import sleep
from threading import Thread
from matplotlib import pyplot as plt
from multiprocessing import Process


def show():
    print("show start ")
    fig  = plt.figure(1)
    plt.plot([1,2,3])
    plt.show()
    print("show end")
    print("1")
    # plt.close()
    print("2")



def close():
    print("close start")
    sleep(2)
    plt.close('all')
    print("close end")

# thread1 = Thread(target=close, args=(2,))
thread2 = Thread(target=show,name="showThread")
print('-------------')
# thread1.start()
thread2.start()

close()
print("end")

# show()