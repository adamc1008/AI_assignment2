import networkx as nx
import matplotlib.pyplot as plt
import random
import sys

def generate_small_world_graph(n, k, p):
    return nx.watts_strogatz_graph(n, k, p)

def plot_random_graph(G, filename):
    pos = nx.spring_layout(G, scale=100)  # Position nodes using Fruchterman-Reingold force-directed algorithm
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors)
    #plt.show()
    plt.savefig("graph1.png")
    plt.close()

def assign_colors(G, colors):
    color_map = {}
    for node in G.nodes():
        color_map[node] = random.choice(colors)
    nx.set_node_attributes(G, color_map, 'color')

def count_conflicts(G):
    conflicts = 0
    for u, v in G.edges():
        if G.nodes[u]['color'] == G.nodes[v]['color']:
            conflicts += 1
    return conflicts

def change_node_colour(G,colors):
    available_colours = colors[:]
    for node in G.nodes():
        conflict = False
        for neighbour in G.neighbors(node):
            if G.nodes[neighbour]['color'] in available_colours:
                available_colours.remove(G.nodes[neighbour]['color'])

            if G.nodes[neighbour]['color'] == G.nodes[node]['color']:
                conflict = True
        if conflict and len(available_colours) > 0:
            G.nodes[node]['color'] = random.choice(available_colours)
        elif conflict and len(available_colours) <= 0:
            G.nodes[node]['color'] = random.choice(colors)

    
    return G

def cause_collision(G, num_nodes):
    for _ in range(num_nodes):
        random_node_id = random.choice(list(G.nodes())) 
        random_node = G.nodes[random_node_id] 

        neighbor_id = random.choice(list(G.neighbors(random_node_id)))
        neighbor_color = G.nodes[neighbor_id]['color']  

        random_node['color'] = neighbor_color
    
    return G

def main():
    n = 20  # Number of nodes
    k = 6  # Each node is connected to its k nearest neighbors in a ring topology
    p = 0.2 # Probability of rewiring each edge
    num_colors = 2  # Number of colors
    max_iterations = 3000
    iterations = 0

    G = generate_small_world_graph(n, k, p)
    colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple'][:num_colors]  
    assign_colors(G, colors)
    conflicts = count_conflicts(G)

    with open('output.txt', 'w') as f:
        sys.stdout = f  # Redirect standard output to the file
        
        print("2 colours ", end=',',file=f)

        while conflicts > 0:
            print(conflicts, end=',')
            G = change_node_colour(G, colors)
            conflicts = count_conflicts(G)
            iterations += 1

            if iterations >= max_iterations:
                iterations = 0  # Reset iteration counter
                num_colors += 1  # Increase the number of colors
                colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple'][:num_colors]  # Update colors
                assign_colors(G, colors)
                print("," + str(iterations))
                print("\n" + str(num_colors) + " colours", end=',',file=f)

            if(conflicts==0):
                plot_random_graph(G, "graph_40_run1.png")
                

            
    with open('output_collisions.txt', 'w') as f:
        sys.stdout = f  # Redirect output to the file
        for _ in range(21):
            for i in range(1,11):
                G = cause_collision(G,i)
                conflicts = i
                iterations = 0
                print(str(i) + " nodes changed: ", end=',')
                while conflicts > 0:
                    G = change_node_colour(G, colors)
                    conflicts = count_conflicts(G)
                    iterations += 1

                    if(conflicts==0):
                        print(str(iterations) + "\n", flush = True)
                        filename = f"graph_{i}_nodes.png"
                        plot_random_graph(G,filename)

    sys.stdout = sys.__stdout__



if __name__ == "__main__":
    main()
