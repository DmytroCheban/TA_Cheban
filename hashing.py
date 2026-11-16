import math

# Номери позицій літер українського алфавіту (рисунок 4.3)
LETTER_POSITIONS = {
    'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Ґ': 5, 'Д': 6, 'Е': 7, 'Є': 8, 'Ж': 9,
    'З': 10, 'И': 11, 'І': 12, 'Ї': 13, 'Й': 14, 'К': 15, 'Л': 16, 'М': 17,
    'Н': 18, 'О': 19, 'П': 20, 'Р': 21, 'С': 22, 'Т': 23, 'У': 24, 'Ф': 25,
    'Х': 26, 'Ц': 27, 'Ч': 28, 'Ш': 29, 'Щ': 30, 'Ь': 31, 'Ю': 32, 'Я': 33,
}
PHRASE = "Більше діла, менше слів — отак добудеш хліб"
A = 0.6180339887            # константа Кнута
M_DIV = 13                  # розмір таблиці для методу ділення
M_MUL = 16                  # розмір таблиці для методу множення
DELETED = "DELETED"


def get_words(text):
    """Розбиває речення на слова, відкидаючи розділові знаки."""
    clean = "".join(ch if ch.isalpha() or ch.isspace() else " " for ch in text)
    return [w.upper() for w in clean.split()]


def key_value(word):
    """Ключ K — сума номерів позицій літер слова в алфавіті."""
    return sum(LETTER_POSITIONS.get(ch, 0) for ch in word)


def hash_div(word, m=M_DIV):
    """Метод ділення: h(K) = K mod m."""
    return key_value(word) % m


def hash_mul(word, m=M_MUL):
    """Метод множення: h(K) = floor(m * (K*A mod 1))."""
    k = key_value(word)
    return int(m * ((k * A) % 1))


# ---------- Відкрите хешування (ланцюжки) ----------
def build_open_hash_table(words, m, h):
    table = [[] for _ in range(m)]
    for w in words:
        table[h(w, m)].append(w)        # вставка в кінець ланцюжка
    return table


def search_open(table, word, h):
    """Повертає (знайдено?, кількість порівнянь ключів)."""
    comparisons = 0
    for item in table[h(word, len(table))]:
        comparisons += 1
        if item == word:
            return True, comparisons
    return False, comparisons


def delete_open(table, word, h):
    """Видалення = пошук + видалення зі списку. Повертає (видалено?, порівняння)."""
    found, c = search_open(table, word, h)
    if found:
        table[h(word, len(table))].remove(word)
    return found, c


# ---------- Закрите хешування (лінійне дослідження) ----------
def build_closed_hash_table(words, m, h):
    table = [None] * m
    for w in words:
        start = h(w, m)
        for i in range(m):
            addr = (start + i) % m      # h(k, i) = (h(k) + i) mod m
            if table[addr] is None or table[addr] == DELETED:
                table[addr] = w
                break
        else:
            print(f"Помилка: таблиця заповнена, слово {w} не додано")
    return table


def search_closed(table, word, h):
    """Повертає (індекс або None, порівняння ключів, кількість досліджених комірок)."""
    m = len(table)
    start = h(word, m)
    comparisons = 0
    probes = 0
    for i in range(m):
        addr = (start + i) % m
        probes += 1
        cell = table[addr]
        if cell is None:                # порожня комірка — ключа немає
            return None, comparisons, probes
        if cell != DELETED:
            comparisons += 1
            if cell == word:
                return addr, comparisons, probes
    return None, comparisons, probes


def delete_closed(table, word, h):
    """Відкладене видалення: комірку позначаємо DELETED."""
    idx, c, p = search_closed(table, word, h)
    if idx is not None:
        table[idx] = DELETED
    return idx, c, p


def display_open(table):
    print(f"--- Відкрита хеш-таблиця (M={len(table)}) ---")
    for i, chain in enumerate(table):
        print(f"Індекс {i:02d}: {chain}")


def display_closed(table):
    print(f"--- Закрита хеш-таблиця (M={len(table)}) ---")
    print("Індекс | Слово")
    for i, item in enumerate(table):
        print(f"{i:02d} | {item if item is not None else '(NULL)'}")


if __name__ == "__main__":
    words = get_words(PHRASE)
    print("Слова:", words)
    for w in words:
        print(f"{w}: K = {key_value(w)}, K mod 13 = {hash_div(w)}, "
              f"h_mul = {hash_mul(w)}")
    for name, h, m in (("ділення", hash_div, M_DIV), ("множення", hash_mul, M_MUL)):
        print(f"\n===== Метод {name} =====")
        t = build_open_hash_table(words, m, h)
        display_open(t)
        t2 = build_closed_hash_table(words, m, h)
        display_closed(t2)
