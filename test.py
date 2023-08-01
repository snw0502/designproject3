def quicksort(arr):
    def partition(arr, low, high):
        pivot = arr[high]  # Choose the pivot element (can be any element, here we choose the last element)
        i = low - 1  # Index of smaller element

        for j in range(low, high):
            if arr[j] < pivot:
                # Increment the index of smaller element and swap arr[i] with arr[j]
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        # Swap the pivot element with the element at index i+1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quicksort_helper(arr, low, high):
        if low < high:
            # Partition the array into two sub-arrays and get the pivot index
            pivot_index = partition(arr, low, high)

            # Recursively sort the sub-arrays
            quicksort_helper(arr, low, pivot_index - 1)
            quicksort_helper(arr, pivot_index + 1, high)

    # Start the quicksort process
    quicksort_helper(arr, 0, len(arr) - 1)

# Example usage:
unsorted_array = [43, 99, 23, 59, 4, 24, 3, 12, 55, 2, 72, 1, 53, 92, 85, 98, 58, 51, 37, 22, 32, 57, 84, 95, 7, 87, 62, 88, 8, 68, 42, 47, 28, 35, 29, 66, 16, 63, 94, 41, 74, 34, 31, 90, 33, 13, 11, 39, 9, 83, 73, 52, 5, 21, 25, 6, 10, 15, 14, 54, 30, 77, 75, 56, 71, 18, 27, 36, 96, 19, 45, 20, 97, 49, 26, 89, 61, 69, 86, 78, 67, 38, 81, 48, 60, 93, 65, 64, 50, 40, 82, 70, 91, 80, 46, 79, 44, 76, 17]
quicksort(unsorted_array)
print(unsorted_array)  # Output: [11, 12, 22, 25, 34, 64, 90]
