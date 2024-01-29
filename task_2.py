def binary_search(array: list, target: float) -> tuple:
    left = 0
    right = len(array) - 1
    counter = 0

    while left <= right:
        mid = (left + right) // 2
        counter += 1

        if array[mid] < target:
            left = mid + 1
        elif array[mid] > target:
            right = mid - 1
        else:
            # Element found
            return counter, array[mid]

    # If the target is not in the array, return the upper bound
    upper = array[left] if left < len(array) else None
    return counter, upper


# Example usage:
sorted_array = [0.2, 1.1, 1.7, 2.6, 3.3, 4.1, 4.7, 5.8, 7.3, 8.1, 8.6, 8.9, 9.7]

targets = [2.1, 4.4, 7.3, 8.8, 10]

for target_value in targets:
    iterations, upper_bound = binary_search(sorted_array, target_value)

    if upper_bound is not None:
        print(f"Target: {target_value}, Number of iterations: {iterations}, "
              f"Upper bound: {upper_bound}")
    else:
        print(f"Target: {target_value}, Number of iterations: {iterations}, "
              f"Target value not found")
