import json
import matplotlib.pyplot as plt

def get_stored_username():
	"""如果存储了用户名，就获取它"""
	filename = 'username.json'
	try:
		with open(filename) as f_obj:
			username = json.load(f_obj)
	except FileNotFoundError:
		return None
	else:
		return username

username=get_stored_username()
print(username)


print("\n\n\n\n\n\n\n\n")


input_value = [1,2,3,4,5]
squares = [x**2 for x in input_value]
#plt.plot(input_value, squares, linewidth = 5,c="yellow")
plt.plot(input_value,squares,linewidth = 5,c="yellow")
plt.title("square Numbers", fontsize=20)
plt.xlabel("value", fontsize = 14)
plt.ylabel("aquares of value", fontsize=14)
plt.tick_params(axis="both", labelsize = 14)

plt.show()

plt.scatter(2,4,s=500,c=(0,0,0.5))
plt.title("square Numbers", fontsize=20)
plt.xlabel("value", fontsize = 14)
plt.ylabel("aquares of value", fontsize=14)
plt.tick_params(axis="both", labelsize = 14)

plt.show()

x=[1,2,3,4,5]
y=[value**2 for value in x]
plt.scatter(x,y,s=500,edgecolor="red", c="blue")
plt.title("square Numbers", fontsize=20)
plt.xlabel("value", fontsize = 14)
plt.ylabel("aquares of value", fontsize=14)
plt.tick_params(axis="both", labelsize = 14)

plt.show()

x = list(range(1000))
y=[value**2 for value in x]
plt.scatter(x,y,s=10,edgecolor="none")
plt.title("square Numbers", fontsize=20)
plt.xlabel("value", fontsize = 14)
plt.ylabel("aquares of value", fontsize=14)
plt.tick_params(axis="both", labelsize = 14)
plt.axis([0,1100,0,1100000])

plt.show()

x = list(range(-100,100))
y=[value**2 for value in x]
plt.scatter(x,y,s=10,c=y, cmap=plt.cm.Greens,edgecolor="none")
plt.title("square Numbers", fontsize=20)
plt.xlabel("value", fontsize = 14)
plt.ylabel("aquares of value", fontsize=14)
plt.tick_params(axis="both", labelsize = 14)

plt.show()
