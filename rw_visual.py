import matplotlib.pyplot as plt
from random_walk import RandomWalk

while True:
    rw = RandomWalk(50000)
    rw.fill_walk()
    
    plt.figure(figsize=(10,6))
    poing_numbers = list(range(rw.num_points))
    plt.scatter(rw.x_value, rw.y_value, s = 1,c = poing_numbers,cmap=plt.cm.Blues,edgecolor="none")
    #plt.plot(rw.x_value,rw.y_value,linewidth=1)
    plt.scatter(rw.x_value[0],rw.y_value[0],c = "green", edgecolor = "none", s = 100)
    plt.scatter(rw.x_value[-1],rw.y_value[-1],c = "red", edgecolor = "none", s = 100)

    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)

    plt.show()

    keep_running = input("make another walk?(y/n): ")
    if keep_running == 'n':
        break

