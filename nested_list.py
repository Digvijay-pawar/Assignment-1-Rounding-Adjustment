import json

# Input
input_numbers = '''{
    "numbers": [
        123456.22,
        [6756.22, 7778899.98, [97876.45, 567.9]],
        9065337.78,
        [776767.87, [896433.23, 335345.87], 568899.45],
        123343.47
    ]
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

# round numbers and calculate total
def round_numbers_and_total(numbers):
    rounded = []
    total = 0
    for num in numbers:
        if isinstance(num, list):
            rounded_sublist, sublist_total = round_numbers_and_total(num)
            rounded.append(rounded_sublist)
            total += sublist_total
        else:
            rounded_number = round(num / 100000, 2)
            rounded.append(rounded_number)
            total += num
    return rounded, total

output['rounded_numbers'], output['unrounded_numbers_total'] = round_numbers_and_total(input_numbers['numbers'])
output['unrounded_numbers_total'] = round(output['unrounded_numbers_total'] / 100000, 2)

# calculate total of rounded numbers
def calculate_rounded_numbers_total(numbers):
    total = 0
    for num in numbers:
        if isinstance(num, list):
            total += calculate_rounded_numbers_total(num)
        else:
            total += num
    return round(total, 2)

output['rounded_numbers_total'] = calculate_rounded_numbers_total(output['rounded_numbers'])

# Difference
output['difference'] = round(output['unrounded_numbers_total'] - output['rounded_numbers_total'], 2)

# flatten the list
def flat_list(numbers):
    flat = []
    for num in numbers:
        if isinstance(num, list):
            flat.extend(flat_list(num))
        else:
            flat.append(num)
    return flat


# Method 1: Adjust the difference in the largest number
def adjust_rounded_numbers(numbers):
    max_value = max(flat_list(numbers))
    adjusted_list = numbers[:]
    print(max_value)
    for i in range(len(adjusted_list)):
        if isinstance(adjusted_list[i], list):
            adjust_rounded_numbers(adjusted_list[i])  
        else:
            if adjusted_list[i] == max_value:  
                adjusted_list[i] += output['difference']
                adjusted_list[i] = round(adjusted_list[i], 2) 
                break  
    return adjusted_list


# Apply Method 1 
output['adjusted_rounded_numbers'] = adjust_rounded_numbers(output['rounded_numbers'])
output['adjusted_rounded_numbers_total'] = calculate_rounded_numbers_total(output['adjusted_rounded_numbers'])


# Print the output
print(json.dumps(output, indent=2))
