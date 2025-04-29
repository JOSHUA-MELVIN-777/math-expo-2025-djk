from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

# Dijkstra's Algorithm
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission and show results
@app.route('/calculate', methods=['POST'])
def calculate():
    # Get user input
    num_nodes = int(request.form['num_nodes'])
    nodes = [request.form[f'node{i}'] for i in range(1, num_nodes + 1)]
    
    graph = {node: [] for node in nodes}
    
    edges = request.form['edges'].strip().splitlines()
    for edge in edges:
        src, dest, weight = edge.split()
        weight = int(weight)
        if src in nodes and dest in nodes:
            graph[src].append((dest, weight))
            graph[dest].append((src, weight))  # For undirected graph

    start_node = request.form['start_node']
    
    if start_node not in nodes:
        return render_template('index.html', error="Starting node is not in the graph!")

    # Compute the shortest paths
    shortest_distances = dijkstra(graph, start_node)
    
    return render_template('index.html', shortest_distances=shortest_distances, nodes=nodes, start_node=start_node)

if __name__ == '__main__':
    app.run(debug=True)
