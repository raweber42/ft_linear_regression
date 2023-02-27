import sys
from colors import colors
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def main():
	try:
		import theta
		theta1 = theta.theta1
		theta0 = theta.theta0
	except:
		theta1 = 0
		theta0 = 0

	while 42:
		try:
			input_mileage = int(input(f"{colors().BLUE}Which mileage do you want to have a price estimation for? {colors().END}"))
			if input_mileage < 0 or input_mileage > 1000000:
				print(f"{colors().RED}Invalid input, please enter a positive integer value!{colors().END}")
				continue
			break
		except:
			print(f"{colors().RED}Invalid input, please enter a positive integer value!{colors().END}")


	prediction = round(theta1 * int(input_mileage) + theta0)
	if prediction < 0:
		prediction = 0
	print(f"\n{colors().BLUE}ESTIMATED PRICE: ${prediction}{colors().END}\n")

	if theta0 and theta1:
		# Plot the resulting regression line
		try:
			data = pd.read_csv('data.csv')
		except:
			print(f"{colors().RED}Error: could not read file{colors().END}")
			exit()
	
		max_km = data['km'].max()
		max_price = data['price'].max()
		tmp_max_km = max_km
		if input_mileage > max_km:
			tmp_max_km = input_mileage
		plt.plot(
			list(range(0, tmp_max_km)), 
			[theta1 * x + theta0 for x in range(0, tmp_max_km)], 
			color="green")
		# uncomment below for prediction marker
		plt.plot(input_mileage, prediction, marker="s", markersize=10, markerfacecolor="lightblue")
		plt.scatter(data.km, data.price, color="black")
		plt.show()


if __name__ == '__main__':
    main()