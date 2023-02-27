import sys
from colors import colors


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


if __name__ == '__main__':
    main()