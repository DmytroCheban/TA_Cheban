def sink(arr, i, n, trace=0):
    """Занурення елемента arr[i] у купі розміром n. Повертає (порівняння, присвоєння)."""
    comparisons = 0
    assignments = 0
    k = i
    assignments += 1
    if trace > 1:
        print(f"Починаємо 'занурювати' елемент: {arr[i]} з індексу {i}")
    while True:
        j = 2 * k + 1                       # індекс лівого дочірнього елемента
        assignments += 1
        if j >= n:
            if trace > 1:
                print(f"Елемент {arr[k]} на індексі {k} досяг кінця купи. Завершуємо.")
            break
        if j + 1 < n:                       # правий дочірній елемент існує
            comparisons += 1
            if arr[j + 1] > arr[j]:
                j += 1
                assignments += 1
                if trace > 1:
                    print(f"  Порівнюємо {arr[j-1]} (лівий) та {arr[j]} (правий). Обираємо {arr[j]}")
            elif trace > 1:
                print(f"  Порівнюємо {arr[j]} (лівий) та {arr[j+1]} (правий). Обираємо {arr[j]}")
        elif trace > 1:
            print(f"  Обираємо лівий дочірній елемент: {arr[j]} на індексі {j}")
        comparisons += 1
        if arr[k] >= arr[j]:
            if trace > 1:
                print(f"  {arr[k]} (батько) >= {arr[j]} (найбільший дочірній). "
                      f"Елемент на своєму місці.")
            break
        if trace > 1:
            print(f"  Міняємо місцями {arr[k]} (батько) та {arr[j]} (дочірній)")
        arr[k], arr[j] = arr[j], arr[k]
        assignments += 3
        k = j
        assignments += 1
        if trace > 1:
            print(f"  Масив після обміну: {arr}")
    return comparisons, assignments


def heapsort(arr, trace=0):
    """Пірамідальне сортування. Повертає (масив, порівняння, присвоєння)."""
    comparisons = 0
    assignments = 0
    n = len(arr)
    assignments += 1
    if trace:
        print(f"Початковий масив: {arr}")
        print("--- Фаза 1: Побудова максимальної купи ---")
    # Фаза 1: побудова максимальної купи
    for i in range(n // 2 - 1, -1, -1):
        if trace == 1:
            print(f"Занурюємо елемент з індексу {i}: {arr[i]}")
        c, a = sink(arr, i, n, trace)
        comparisons += c
        assignments += a
        if trace > 1:
            print("---------------------------------")
    if trace:
        print(f"Масив після побудови купи: {arr}")
        print("--- Фаза 2: Сортування ---")
    # Фаза 2: сортування
    for i in range(n - 1, 0, -1):
        if trace:
            print(f"Міняємо місцями корінь ({arr[0]}) та останній елемент ({arr[i]})")
        arr[0], arr[i] = arr[i], arr[0]
        assignments += 3
        size = i                            # розмір купи зменшується
        assignments += 1
        if trace:
            print(f"Розмір купи зменшився до {size}. Відновлюємо властивості купи.")
        c, a = sink(arr, 0, size, trace)
        comparisons += c
        assignments += a
        if trace:
            print(f"Масив на поточному кроці: {arr}")
    if trace:
        print(f"Відсортований масив: {arr}")
    return arr, comparisons, assignments


def heapsort_pairs(p):
    """Те саме сортування для пар (ключ, поле): порівняння лише за ключем."""
    def sink_p(a, i, n):
        k = i
        while True:
            j = 2 * k + 1
            if j >= n:
                break
            if j + 1 < n and a[j + 1][0] > a[j][0]:
                j += 1
            if a[k][0] >= a[j][0]:
                break
            a[k], a[j] = a[j], a[k]
            k = j
    p = p.copy()
    n = len(p)
    for i in range(n // 2 - 1, -1, -1):
        sink_p(p, i, n)
    for i in range(n - 1, 0, -1):
        p[0], p[i] = p[i], p[0]
        sink_p(p, 0, i)
    return p


if __name__ == "__main__":
    variant17 = [7, 89, 4, 68, 70, 49, 10, 62, 51]
    res, c, a = heapsort(variant17.copy(), trace=1)
    print("Кількість порівнянь:", c)
    print("Кількість присвоєнь:", a)
    print("\nСтійкість:", heapsort_pairs([(2, 'a'), (2, 'b'), (1, 'c')]))
