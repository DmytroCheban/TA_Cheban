# ---------- Сортування злиттям: ітеративна версія ----------
def merge_sort_iterative(a, trace=False):
    n = len(a)
    comparisons = 0
    assignments = 0
    if trace:
        print("Початковий масив:", a)
    i = 1
    assignments += 1
    while i < n:
        j = 0
        assignments += 1
        while j < n - i:
            left = j
            mid = j + i
            right = min(j + 2 * i, n)
            assignments += 3
            c, s = merge_iterative(a, left, mid, right, trace)
            comparisons += c
            assignments += s
            j += 2 * i
            assignments += 1
        i *= 2
        assignments += 1
    return a, comparisons, assignments


def merge_iterative(a, left, mid, right, trace=False):
    comparisons = 0
    assignments = 0
    n1 = mid - left
    n2 = right - mid
    # Тимчасові підмасиви
    L = a[left:mid]
    R = a[mid:right]
    assignments += n1 + n2
    it1 = it2 = 0
    k = left
    assignments += 3
    if trace:
        print(f"Об'єднуємо a[{left}:{mid}] ({L}) і a[{mid}:{right}] ({R})")
    while it1 < n1 and it2 < n2:
        comparisons += 1
        if trace:
            print(f"  Порівняння: {L[it1]} <= {R[it2]}")
        if L[it1] <= R[it2]:        # <= забезпечує стійкість
            a[k] = L[it1]
            it1 += 1
        else:
            a[k] = R[it2]
            it2 += 1
        k += 1
        assignments += 3            # запис a[k], зсув it, зсув k
    while it1 < n1:                 # залишок лівого підмасиву
        a[k] = L[it1]
        it1 += 1
        k += 1
        assignments += 3
    while it2 < n2:                 # залишок правого підмасиву
        a[k] = R[it2]
        it2 += 1
        k += 1
        assignments += 3
    if trace:
        print("Масив після об'єднання:", a)
    return comparisons, assignments


# ---------- Сортування злиттям: рекурсивна версія ----------
def merge_sort_recursive(arr, trace=False, depth=0):
    comparisons = 0
    assignments = 0
    recursive_calls = 1             # поточний виклик
    pad = "  " * depth
    if len(arr) <= 1:
        return arr, comparisons, assignments, recursive_calls
    if trace:
        print(f"{pad}Розділяємо масив: {arr}")
    mid = len(arr) // 2
    assignments += 1
    left_half, c1, a1, r1 = merge_sort_recursive(arr[:mid], trace, depth + 1)
    right_half, c2, a2, r2 = merge_sort_recursive(arr[mid:], trace, depth + 1)
    comparisons += c1 + c2
    assignments += a1 + a2
    recursive_calls += r1 + r2
    merged, c, s = merge(left_half, right_half, trace, pad)
    comparisons += c
    assignments += s
    return merged, comparisons, assignments, recursive_calls


def merge(left, right, trace=False, pad=""):
    result = []
    comparisons = 0
    assignments = 3                 # result, i, j
    i = j = 0
    if trace:
        print(f"{pad}Зливаємо {left} та {right}")
    while i < len(left) and j < len(right):
        comparisons += 1
        if trace:
            print(f"{pad}  Порівняння: {left[i]} <= {right[j]}")
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
        assignments += 2            # append та зсув індексу
    while i < len(left):
        result.append(left[i])
        i += 1
        assignments += 2
    while j < len(right):
        result.append(right[j])
        j += 1
        assignments += 2
    if trace:
        print(f"{pad}Результат злиття: {result}")
    return result, comparisons, assignments


# ---------- Швидке сортування (схема Хоара) ----------
def quicksort(a, l, r, trace=False, depth=0):
    pad = "  " * depth
    comparisons = 0
    assignments = 0
    recursive_calls = 1             # поточний виклик
    if trace:
        print(f"{pad}quicksort: a = {a}, l = {l}, r = {r}")
    if l < r:
        q, c1, a1 = partition(a, l, r, trace, pad)
        comparisons += c1
        assignments += a1
        c2, a2, r2 = quicksort(a, l, q, trace, depth + 1)
        c3, a3, r3 = quicksort(a, q + 1, r, trace, depth + 1)
        comparisons += c2 + c3
        assignments += a2 + a3
        recursive_calls += r2 + r3
    return comparisons, assignments, recursive_calls


def partition(a, l, r, trace=False, pad=""):
    comparisons = 0
    assignments = 0
    pivot = a[l]
    i = l - 1
    j = r + 1
    assignments += 3
    if trace:
        print(f"{pad}  Опорний елемент (pivot) = {pivot}")
    while True:
        i += 1
        assignments += 1
        comparisons += 1                    # перевірка a[i] < pivot
        while a[i] < pivot:
            i += 1
            assignments += 1
            comparisons += 1
        j -= 1
        assignments += 1
        comparisons += 1                    # перевірка a[j] > pivot
        while a[j] > pivot:
            j -= 1
            assignments += 1
            comparisons += 1
        comparisons += 1                    # перевірка i >= j
        if i >= j:
            if trace:
                print(f"{pad}  i = {i}, j = {j}: індекси перетнулися, "
                      f"повертаємо q = {j}. Масив: {a}")
            return j, comparisons, assignments
        if trace:
            print(f"{pad}  i = {i}, j = {j}: обмін a[{i}] ({a[i]}) "
                  f"і a[{j}] ({a[j]})")
        a[i], a[j] = a[j], a[i]
        assignments += 3
        if trace:
            print(f"{pad}  Масив: {a}")


# ---------- Перевірка стійкості (ключ — перше поле пари) ----------
def stable_merge(p):
    if len(p) <= 1:
        return p
    m = len(p) // 2
    L, R = stable_merge(p[:m]), stable_merge(p[m:])
    res = []
    i = j = 0
    while i < len(L) and j < len(R):
        if L[i][0] <= R[j][0]:
            res.append(L[i]); i += 1
        else:
            res.append(R[j]); j += 1
    return res + L[i:] + R[j:]


def quick_pairs(p, l, r):
    if l < r:
        pivot = p[l][0]
        i, j = l - 1, r + 1
        while True:
            i += 1
            while p[i][0] < pivot:
                i += 1
            j -= 1
            while p[j][0] > pivot:
                j -= 1
            if i >= j:
                break
            p[i], p[j] = p[j], p[i]
        quick_pairs(p, l, j)
        quick_pairs(p, j + 1, r)


if __name__ == "__main__":
    variant17 = [7, 89, 4, 68, 70, 49, 10, 62, 51]
    print("=== ІТЕРАТИВНЕ СОРТУВАННЯ ЗЛИТТЯМ ===")
    res, c, s = merge_sort_iterative(variant17.copy(), trace=True)
    print("Відсортований список:", res)
    print("Кількість порівнянь:", c)
    print("Кількість присвоєнь:", s)
    print("\n=== РЕКУРСИВНЕ СОРТУВАННЯ ЗЛИТТЯМ ===")
    res, c, s, rc = merge_sort_recursive(variant17.copy(), trace=True)
    print("Відсортований список:", res)
    print("Кількість порівнянь:", c)
    print("Кількість присвоєнь:", s)
    print("Кількість рекурсивних викликів:", rc)
    print("\n=== ШВИДКЕ СОРТУВАННЯ (СХЕМА ХОАРА) ===")
    arr = variant17.copy()
    c, s, rc = quicksort(arr, 0, len(arr) - 1, trace=True)
    print("Відсортований список:", arr)
    print("Кількість порівнянь:", c)
    print("Кількість присвоєнь:", s)
    print("Кількість рекурсивних викликів:", rc)
    print("\n=== СТІЙКІСТЬ ===")
    data = [(2, 'a'), (2, 'b'), (1, 'c')]
    q = data.copy()
    quick_pairs(q, 0, len(q) - 1)
    print("Злиття:", stable_merge(data))
    print("Швидке:", q)
