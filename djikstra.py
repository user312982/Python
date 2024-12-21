def minimum(dict):
    min_key = list(dict.keys())[0]
    for i in list(dict.keys())[1:]:
        if dict[i] < dict[min_key]:
            min_key = i
    return min_key

def dijkstra(nodes, edges, start, end):
    unexplored = {node: float('inf') for node in nodes}
    unexplored[start] = 0
    previous_nodes = {node: None for node in nodes}
    explored = {}

    while unexplored:
        explore = minimum(unexplored)
        current_distance = unexplored[explore]
        del unexplored[explore]
        explored[explore] = current_distance

        if explore == end:
            break

        for (from_node, to_node), weight in edges.items():
            if from_node == explore and to_node in unexplored:
                check_time = current_distance + weight
                if check_time < unexplored[to_node]:
                    unexplored[to_node] = check_time
                    previous_nodes[to_node] = explore
            elif to_node == explore and from_node in unexplored:
                check_time = current_distance + weight
                if check_time < unexplored[from_node]:
                    unexplored[from_node] = check_time
                    previous_nodes[from_node] = explore

    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    print(f"Prev node: {previous_nodes}")
    print(f"Shortest node from {start} to {end}: {path}")
    return explored[end], path

# Nodes and edges
nodes = ["1", "2", "3", "4", "5", "6", "7", "8"]
edges = {
    ("1", "2"): 5, ("1", "3"): 3, ("1", "4"): 6, ("1", "5"): 10,
    ("2", "5"): 7, ("2", "6"): 9, ("3", "5"): 2, ("3", "6"): 4, ("3", "8"): 6,
    ("4", "6"): 3, ("4", "7"): 8, ("5", "7"): 5, ("5", "8"): 3, ("6", "7"): 11, ("7", "8"): 4
}

# Find the shortest path
distance, target_path = dijkstra(nodes, edges, "1", "8")
print(f"Shortest distance: {distance}")
