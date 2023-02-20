import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
		b_gradient += estimate_price(x, m_now, b_now) - y
		m_gradient += (estimate_price(x, m_now, b_now) - y) * x

	b_gradient /= n;
	m_gradient /= n;
	m = m_gradient * L
	b = b_gradient * L

	return (m, b)


def main():
	data = pd.read_csv('data.csv')
	m = 0
	b = 0
	L = 0.0001
	epochs = 100
	print("#Estimate price BEFORE training (500 miles): ", estimate_price(500, m, b))

	########### normalize data start ###########
	max_km = data['km'].max()
	min_km = data['km'].min()
	max_price = data['price'].max()
	min_price = data['price'].min()
	data['km'] = data['km'].astype(float)
	data['price'] = data['price'].astype(float)
	for i in range(len(data)):
		# data.iloc[i, data.columns.get_loc('km')] = data.iloc[i, data.columns.get_loc('km')] / max_km 
		# data.iloc[i, data.columns.get_loc('price')] = data.iloc[i, data.columns.get_loc('price')] / max_price
		data.iloc[i, data.columns.get_loc('km')] = (data.iloc[i, data.columns.get_loc('km')] - min_km) / (max_km - min_km) 
		data.iloc[i, data.columns.get_loc('price')] = (data.iloc[i, data.columns.get_loc('price')] - min_price) / (max_price - min_price) 
	# print(data)
	########### normalize data end ###########


	for i in range(epochs):
		m, b = gradient_descent(m, b, data, L)
		# print(m, b)
	# print("loss function returns: ", loss_function(m, b, data))

	############ DEnormalize data start ###########
	# for i in range(len(data)):
	# 	data.iloc[i, data.columns.get_loc('km')] = (data.iloc[i, data.columns.get_loc('km')] * (max_km - min_km) + min_km)
	# 	data.iloc[i, data.columns.get_loc('price')] = (data.iloc[i, data.columns.get_loc('price')] * (max_price - min_price) + min_price)
	# print(data)
	############ DEnormalize data end ###########


	print("#Estimate price AFTER training (500 miles): ", estimate_price(500, m, b))
	plt.scatter(data.km, data.price, color="black")
	# Plot the resulting regression line
    # x = data["km"]
    # y = (theta1 * x) + theta0 # y = mx + b 
    # plt.plot(x, y, 'r')
    # plt.scatter(data.km, data.price)
	plt.xlabel('mileage')
	plt.ylabel('price')
	plt.plot(
		list(range(0, 2)), 
		[m * x + b for x in range(0, 2)], 
		color="green")

	plt.show()


if __name__ == '__main__':
    main()