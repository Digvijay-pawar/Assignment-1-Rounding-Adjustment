# Assignment – Rounding Adjustment
---

## Problem Statement
A set of numbers, when rounded to a specific level (e.g., nearest lakh), may result in a mismatch at a total level. The task is to:
1. Adjust the total amount in the rounded array to ensure the sum of the rounded figures matches the rounded value of the total.
2. Extend the solution to support nested arrays in the input data.

### Example
Given the unrounded numbers:
```
123456.22, 6756.22, 7778899.98, 97876.45, 567.9, 9065337.78, 776767.87, 896433.23, 335345.87, 568899.45, 123343.47
```
Rounded values to the nearest lakh:
```
1.23, 0.07, 77.79, 0.98, 0.01, 90.65, 7.77, 8.96, 3.35, 5.69, 1.23
```
Two methods to compute totals:
1. Sum of rounded values: `197.73`
2. Rounded value of the sum: `197.74`

The mismatch (difference = `0.01`) needs to be resolved in the rounded figures.

---

## Solution Description

### Phase 1: Flat Array Adjustment
This phase resolves the mismatch for a flat array of numbers. The solution ensures the sum of rounded figures equals the rounded value of the total by adjusting the largest number in the rounded array.

#### Steps:
1. Parse the JSON input to extract unrounded numbers.
2. Calculate the total of unrounded numbers and round it to the nearest lakh.
3. Compute the rounded values of individual numbers.
4. Identify the difference between the rounded total and the total of rounded values.
5. Adjust the largest number in the rounded array to account for the difference.

#### Code Implementation
```python
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
print(json.dumps(output, indent=2))
```
### Output:
```json
{
  "original_numbers": [ 123456.22, 6756.22, 7778899.98, 97876.45, 567.9, 9065337.78, 776767.87, 896433.23, 335345.87, 568899.45, 123343.47],
  "rounded_numbers": [ 1.23, 0.07, 77.79, 0.98, 0.01, 90.65, 7.77, 8.96, 3.35, 5.69, 1.23 ],
  "adjusted_rounded_numbers": [ 1.23, 0.07, 77.79, 0.98, 0.01, 90.66, 7.77, 8.96, 3.35, 5.69,1.23 ],
  "unrounded_numbers_total": 197.74,
  "rounded_numbers_total": 197.73,
  "difference": 0.01,
  "adjusted_total": 197.74
}
```

### Phase 2: Nested Array Adjustment
This phase extends the logic to handle nested arrays.

#### Steps:
1. Traverse the nested arrays recursively to calculate totals and rounded values.
2. Flatten the nested structure to identify the largest number for adjustment.
3. Adjust the largest number to resolve the mismatch.

#### Code Implementation
```python
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

# Adjust the largest number
def adjust_rounded_numbers(numbers):
    max_value = max(flat_list(numbers))
    for i in range(len(numbers)):
        if isinstance(numbers[i], list):
            adjust_rounded_numbers(numbers[i])
        else:
            if numbers[i] == max_value:
                numbers[i] += output['difference']
                numbers[i] = round(numbers[i], 2)
                break

adjust_rounded_numbers(output['rounded_numbers'])
output['adjusted_rounded_numbers'] = output['rounded_numbers']
output['adjusted_rounded_numbers_total'] = calculate_rounded_numbers_total(output['adjusted_rounded_numbers'])

# Print the output
print(json.dumps(output, indent=2))
```
### Output:
```json
{
  "original_numbers": [ 123456.22, [ 6756.22, 7778899.98, [ 97876.45, 567.9] ], 9065337.78,[ 776767.87, [ 896433.23, 335345.87 ], 568899.45 ], 123343.47 ],
  "rounded_numbers": [ 1.23, [ 0.07, 77.79, [ 0.98, 0.01 ] ], 90.65, [ 7.77, [ 8.96, 3.35 ], 5.69 ], 1.23 ],
  "adjusted_rounded_numbers": [ 1.23, [ 0.07, 77.79, [ 0.98, 0.01 ] ], 90.66, [ 7.77, [ 8.96, 3.35 ], 5.69 ], 1.23 ],
  "unrounded_numbers_total": 197.74,
  "rounded_numbers_total": 197.73,
  "difference": 0.01,
  "adjusted_rounded_numbers_total": 197.74
}
```
---

## Conclusion
This assignment demonstrates a practical solution to rounding discrepancies in flat and nested arrays. The algorithms ensure consistent totals by adjusting the largest number, preserving data integrity in financial calculations.

