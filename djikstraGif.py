import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

    return explored[end], path

def draw_graph(nodes, edges, shortest_path=None, output_file="graph_animation.gif"):
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node)

    for (from_node, to_node), weight in edges.items():
        graph.add_edge(from_node, to_node, weight=weight)

    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, ax=ax)

        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)

        if shortest_path and frame <= len(shortest_path) - 1:
            path_edges = list(zip(shortest_path[:frame + 1], shortest_path[1:frame + 2]))
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2, ax=ax)

    ani = FuncAnimation(fig, update, frames=len(shortest_path) if shortest_path else 1, interval=1000, repeat=False)
    ani.save(output_file, writer="pillow")
    plt.close(fig)

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
print(f"Path: {target_path}")

# Draw the graph with the shortest path highlighted and save as GIF
draw_graph(nodes, edges, shortest_path=target_path, output_file="shortest_path.gif")
