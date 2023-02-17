import pandas as pd
import matplotlib.pyplot as plt

def estimate_price(mileage, theta0, theta1):
	return (theta0 + (theta1 * mileage))


def loss_function(m, b, points):
	total_error = 0
	for i in range(len(points)):
		x = points.iloc[i].km
		y = points.iloc[i].price
		total_error += ((y - (m * x + b)) ** 2)
	return (total_error / float(len(points)))


def gradient_descent(m_now, b_now, points, L):
	m_gradient = 0
	b_gradient = 0

	n = len(points)

	for i in range(n):
		x = points.iloc[i].km
		y = points.iloc[i].price
		# m_gradient += -(2/n) * x * (y - (m_now * x + b_now))
		# b_gradient += -(2/n) * (y - (m_now * x + b_now))
		b_gradient += estimate_price(x, b_now, m_now) - y
		m_gradient += (estimate_price(x, b_now, m_now) - y) * x

	b_gradient /= n;
	m_gradient /= n;
	m = m_gradient * L
	b = b_gradient * L

	return (m, b)


def main():
	data = pd.read_csv('data.csv')
	m = 0
	b = 1000
	L = 0.0000001
	epochs = 10

	print("#Estimate price BEFORE training (500 miles): ", estimate_price(500, b, m))

	for i in range(epochs):
		m, b = gradient_descent(m, b, data, L)
		print(m, b)

	print("m, b: ", m, b)
	print("#Estimate price AFTER training (500 miles): ", estimate_price(500, b, m))
	




	# print(m, b)
	# plt.scatter(data.km, data.price, color="black")
	# plt.plot(
	# 	list(range(20, 250000)), 
	# 	[m * x + b for x in range(20, 250000)], 
	# 	color="green")
	# # data.km, 
	# # 	data.price, 
	# plt.show()


if __name__ == '__main__':
    main()