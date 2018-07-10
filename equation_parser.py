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


parentheses(expression)
	
	--              --                 /              \ 
	|                |                |                |
	|  (expression)  |       OR       |  (expression)  |
	|                |                |                |
	--              --                 \              / 


mathematical_operation(op)

	[num1] op [num2]


exp(base, pow)

        pow
    base

'''

import sys

def exp_frac(output_matrix, base, exp_num, exp_denom):

	# TODO - tidy this, make less use of magic numbers
	max_buffer = max(len(exp_num), len(exp_denom))

	output_matrix[0] += "   " + " " * int(((max_buffer-len(exp_num))/2)) + exp_num + " " * int(((max_buffer-len(exp_num))/2)) + " "*len(base)
	output_matrix[1] += "  " + "-" * (max_buffer + 2)
	output_matrix[2] += "   " + " " * int(((max_buffer-len(exp_denom))/2)) + exp_denom + " " * int(((max_buffer-len(exp_denom))/2)) + " "*len(base)
	output_matrix[3] += " " + base + " "*max_buffer + "  "
	output_matrix[4] += " "*(len(base) + max_buffer + 1) + "  "

def exp(output_matrix, base, exp):

	# +1 instead of -1 to account for spacing on the ends of the characters
	output_matrix[0] += " "*(len(base) + len(exp) + 1)
	output_matrix[1] += " "*len(base) + exp + " "
	output_matrix[2] += " " + base + " "*len(exp)
	output_matrix[3] += " "*(len(base) + len(exp) + 1)
	output_matrix[4] += " "*(len(base) + len(exp) + 1)

def math_ops(output_matrix, symbol):
	buflen = len(symbol)+2

	output_matrix[0] += " "*buflen
	output_matrix[1] += " "*buflen
	output_matrix[2] += " " + symbol + " "
	output_matrix[3] += " "*buflen
	output_matrix[4] += " "*buflen

def print_matrix(matrix):
	for line in matrix:
		print(line)

def brackets(output_matrix, expression):
	buflen = len(expression)

	output_matrix[0] += " " + "--"  + " "*(buflen+2) + "--"
	output_matrix[1] += " " + "| "  + " "*(buflen+2) + " |"
	output_matrix[2] += " " + "| "  + " " + expression + " " + " |"
	output_matrix[3] += " " + "| "  + " "*(buflen+2) + " |"
	output_matrix[4] += " " + "--" + " "*(buflen+2) + "--"

def parentheses(output_matrix, expression):
	buflen = len(expression)

	output_matrix[0] += " " + " /"  + " "*(buflen+2) + "\\ "
	output_matrix[1] += " " + "| "  + " "*(buflen+2) + " |"
	output_matrix[2] += " " + "| "  + " " + expression + " " + " |"
	output_matrix[3] += " " + "| "  + " "*(buflen+2) + " |"
	output_matrix[4] += " " + " \\" + " "*(buflen+2) + "/ "

def product(output_matrix, counter, limit, equation):
	max_buffer = max(len(counter), len(limit), len(equation))
	PI_LENGTH = len("_____")

	output_matrix[0] += "   " + str(limit) + " " * (max_buffer-len(limit)+PI_LENGTH)
	output_matrix[1] += "  " + "_____ " + " " * max_buffer
	output_matrix[2] += "  " + " | |  " + str(equation) + " " * (max_buffer-len(equation))
	output_matrix[3] += "  " + " | |  " + " " * max_buffer
	output_matrix[4] += "   " + str(counter) + " " * (max_buffer-len(counter)+PI_LENGTH)

def frac(output_matrix, numerator, denominator):
	max_buffer = max(len(numerator), len(denominator))

	output_matrix[0] += "  " + " " * (max_buffer+2)
	output_matrix[1] += "   " + " " * int(((max_buffer-len(numerator))/2)) + numerator + " " * int(((max_buffer-len(numerator))/2)) + " "
	output_matrix[2] += "  " + "-" * (max_buffer + 2)
	output_matrix[3] += "   " + " " * int(((max_buffer-len(denominator))/2)) + denominator + " " * int(((max_buffer-len(denominator))/2)) + " "
	output_matrix[4] += "  " + " " * (max_buffer+2)

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
	output_matrix[4] += "  \-/ " + str(lower) + " "*(max_buffer-len(lower)+2)

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

	summation(equation_matrix, "i=1fsdfs", "kfdsfds", "x_i")
	integral(equation_matrix, "0", "infinity", "(1 / fdsfdsfdsx) dx")
	product(equation_matrix, "k", "334", "(1 + (x / 3)")
	math_ops(equation_matrix, "+")
	exp_frac(equation_matrix, "e", "13134", "2")
	exp(equation_matrix, "20232", "10100")
	frac(equation_matrix, "c^2", "b + a")
	brackets(equation_matrix, "x + 3/2")

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


