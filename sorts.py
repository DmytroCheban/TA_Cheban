def selection_sort(arr, trace=False):
    n = len(arr)
    comparisons = 0
    assignments = 0
    if trace:
        print("Початковий масив:", arr)
    # Зовнішній цикл: від 0 до n-2 (n-1 проходів)
    for i in range(n - 1):
        min_index = i
        assignments += 1
        if trace:
            print(f"Ітерація {i}:")
            print(f"  Поточний елемент: arr[{i}] = {arr[i]}")
            print(f"  Частина для пошуку: {arr[i:]}")
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_index]:
                min_index = j
                assignments += 1
        # Порівняння min_index != i
        comparisons += 1
        if trace:
            print(f"  Мінімум: arr[{min_index}] = {arr[min_index]}")
        if min_index != i:
            if trace:
                print(f"  Обмін arr[{i}] ({arr[i]}) і arr[{min_index}] ({arr[min_index]})")
            arr[i], arr[min_index] = arr[min_index], arr[i]
            assignments += 3
        elif trace:
            print("  min_index == i, обмін не потрібен")
        if trace:
            print(f"  Масив після ітерації {i}: {arr}")
    return arr, comparisons, assignments


def insertion_sort(arr, trace=False):
    n = len(arr)
    comparisons = 0
    assignments = 0
    if trace:
        print("Початковий масив:", arr)
    for i in range(1, n):
        # Зберігаємо елемент для вставки
        key = arr[i]
        assignments += 1
        j = i - 1
        assignments += 1
        if trace:
            print(f"Ітерація {i}:")
            print(f"  Елемент для вставки (key): {key}")
            print(f"  Відсортована частина: {arr[:i]}")
        while j >= 0 and arr[j] > key:
            comparisons += 1
            if trace:
                print(f"  Порівняння: {arr[j]} > {key}. True. Зсуваємо {arr[j]} вправо.")
            arr[j + 1] = arr[j]
            assignments += 1
            j -= 1
            assignments += 1
        if j >= 0:
            comparisons += 1
            if trace:
                print(f"  Порівняння: {arr[j]} > {key}. False. Цикл завершено.")
        elif trace:
            print("  Досягнуто початку масиву. Цикл завершено.")
        arr[j + 1] = key
        assignments += 1
        if trace:
            print(f"  Вставка {key} на позицію {j + 1}.")
            print(f"  Масив після ітерації {i}: {arr}")
    return arr, comparisons, assignments


def stability_demo():
    data = [(2, 'a'), (2, 'b'), (1, 'c')]
    for name in ("Вибором", "Вставками"):
        print(name, sort_pairs(data, name))


def sort_pairs(p, kind):
    p = p.copy()
    if kind == "Вибором":
        for i in range(len(p) - 1):
            m = i
            for j in range(i + 1, len(p)):
                if p[j][0] < p[m][0]:
                    m = j
            p[i], p[m] = p[m], p[i]
    else:
        for i in range(1, len(p)):
            k = p[i]
            j = i - 1
            while j >= 0 and p[j][0] > k[0]:
                p[j + 1] = p[j]
                j -= 1
            p[j + 1] = k
    return p


if __name__ == "__main__":
    variant17 = [7, 89, 4, 68, 70, 49, 10, 62, 51]
    print("=== Сортування вибором ===")
    res, c, a = selection_sort(variant17.copy(), trace=True)
    print("Відсортований масив:", res)
    print("Кількість порівнянь:", c)
    print("Кількість присвоєнь:", a)
    print("\n=== Сортування вставками ===")
    res, c, a = insertion_sort(variant17.copy(), trace=True)
    print("Відсортований масив:", res)
    print("Кількість порівнянь:", c)
    print("Кількість присвоєнь:", a)
    print("\n=== Стійкість (ключ — перше поле) ===")
    stability_demo()
