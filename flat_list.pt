import json

# Input
input_numbers = '''{
    "numbers": [123456.22, 6756.22, 7778899.98, 97876.45, 567.9, 9065337.78, 776767.87, 896433.23, 335345.87, 568899.45, 123343.47]
}'''
input_numbers = json.loads(input_numbers)

# Output
output = {
    "original_numbers": input_numbers['numbers'],
    "rounded_numbers": [],
    "adjusted_rounded_numbers": [],
    "unrounded_numbers_total": 0,
    "rounded_numbers_total": 0,
    "difference": 0
}

# Calculate unrounded total
output['unrounded_numbers_total'] = round(sum(input_numbers['numbers']) / 100000, 2)

# Rounding function
def rounding_of_numbers(input_numbers):
    for i in input_numbers['numbers']:
        rounded_number = round(i / 100000, 2)
        output['rounded_numbers'].append(rounded_number)
rounding_of_numbers(input_numbers)

# Calculate rounded total
output['rounded_numbers_total'] = round(sum(output['rounded_numbers']), 2)

# Count difference
difference = output['unrounded_numbers_total'] - output['rounded_numbers_total']
output['difference'] = round(difference, 2)

# Adjust the difference in one number (e.g., largest number)
def adjust_rounded_numbers():
    largest_index = output['rounded_numbers'].index(max(output['rounded_numbers']))
    adjusted_rounded_numbers = output['rounded_numbers'][:]
    adjusted_rounded_numbers[largest_index] += output['difference']
    output['adjusted_rounded_numbers'] = adjusted_rounded_numbers
    output['adjusted_total'] = round(sum(adjusted_rounded_numbers), 2)
    
adjust_rounded_numbers()

# Print the output
print(json.dumps(output, indent=1))
