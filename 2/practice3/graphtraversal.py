import matplotlib.pyplot as plt

def build_graph(edges):
    graph = {}
    for e in edges:
        src = e[0]
        dest = e[1]
        if dest not in graph:
            graph[dest] = list()
        if src not in graph:
            graph[src] = list()
        graph[src].append((dest, 0))
    return graph

def in_visited(node, visited):
    return node[0] in [x[0] for x in visited]

def dfs(graph, start, depth):
    visited, stack = [], [(start, 0)]
    while stack:
        vertex = stack.pop()
        if not in_visited(vertex, visited) and vertex[1] <= depth:
            d = vertex[1]
            visited.append(vertex)
            adj = list(map(lambda y: (y[0], d + 1), [x for x in graph[vertex[0]] if not in_visited(x, visited)]))
            stack += adj
    return visited

def bfs(graph, start, depth):
    visited, queue = [], [(start, 0)]
    while queue:
        vertex = queue.pop(0)
        if not in_visited(vertex, visited) and vertex[1] <= depth:
            d = vertex[1]
            visited.append(vertex)
            adj = list(map(lambda y: (y[0], d + 1), [x for x in graph[vertex[0]] if not in_visited(x, visited)]))
            queue += adj
    return visited

edges_path = 'data/edges.csv'
nodes_path = 'data/nodes.csv'
start = '5281959998'

# Loading egdes and nodes
with open(edges_path, 'r') as f:
    edges = list(map(lambda x: x.strip('\n').split(','), f.readlines()))[1:]
with open(nodes_path, 'r') as f:
    nodes = dict(list(map(lambda x: x.strip('\n').split(','), f.readlines()))[1:])
graph = build_graph(edges)

# BFS
tree = list(map(lambda x: (nodes[x[0]], x[1]), bfs(graph, start, 10000)))
levels = [[tree[0]]]
for n in tree[1:]:
    if n[1] == levels[-1][-1][1]:
        levels[-1].append(n)
    else:
        levels += [[n]]
levels.pop(0)
# Plot
plt.bar(range(1, len(levels) + 1),
        [len(x) for x in levels],
        0.4,
        color='g')
ax = plt.subplot()
for i, v in enumerate([len(x) for x in levels]):
    ax.text(i + 1, v + 3, str(v), horizontalalignment='center')
plt.title('Número de nodos por nivel')
plt.show()

# DFS
tree = list(map(lambda x: (nodes[x[0]], x[1]), dfs(graph, start, 10000)))
levels = {0: [[tree[0]]]}
temp = []
for n in tree[1:]:
    if temp == [] or n[1] > temp[-1][1]:
        # build depth path
        temp.append(n)
    else:
        # path ends, must be placed in the correct length list
        if len(temp) in levels:
            levels[len(temp)].append(temp)
        else:
            levels[len(temp)] = [temp]
        temp = []
del levels[0]

# Plot
hist = [len(levels[x]) if x in levels else 0 for x in range(1, max(levels.keys()) + 1)]
plt.bar(range(1, max(levels.keys()) + 1),
        hist,
        0.4,
        color='r')
ax = plt.subplot()
for i, v in enumerate(hist):
    ax.text(i + 1, v + 3, str(v), horizontalalignment='center')
plt.title('Cantidad de caminos por profundidad')
plt.show()
