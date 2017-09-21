def build_graph(edges):
    graph = {}
    for e in edges:
        src = e[0]
        dest = e[1]
        if dest in graph:
            graph[dest]['likes'].append(src)
        else:
            graph[dest] = {
                'PR': 0.0,
                'C': 0,
                'likes': [src]
            }

        if src in graph:
            graph[src]['C'] += 1
        else:
            graph[src] = {
                'PR': 0.0,
                'C': 1,
                'likes': []
            }
    return graph

def PR(node, graph, d):
    s = 0
    for n in graph[node]['likes']:
        s += graph[n]['PR'] / graph[n]['C']
    return (1 - d) + d * s


def PR_graph(graph, d, it):
    nodes = list(graph.keys())
    l = len(nodes)
    for i in range(l * it):
        n = nodes[i % l]
        graph[n]['PR'] = PR(n, graph, d)
    return graph

# Loading egdes and nodes
edges_path = 'data/edges.csv'
nodes_path = 'data/nodes.csv'
d = 0.85
it = 1000
with open(edges_path, 'r') as f:
    edges = list(map(lambda x: x.strip('\n').split(','), f.readlines()))[1:]
with open(nodes_path, 'r') as f:
    nodes = dict(list(map(lambda x: x.strip('\n').split(','), f.readlines()))[1:])
graph = build_graph(edges)

# Calculating PR
new_graph = PR_graph(graph, d, it)
influences = sorted(new_graph, key=lambda x: new_graph[x]['PR'], reverse=True)

print('Most influential:')
for i in range(5):
    node_id = influences[i]
    node_name = nodes[node_id]
    print(node_name + ': ' + str(graph[node_id]['PR']))
print()

# Average
average = 0
for node in new_graph.values():
    average += node['PR']
average /= len(new_graph.values())
print('Average: ' + str(average))
