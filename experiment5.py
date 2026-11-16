import random, heapq, json
from functools import cmp_to_key
INF = float('inf')


def random_graph(n, m, seed):
    rnd = random.Random(seed)
    edges = set()
    order = list(range(n)); rnd.shuffle(order)
    for i in range(1, n):                       # випадкове кістякове дерево (зв'язність)
        a, b = order[i], order[rnd.randrange(i)]
        edges.add((min(a, b), max(a, b)))
    while len(edges) < m:
        a, b = rnd.sample(range(n), 2)
        edges.add((min(a, b), max(a, b)))
    ws = list(range(1, len(edges) + 1)); rnd.shuffle(ws)   # різні ваги -> єдине MST
    return [(u, v, w) for (u, v), w in zip(sorted(edges), ws)]


def prim_matrix(n, edges):
    g = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        g[u][v] = g[v][u] = w
    key = [INF] * n; used = [False] * n; key[0] = 0; ops = 0; total = 0
    for _ in range(n):
        u = -1
        for v in range(n):
            ops += 1
            if not used[v] and (u == -1 or key[v] < key[u]): u = v
        used[u] = True; total += key[u]
        for v in range(n):
            ops += 1
            if not used[v] and g[u][v] < key[v]: key[v] = g[u][v]
    return total, ops


class Item(tuple):
    """Елемент купи: підраховує кількість порівнянь, виконаних купою."""
    cmp = 0
    def __lt__(self, other):
        Item.cmp += 1
        return tuple.__lt__(self, other)


def prim_heap(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w)); adj[v].append((u, w))
    Item.cmp = 0
    used = [False] * n; h = [Item((0, 0))]; total = 0
    while h:
        w, u = heapq.heappop(h)
        if used[u]: continue
        used[u] = True; total += w
        for v, ww in adj[u]:
            if not used[v]:
                heapq.heappush(h, Item((ww, v)))
    return total, Item.cmp


def kruskal(n, edges):
    cnt = [0]
    def cmp(a, b):
        cnt[0] += 1
        return (a[2] > b[2]) - (a[2] < b[2])
    es = sorted(edges, key=cmp_to_key(cmp))
    parent = list(range(n)); finds = [0]
    def find(x):
        finds[0] += 1
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    total = 0; k = 0
    for u, v, w in es:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; total += w; k += 1
            if k == n - 1: break
    return total, cnt[0] + finds[0]


if __name__ == "__main__":
    rows = []
    for kind, sizes in (("rare", [100, 200, 400, 800]), ("dense", [100, 200, 400])):
        for n in sizes:
            m = 3 * n if kind == "rare" else n * n // 4
            e = random_graph(n, m, 17)
            a, b, c = prim_matrix(n, e), prim_heap(n, e), kruskal(n, e)
            assert a[0] == b[0] == c[0]
            rows.append(dict(kind=kind, n=n, m=len(e), prim_m=a[1], prim_h=b[1], kr=c[1], w=a[0]))
            print(rows[-1])
    json.dump(rows, open('exp5.json', 'w'))
