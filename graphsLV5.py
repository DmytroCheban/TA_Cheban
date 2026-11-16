INF = float('inf')
V = 8
# Граф варіанта 17: ребра (u, v, вага), вершини нумеруються з 1
EDGES = [(1, 3, 2), (1, 2, 8), (1, 5, 3), (1, 4, 4), (2, 6, 3), (2, 5, 6),
         (3, 8, 4), (3, 4, 6), (3, 6, 7), (4, 5, 1), (5, 7, 4), (6, 8, 1),
         (6, 7, 3), (7, 8, 5)]


def build_adjacency_matrix(n, edges):
    """Матриця суміжності зваженого неорієнтованого графа (INF — ребра немає)."""
    g = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        g[u - 1][v - 1] = w
        g[v - 1][u - 1] = w
    return g


def build_adjacency_lists(n, edges):
    """Списки суміжності: для кожної вершини — список пар (сусід, вага)."""
    adj = {i: [] for i in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    for i in adj:
        adj[i].sort()
    return adj


def print_matrix(g):
    n = len(g)
    print("    " + " ".join(f"{j + 1:>3}" for j in range(n)))
    for i in range(n):
        print(f"{i + 1:>3} " + " ".join(f"{'-' if x == INF else x:>3}" for x in g[i]))


def print_lists(adj):
    for v, nb in adj.items():
        print(f"{v}: " + ", ".join(f"{u}({w})" for u, w in nb))


def prim(g, start=0, trace=False):
    """Алгоритм Прима за псевдокодом: на кожному кроці вибирається найменше
    ребро між VT і V - VT. При однакових вагах береться ребро з меншими (i, j)."""
    n = len(g)
    vt = [start]                         # множина вершин MST
    et = []                              # множина ребер MST
    if trace:
        print(f"Початок: VT = {{{start + 1}}}, ET = {{}}")
    for step in range(1, n):
        # допустимі (примежові) ребра: i в VT, j поза VT
        frontier = [(g[i][j], i, j) for i in sorted(vt)
                    for j in range(n) if j not in vt and g[i][j] != INF]
        w, i, j = min(frontier)          # жадібний вибір
        if trace:
            print(f"Крок {step}:")
            print("  VT =", "{" + ",".join(str(x + 1) for x in sorted(vt)) + "}")
            print("  E  =", " ".join(f"({a + 1},{b + 1})={c}" for c, a, b in
                                      sorted(frontier, key=lambda t: (t[1], t[2]))))
            print(f"  e* = ({i + 1},{j + 1}) = {w}")
        vt.append(j)
        et.append((i + 1, j + 1, w))
        if trace:
            print("  ET =", " ".join(f"({a},{b})={c}" for a, b, c in et))
    return et, sum(w for _, _, w in et)


class DSU:
    """Система неперетинних множин (Union-Find)."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # стиснення шляхів
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


def kruskal(n, edges, trace=False):
    """Алгоритм Крускала: сортуємо ребра за вагою, додаємо ребро, якщо
    воно не утворює цикл (FIND(u) != FIND(v))."""
    e_sorted = sorted((w, u, v) for u, v, w in edges)
    if trace:
        print("E (відсортовані) =", " ".join(f"({u},{v})={w}" for w, u, v in e_sorted))
    dsu = DSU(n)
    et = []
    for w, u, v in e_sorted:
        if len(et) == n - 1:             # ecounter = |V| - 1: дерево побудовано
            break
        ru, rv = dsu.find(u - 1), dsu.find(v - 1)
        if ru != rv:
            dsu.union(ru, rv)
            et.append((u, v, w))
            if trace:
                print(f"({u},{v})={w}: FIND({u})={ru + 1}, FIND({v})={rv + 1} -> додано")
        elif trace:
            print(f"({u},{v})={w}: FIND({u})={ru + 1}, FIND({v})={rv + 1} -> цикл, пропущено")
    return et, sum(w for _, _, w in et)


if __name__ == "__main__":
    g = build_adjacency_matrix(V, EDGES)
    print("Матриця суміжності:")
    print_matrix(g)
    print("\nСписки суміжності:")
    print_lists(build_adjacency_lists(V, EDGES))
    print("\n=== Алгоритм Прима (початок з вершини 1) ===")
    et, total = prim(g, 0, trace=True)
    print("Ребра MST:", " ".join(f"({a},{b})={c}" for a, b, c in et))
    print("Вартість MST:", total)
    print("\n=== Алгоритм Крускала ===")
    et, total = kruskal(V, EDGES, trace=True)
    print("Ребра MST:", " ".join(f"({a},{b})={c}" for a, b, c in et))
    print("Вартість MST:", total)
