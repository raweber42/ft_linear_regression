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
	mse_array = []
	while 42:
		try:
			input_mileage = int(input(f"{colors().BLUE}Which mileage do you want to have a price estimation for? {colors().END}"))
			if input_mileage < 0 or input_mileage > 1000000:
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
		temp_mse = loss_function(m, b, data)
		mse_array.append(temp_mse)
		if (i % 100) == 0:
			print(f"Mean squared error after {i} of {epochs} epochs is: ", temp_mse)
		
	print(f"{colors().GREEN}Final mean squared error value after {i} epochs is: ", temp_mse, colors().END)
	########### training the model end ###########


	############ denormalize data start ###########
	print("\nDenormalizing data...")
	data['km'] *= max_km
	data['price'] *= max_price
	b *= max_price
	m *= (max_price / max_km)
	############ denormalize data end ###########


	plt.xlabel('epochs')
	plt.ylabel('mean sqared error')
	plt.plot(np.array(mse_array), color="red")
	plt.show()


if __name__ == '__main__':
    main()