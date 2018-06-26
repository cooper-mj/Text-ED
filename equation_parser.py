'''
Description: library of functions to render Latex-like syntax into
ASCII-art equations.

Initial Syntax / Visualization Reference:

summation(equation, counter, limit)

	limit
	___
	\     (equation)
	/__ 
	counter


frac(numerator, denominator)

	 numerator
	-----------
	denominator


product(equation, counter, limit)

	limit
	_____
	 | | 	(equation)
	 | |
	counter


integral(lower, upper, equation)

	  /-\ upper
	  |
	  |		(equation)
	  |
	\-/ lower



## The following have yet to be implemented

exp(base, pow)

        pow
    base


parentheses(expression)
	
	--              --                 /              \ 
	|                |                |                |
	|  (expression)  |       OR       |  (expression)  |
	|                |                |                |
	--              --                 \              / 


times(num1, num2)

	num1 x num2

'''

import sys

def print_matrix(matrix):
	for line in matrix:
		print(line)

def product(output_matrix, counter, limit, equation):
	max_buffer = max(len(counter), len(limit), len(equation))
	PI_OFFSET = len(" ")

	output_matrix[0] += "   " + str(limit) + " " * (max_buffer-len(limit)-PI_OFFSET)
	output_matrix[1] += "  " + "_____ " + " " * max_buffer
	output_matrix[2] += "  " + " | |  " + str(equation) + " " * (max_buffer-len(equation))
	output_matrix[3] += "  " + " | |  " + " " * max_buffer
	output_matrix[4] += "   " + str(counter) + " " * (max_buffer-len(counter)-PI_OFFSET)

def frac(output_matrix, numerator, denominator):
	max_buffer = max(len(numerator), len(denominator))

	output_matrix[0] += "  " + " " * max_buffer
	output_matrix[1] += "   " + " " * int(((max_buffer-len(numerator))/2)) + numerator + " " * int(((max_buffer-len(numerator))/2))
	output_matrix[2] += "  " + "-" * (max_buffer + 2)
	output_matrix[3] += "   " + " " * int(((max_buffer-len(denominator))/2)) + denominator + " " * int(((max_buffer-len(denominator))/2))
	output_matrix[4] += "  " + " " * max_buffer

def summation(output_matrix, counter, limit, equation):

	max_buffer = max(len(str(counter)), len(str(limit)), len(str(equation)))
	SIGMA_LENGTH = len("_____ ") # The length of the sigma character
	LIMIT_COUNTER_OFFSET = len("  ")

	output_matrix[0] += "    " + str(limit) + " "*(max_buffer-len(limit)+SIGMA_LENGTH-LIMIT_COUNTER_OFFSET)
	output_matrix[1] += "  _____ " + " "*max_buffer
	output_matrix[2] += "  \     " + str(equation) + " "*(max_buffer-len(equation))
	output_matrix[3] += "  /____ " + " "*max_buffer
	output_matrix[4] += "    " + str(counter) + " "*(max_buffer-len(counter)+SIGMA_LENGTH-LIMIT_COUNTER_OFFSET)

def integral(output_matrix, lower, upper, equation):

	max_buffer = max(len(str(lower)), len(str(upper)), len(str(equation)))

	output_matrix[0] += "    /-\ " + str(upper) + " "*(max_buffer-len(upper))
	output_matrix[1] += "    |   " + " "*max_buffer
	output_matrix[2] += "    |   " + str(equation) + " "*(max_buffer-len(equation))
	output_matrix[3] += "    |   " + " "*max_buffer
	output_matrix[4] += "  \-/   " + str(lower) + " "*(max_buffer-len(lower))

def parser_test_mode():

	# NOTE: When parsing is functional, this will serve as a shell-like environment 
	# to test equation rendering. In current form, it provides basic tests of 
	# the presently implemented renderings of mathematical symbols.

	equation_matrix = [ # Adds to each line at a time as it parses the equation
	"",
	"",
	"",
	"",
	"",
	]

	print("\n")

	summation(equation_matrix, "i=1", "k", "x_i")
	integral(equation_matrix, "0", "infinity", "(1 / x) dx")
	product(equation_matrix, "22", "334", "(1 + (x / 3)")
	frac(equation_matrix, "c^2", "b + a")

	print_matrix(equation_matrix)

	print("\n")

	return

def main():
	return

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        # Then run the server in testing mode
		parser_test_mode()
	else:
		main()


