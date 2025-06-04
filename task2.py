def binary_search_with_upper_bound(arr, target):
    left = 0
    right = len(arr) - 1
    iterations = 0  # Лічильник ітерацій
    upper_bound = None  # Змінна для збереження верхньої межі

    while left <= right:
        iterations += 1  # Збільшуємо кількість ітерацій
        mid = (left + right) // 2  # Обчислюємо середній індекс

        if arr[mid] == target:
            upper_bound = arr[mid]  # Якщо знайшли точне співпадіння
            return (iterations, upper_bound)

        elif arr[mid] < target:
            left = mid + 1  # Пошук правіше

        else:
            upper_bound = arr[mid]  # Можливий кандидат на верхню межу
            right = mid - 1  # Пошук лівіше

    # Повертаємо кількість ітерацій і знайдену верхню межу (може бути None)
    return (iterations, upper_bound)


# Тестуємо функцію:
array = [1.2, 2.5, 3.7, 4.4, 5.0, 6.8, 7.3]
target = 4.0

result = binary_search_with_upper_bound(array, target)
print(result)  # Наприклад, виведе: (3, 4.4)
