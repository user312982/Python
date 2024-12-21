import time
from copy import copy
from prettytable import PrettyTable

def minimum(dict_data):
    min_key = list(dict_data.keys())[0]
    for i in list(dict_data.keys())[1:]:
        if dict_data[i] < dict_data[min_key]:
            min_key = i
    return min_key

def generate_table(iteration, nodes, distances, previous_nodes, current_node, completed_nodes, combined_values):
    table = PrettyTable()
    table.title = f"Iteration {iteration}: Exploring node {current_node}"
    table.field_names = ["Node"] + nodes  # Nodes as header
    
    row = ["Value"]
    
    for node in nodes:
        if distances[node] == float('inf'):
            value = "INF"
        else:
            value = str(distances[node]) + f"/{previous_nodes[node]}" if previous_nodes[node] else str(distances[node])
        
        # Combine the value for the current iteration with the previous ones
        if node in completed_nodes:
            value = f"\033[91m{value}\033[0m"  # Red color for completed nodes

        # Append the value to the combined list for this node
        if node not in combined_values:
            combined_values[node] = []
        combined_values[node].append(value)

        # Stack the values for each node from previous iterations
        value_str = "\n".join(combined_values[node])
        row.append(value_str)

    table.add_row(row)
    return table.get_string()

def dijkstra_with_table(nodes, edges, start, end):
    unexplored = {node: float('inf') for node in nodes}
    unexplored[start] = 0
    previous_nodes = {node: None for node in nodes}
    explored = {}
    iteration = 0
    combined_tables = []
    completed_nodes = set()
    combined_values = {}

    while unexplored:
        iteration += 1
        explore = minimum(unexplored)
        current_distance = unexplored[explore]
        del unexplored[explore]
        explored[explore] = current_distance
        completed_nodes.add(explore)

        # Generate the table for the current iteration
        table = generate_table(iteration, nodes, {**unexplored, **explored}, previous_nodes, explore, completed_nodes, combined_values)

        # Print the table for this iteration
        print(f"\n=== Iteration {iteration} ===")
        print(table)

        # Pause to simulate processing
        time.sleep(1)

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

    # Final results
    print("\n=== Final Combined Table ===")
    for table in combined_tables:
        print(table)

    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    print(f"\nShortest path from {start} to {end}: {path}")
    return explored[end], path

# Nodes and edges
nodes = ["1", "2", "3", "4", "5", "6", "7", "8"]
edges = {
    ("1", "2"): 5, ("1", "3"): 3, ("1", "4"): 6, ("1", "5"): 10,
    ("2", "5"): 7, ("2", "6"): 9, ("3", "5"): 2, ("3", "6"): 4, ("3", "8"): 6,
    ("4", "6"): 3, ("4", "7"): 8, ("5", "7"): 5, ("5", "8"): 3, ("6", "7"): 11, ("7", "8"): 4
}

# Find the shortest path
distance, target_path = dijkstra_with_table(nodes, edges, "1", "8")
print(f"\nShortest distance: {distance}")
