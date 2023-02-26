import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from colors import colors

def estimate_price(mileage, m_now, b_now):
	return (b_now + (m_now * mileage))


def loss_function(m, b, points):
	total_error = 0
	for i in range(len(points)):
		x = points.iloc[i].km
		y = points.iloc[i].price
		total_error += ((y - (m * x + b)) ** 2)
	return (total_error / float(len(points)))


def gradient_descent(m_now, b_now, data, L):
	m_gradient = 0
	b_gradient = 0

	n = len(data)

	for i in range(n):
		x = data.iloc[i].km
		y = data.iloc[i].price
		# m_gradient += -(2/n) * x * (y - (m_now * x + b_now))
		# b_gradient += -(2/n) * (y - (m_now * x + b_now))
		# b_gradient += np.sum(estimate_price(x, b_now, m_now) - y)
		# m_gradient += np.sum((estimate_price(x, b_now, m_now) - y) * x)
		# b_gradient += L * (1/n) * estimate_price(x, b_now, m_now) - y
		# m_gradient += L * (1/n) * (estimate_price(x, b_now, m_now) - y) * x
		m_gradient = (estimate_price(x, m_now, b_now) - y) * x
		b_gradient = estimate_price(x, m_now, b_now) - y
		m_now -= L * (1 / n) * m_gradient
		b_now -= L * (1 / n) * b_gradient

	# b_gradient /= n;
	# m_gradient /= n;
	# m = m_gradient * L
	# b = b_gradient * L

	return (m_now, b_now)


# minimum step size: 0.001 !!! for m_gradient * L
# maximum number of steps: 1000

def main():
	data = pd.read_csv('data.csv')
	m = 0
	b = 0
	L = 0.1
	epochs = 1000
	while 42:
		try:
			input_mileage = int(input(f"{colors().BLUE}Which mileage do you want to have a price estimation for? {colors().END}"))
			if input_mileage < 0:
				print(f"{colors().RED}Invalid input, please enter a positive integer value!{colors().END}")
				continue
			break
		except:
			print(f"{colors().RED}Invalid input, please enter a positive integer value!{colors().END}")


	########### normalize data start ###########
	print("\nNormalizing data from data.csv...")
	time.sleep(1)
	max_km = data['km'].max()
	max_price = data['price'].max()
	data['km'] /= max_km
	data['price'] /= max_price
	########### normalize data end ###########


	########### training the model start ###########
	print("\nTraining the model...")
	for i in range(1, epochs + 1):
		m, b = gradient_descent(m, b, data, L)
		if (i % 100) == 0:
			print(f"Loss function after {i} of {epochs} epochs returns: ", loss_function(m, b, data))
	
	print(f"{colors().GREEN}Final loss function result after {i} epochs is: ", loss_function(m, b, data), colors().END)
	########### training the model end ###########


	############ denormalize data start ###########
	print("\nDenormalizing data...")
	data['km'] *= max_km
	data['price'] *= max_price
	b *= max_price
	m *= (max_price / max_km)
	############ denormalize data end ###########


	estimate = round(estimate_price(input_mileage, m, b))
	if estimate < 0:
		estimate = 0
	print(f"\n{colors().BLUE}ESTIMATED PRICE: ${estimate}{colors().END}\n")
	plt.scatter(data.km, data.price, color="black")
	# Plot the resulting regression line
	plt.xlabel('mileage')
	plt.ylabel('price')
	plt.plot(
		list(range(0, max_km)), 
		[m * x + b for x in range(0, max_km)], 
		color="green")
	plt.plot(input_mileage, estimate, marker="o", markersize=10, markerfacecolor="lightblue")
	plt.show()


if __name__ == '__main__':
    main()