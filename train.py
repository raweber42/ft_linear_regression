import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
from colors import colors


def estimate_price(mileage, m_now, b_now):
	return (b_now + (m_now * mileage))


# def loss_function(m, b, points):
# 	total_error = 0
# 	for i in range(len(points)):
# 		x = points.iloc[i].km
# 		y = points.iloc[i].price
# 		total_error += ((y - (m * x + b)) ** 2)
# 	return (total_error / float(len(points)))


def gradient_descent(m_now, b_now, data, L):
	m_gradient = 0
	b_gradient = 0

	n = len(data)

	for i in range(n):
		x = data.iloc[i].km
		y = data.iloc[i].price
		m_gradient = (estimate_price(x, m_now, b_now) - y) * x
		b_gradient = estimate_price(x, m_now, b_now) - y
		m_now -= L * (1 / n) * m_gradient
		b_now -= L * (1 / n) * b_gradient

	return (m_now, b_now)


def main():
	try:
		data = pd.read_csv('data.csv')
	except:
		print(f"{colors().RED}Error: could not read file{colors().END}")
		exit()
	m = 0
	b = 0
	L = 0.1
	epochs = 1000
	

	########### normalize data start ###########
	print("\nNormalizing data from data.csv...")
	time.sleep(1)
	max_km = data['km'].max()
	max_price = data['price'].max()
	min_km = data['km'].min()
	min_price = data['price'].min()
	data['km'] /= max_km
	data['price'] /= max_price
	########### normalize data end ###########


	########### prepare animation/graph start ###########
	fig, ax = plt.subplots()
	x_max = max_km
	ax.set_xlim(min_km, max_km)
	ax.set_ylim(min_price, max_price)
	ax.set_xlim(0, x_max)
	ax.set_ylim(0, 10000)
	ax.set_xlabel('mileage')
	ax.set_ylabel('price')
	ax.grid()
	
	line, = ax.plot([], [], 'red')
	animation_store = []
	########### prepare animation/graph end ###########


	########### training the model start ###########
	print("\nTraining the model...")
	for i in range(1, epochs + 1):
		if (i % 50) == 0:
			animation_store.append([m, b])
		m, b = gradient_descent(m, b, data, L)
		# if (i % 100) == 0:
		# 	print(f"Loss function after {i} of {epochs} epochs returns: ", loss_function(m, b, data))
	# print(f"{colors().GREEN}Final loss function result after {i} epochs is: ", loss_function(m, b, data), colors().END)
	animation_store.append([m, b])
	########### training the model end ###########
	

	########### export m & b as thetas start ###########
	file = open('theta.py', 'w')
	theta_content = "theta0 = " + str((b * max_price)) + "\r\n" + "theta1 = " + str((m * max_price / max_km)) + "\r\n"
	file.write(theta_content)
	file.close()
	########### export m & b as thetas end ###########


	############ denormalize data start ###########
	print("\nDenormalizing data...")
	data['km'] *= max_km
	data['price'] *= max_price
	b *= max_price
	m *= (max_price / max_km)
	############ denormalize data end ###########


	######### animation helper start#########
	def animate(n):
		line.set_data(list(range(0, max_km)), [(animation_store[n][0] * (max_price / max_km) ) * x + (animation_store[n][1] * max_price ) for x in range(0, max_km)])
	######### animation helper end#########
	

	plt.scatter(data.km, data.price, color="black")
	anim = animation.FuncAnimation(fig, animate, frames=len(animation_store), interval=20, repeat=False)
	plt.show()


if __name__ == '__main__':
    main()