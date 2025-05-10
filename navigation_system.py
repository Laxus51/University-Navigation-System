import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import numpy as np
import heapq
import time


class Node:
    def __init__(self, name, x, y, is_room=True):
        self.name = name
        self.x = x
        self.y = y
        self.is_room = is_room
        self.neighbors = {}  # neighbor_node: distance

    def add_neighbor(self, node, distance):
        self.neighbors[node] = distance

    def __lt__(self, other):
        # For priority queue in Dijkstra's algorithm
        return False


class DepartmentGraph:
    def __init__(self):
        self.nodes = {}  # name: Node
        self.load_background_image()
        self.create_nodes()
        self.create_edges()

    def load_background_image(self):
        self.bg_img = mpimg.imread('Map.png')

    def add_node(self, name, x, y, is_room=True):
        self.nodes[name] = Node(name, x, y, is_room)

    def create_nodes(self):
        # Door nodes with coordinates copied from the room nodes
        self.add_node("Library_door", 292, 253, False)
        self.add_node("Exam_Office_door", 482, 137, False)
        self.add_node("Bath_3_door", 547.3, 121, False)
        self.add_node("Room_9_door", 557.3, 117, False)
        self.add_node("Room_8_door", 561.5, 100, False)
        self.add_node("Room_7_door", 561.5, 72, False)
        self.add_node("Faculty_Lounge_door", 561.5, 50, False)
        self.add_node("Room_6_door", 538, 41.5, False)
        self.add_node("Room_5_door", 511, 41.5, False)
        self.add_node("Conference_Room_door", 385, 41, False)
        self.add_node("Bath_2_door", 364.5, 41, False)
        self.add_node("Principal_Office_door", 350, 50, False)
        self.add_node("Room_3_door", 350, 94, False)
        self.add_node("Room_2_door", 350, 133, False)
        self.add_node("Room_1_door", 363, 133, False)
        self.add_node("Bath_1_door", 363, 107, False)
        self.add_node("Treasure_Office_door", 385, 61, False)
        self.add_node("Admission_Office_door", 439.5, 137, False)

        # Additional 30 door nodes for the larger map
        self.add_node("Geology_Lab_door", 301, 407, False)
        self.add_node("1st_Floor_Stairs_door", 301, 483, False)
        self.add_node("Experiment_Lab_door", 229, 392, False)
        self.add_node("Water_Test_Lab_door", 229, 538, False)
        self.add_node("Seminar_Hall_door", 139, 392, False)
        self.add_node("Toxicology_Lab_door", 139, 538, False)
        self.add_node("Biology_Lab_door", 96, 399.5, False)
        self.add_node("Chemistry_Lab_door", 96, 531, False)
        self.add_node("Male_Common_Room_door", 90, 415, False)
        self.add_node("Female_Common_Room_door", 90, 435, False)
        self.add_node("AAS_Lab_door", 90, 481, False)
        self.add_node("Photocopy_Shop_door", 631, 420, False)
        self.add_node("Reception_door", 631, 512, False)
        self.add_node("Room_101_door", 639, 396, False)
        self.add_node("Room_110_door", 639, 534, False)
        self.add_node("Room_102_door", 683, 390, False)
        self.add_node("Culinary_Lab_door", 683, 538, False)
        self.add_node("Room_103_door", 770, 390, False)
        self.add_node("Room_108_door", 770, 538, False)
        self.add_node("Room_104_door", 813, 396.7, False)
        self.add_node("Room_107_door", 813, 533.6, False)
        self.add_node("Room_105_door", 819, 428, False)
        self.add_node("Room_106_door", 819, 499.5, False)
        self.add_node("Computer_Lab_door", 271.5, 530, False)

        # Special corridor nodes
        # Corridor node for main building entry
        self.add_node("1st_Corridor_Main", 461, 227, False)
        # Corridor node for library path
        self.add_node("1st_Corridor_Library", 425, 253, False)
        self.add_node("1st_Corridor_Top", 461, 279, False)
        self.add_node("Main_Entrance", 461, 50, False)  # Main entrance
        self.add_node("2nd_Corridor_Main", 461, 446.5, False)
        self.add_node("2nd_Corridor_Left", 442, 466, False)
        self.add_node("2nd_Corridor_Right", 479, 466, False)

        # 16 Junction nodes to be positioned (not connected yet)
        self.add_node("Junction_1", 356.4, 133, False)  # Placeholder position
        self.add_node("Junction_2", 356.4, 107, False)  # Placeholder position
        self.add_node("Junction_3", 356.4, 94, False)  # Placeholder position
        self.add_node("Junction_4", 356.4, 50, False)  # Placeholder position
        self.add_node("Junction_5", 364.5, 50, False)  # Placeholder position
        self.add_node("Junction_6", 385, 50, False)  # Placeholder position
        self.add_node("Junction_7", 461, 137, False)  # Placeholder position
        self.add_node("Junction_9", 511, 50, False)  # Placeholder position
        self.add_node("Junction_10", 538, 50, False)  # Placeholder position
        self.add_node("Junction_11", 552, 50, False)  # Placeholder position
        self.add_node("Junction_12", 552, 72, False)  # Placeholder position
        self.add_node("Junction_13", 552, 100, False)  # Placeholder position
        self.add_node("Junction_14", 552, 109, False)  # Placeholder position
        self.add_node("Junction_15", 547.3, 109, False)  # Placeholder position
        self.add_node("Junction_16", 461, 109, False)  # Placeholder position

        # Additional junction nodes for the new doors
        self.add_node("Junction_17", 461, 253, False)
        self.add_node("Junction_18", 461, 466, False)
        self.add_node("Junction_19", 301, 466, False)
        self.add_node("Junction_20", 261, 466, False)
        self.add_node("Junction_21", 229, 403, False)
        self.add_node("Junction_22", 139, 403, False)
        self.add_node("Junction_23", 103, 403, False)
        self.add_node("Junction_24", 103, 415, False)
        self.add_node("Junction_25", 103, 435, False)
        self.add_node("Junction_26", 103, 481, False)
        self.add_node("Junction_27", 103, 528, False)
        self.add_node("Junction_28", 139, 528, False)
        self.add_node("Junction_29", 229, 528, False)
        self.add_node("Junction_30", 261, 528, False)
        self.add_node("Junction_31", 643, 466, False)

        # Horizontal corridor for upper left
        self.add_node("Junction_32", 643, 530, False)
        # Vertical corridor for left
        self.add_node("Junction_33", 643, 512, False)
        # Vertical corridor for right
        self.add_node("Junction_34", 643, 420, False)
        self.add_node("Junction_35", 643, 400, False)

        self.add_node("Junction_36", 683, 400, False)
        self.add_node("Junction_37", 770, 400, False)
        self.add_node("Junction_38", 806, 400, False)
        self.add_node("Junction_39", 806, 428, False)
        self.add_node("Junction_40", 806, 499.5, False)
        self.add_node("Junction_41", 806, 530, False)
        self.add_node("Junction_42", 683, 530, False)
        self.add_node("Junction_43", 770, 530, False)
        self.add_node("Junction_44", 261, 403, False)
        self.add_node("Junction_45", 301, 415, False)

    def create_edges(self):
        # Function to calculate Euclidean distance between two nodes
        def calculate_distance(node1, node2):
            return np.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

        # Helper function to connect two nodes
        def connect_nodes(node1_name, node2_name):
            if node1_name in self.nodes and node2_name in self.nodes:
                node1 = self.nodes[node1_name]
                node2 = self.nodes[node2_name]
                distance = calculate_distance(node1, node2)
                node1.add_neighbor(node2, distance)
                node2.add_neighbor(node1, distance)  # Bidirectional connection

        # Manually set a very high distance to force the algorithm to take a different path
        def connect_nodes_with_penalty(node1_name, node2_name, penalty=10.0):
            if node1_name in self.nodes and node2_name in self.nodes:
                node1 = self.nodes[node1_name]
                node2 = self.nodes[node2_name]
                # Add a penalty factor to make this path less desirable
                distance = calculate_distance(node1, node2) * penalty
                node1.add_neighbor(node2, distance)
                node2.add_neighbor(node1, distance)

        # Create a preferred path with reduced distance to make it more attractive
        def connect_nodes_preferred(node1_name, node2_name, discount_factor=0.5):
            if node1_name in self.nodes and node2_name in self.nodes:
                node1 = self.nodes[node1_name]
                node2 = self.nodes[node2_name]
                # Apply a discount factor to make this path more desirable
                distance = calculate_distance(node1, node2) * discount_factor
                node1.add_neighbor(node2, distance)
                node2.add_neighbor(node1, distance)  # Bidirectional connection

        # Clear any existing connections to rebuild them
        for node_name in self.nodes:
            self.nodes[node_name].neighbors = {}

        # First floor connections
        connect_nodes("Main_Entrance", "Junction_7")
        connect_nodes("Junction_7", "Exam_Office_door")
        connect_nodes("Junction_7", "Admission_Office_door")

        # Create a preferred direct path from Main_Entrance to Room 5 area
        connect_nodes_preferred("Main_Entrance", "Junction_9", 0.5)

        # Create a reasonable path from Main_Entrance through proper corridor structure
        # Main_Entrance to corridor junction
        connect_nodes("Main_Entrance", "Junction_6")
        connect_nodes("Junction_6", "Junction_5")  # Follow corridor path
        connect_nodes("Junction_5", "Junction_4")  # Follow corridor path
        connect_nodes("Junction_4", "Junction_3")  # Connect to Room 3 junction
        connect_nodes("Junction_3", "Junction_2")  # Connect to Bath 1 junction

        # First floor horizontal corridor
        connect_nodes("Conference_Room_door", "Junction_6")
        connect_nodes("1st_Corridor_Main", "Junction_7")

        # Connect other doors on first floor
        connect_nodes("Bath_2_door", "Junction_5")
        connect_nodes("Junction_5", "Junction_6")

        connect_nodes("Principal_Office_door", "Junction_4")
        connect_nodes("Junction_4", "Junction_5")

        connect_nodes("Room_3_door", "Junction_3")
        connect_nodes("Junction_3", "Junction_4")

        connect_nodes("Bath_1_door", "Junction_2")
        connect_nodes("Junction_2", "Junction_3")

        # Only connect Junction_1 to Room_1_door, Room_2_door, and Junction_2
        connect_nodes("Room_1_door", "Junction_1")
        connect_nodes("Room_2_door", "Junction_1")
        # Direct connection to Junction_2 only
        connect_nodes("Junction_1", "Junction_2")

        # Remove the direct connection between Junction_4 and Junction_1
        # This forces the path to go through Junction_2

        # Right side corridor
        connect_nodes("Bath_3_door", "Junction_15")
        connect_nodes("Junction_15", "Junction_14")
        connect_nodes("Junction_15", "Junction_16")
        connect_nodes("Room_9_door", "Junction_14")
        connect_nodes("Junction_14", "Junction_13")
        connect_nodes("Room_8_door", "Junction_13")
        connect_nodes("Junction_13", "Junction_12")
        connect_nodes("Room_7_door", "Junction_12")
        connect_nodes("Junction_12", "Junction_11")
        connect_nodes("Faculty_Lounge_door", "Junction_11")

        # Add direct connections between Faculty Lounge area and Principal Office area
        connect_nodes("Junction_11", "Junction_4")

        connect_nodes("Junction_11", "Junction_10")
        connect_nodes("Room_6_door", "Junction_10")
        connect_nodes("Junction_10", "Junction_9")
        connect_nodes("Room_5_door", "Junction_9")

        # Add direct connections from Room 5, 6 junctions to the main corridor
        connect_nodes("Junction_9", "Junction_6")  # Room 5 to main corridor
        connect_nodes("Junction_10", "Junction_6")  # Room 6 to main corridor

        # Connect Room 7, 8, 9 doors to their respective junction nodes
        # Room 7 door to its junction
        connect_nodes("Room_7_door", "Junction_12")
        # Room 8 door to its junction
        connect_nodes("Room_8_door", "Junction_13")
        # Room 9 door to its junction
        connect_nodes("Room_9_door", "Junction_14")

        # Add penalties to undesired paths
        connect_nodes_with_penalty("Junction_9", "Junction_10", 5.0)
        connect_nodes_with_penalty("Junction_10", "Junction_11", 5.0)
        connect_nodes_with_penalty("Junction_11", "Junction_12", 5.0)
        connect_nodes_with_penalty("Junction_12", "Junction_13", 5.0)
        connect_nodes_with_penalty("Junction_13", "Junction_14", 5.0)

        # Treasure office connection
        connect_nodes("Junction_16", "Treasure_Office_door")
        connect_nodes("Main_Entrance", "Junction_16")
        connect_nodes("Junction_16", "Junction_7")

        # Library connections
        connect_nodes("1st_Corridor_Library", "Library_door")
        connect_nodes("1st_Corridor_Main", "1st_Corridor_Library")
        connect_nodes("Junction_17", "Library_door")
        connect_nodes("Junction_17", "Junction_7")

        # Add direct preferred path from Library to Top Corridor
        connect_nodes_preferred("1st_Corridor_Library",
                                "1st_Corridor_Top", 0.5)

        # Vertical connections to second floor
        connect_nodes("1st_Corridor_Main", "Junction_17")
        connect_nodes("Junction_17", "1st_Corridor_Top")
        connect_nodes("1st_Corridor_Top", "2nd_Corridor_Main")

        # Second floor connections
        connect_nodes("2nd_Corridor_Main", "Junction_18")
        connect_nodes("Junction_18", "2nd_Corridor_Left")
        connect_nodes("Junction_18", "2nd_Corridor_Right")

        # Connect Junction_19 to Junction_18 for proper second floor routing
        # Connection through second floor corridor
        connect_nodes("Junction_19", "Junction_18")

        # Left side connections
        # Create preferred path through Junction_20 and Junction_19
        connect_nodes_preferred("Junction_44", "Junction_20", 0.5)
        connect_nodes_preferred("Junction_20", "Junction_19", 0.5)
        connect_nodes("Junction_44", "Junction_21")

        # Add penalty to the path through Junction_45
        connect_nodes_with_penalty("Junction_44", "Junction_45", 5.0)
        connect_nodes_with_penalty("Junction_45", "Geology_Lab_door", 5.0)
        connect_nodes("Junction_21", "Junction_22")
        connect_nodes("Junction_22", "Junction_23")
        connect_nodes("Junction_23", "Junction_24")
        connect_nodes("Junction_24", "Junction_25")
        connect_nodes("Junction_25", "Junction_26")
        connect_nodes("Junction_26", "Junction_27")
        connect_nodes("Junction_27", "Junction_28")
        connect_nodes("Junction_28", "Junction_29")
        connect_nodes("Junction_29", "Junction_30")

        # Door connections on left side
        connect_nodes("Junction_19", "Geology_Lab_door")
        connect_nodes("Junction_17", "Junction_18")
        connect_nodes("Junction_44", "Junction_45")
        connect_nodes("Junction_19", "1st_Floor_Stairs_door")
        connect_nodes("Junction_44", "Experiment_Lab_door")
        connect_nodes("Junction_22", "Seminar_Hall_door")
        connect_nodes("Junction_23", "Biology_Lab_door")
        connect_nodes("Junction_24", "Male_Common_Room_door")
        connect_nodes("Junction_25", "Female_Common_Room_door")
        connect_nodes("Junction_26", "AAS_Lab_door")
        connect_nodes("Junction_27", "Chemistry_Lab_door")
        connect_nodes("Junction_28", "Toxicology_Lab_door")
        connect_nodes("Junction_29", "Water_Test_Lab_door")
        connect_nodes("Junction_30", "Computer_Lab_door")

        # Right side - completely redesigned for proper routing
        # Right side connections with penalties to prevent unwanted routing
        connect_nodes_with_penalty(
            "2nd_Corridor_Right", "Junction_31", 5.0)  # Add high penalty
        connect_nodes("Junction_31", "Junction_32")
        connect_nodes("Junction_32", "Junction_33")
        connect_nodes("Junction_33", "Junction_34")
        connect_nodes("Junction_34", "Junction_35")
        connect_nodes("Junction_35", "Junction_36")
        connect_nodes("Junction_36", "Junction_37")
        connect_nodes("Junction_37", "Junction_38")
        connect_nodes("Junction_38", "Junction_39")
        connect_nodes("Junction_39", "Junction_40")
        connect_nodes("Junction_40", "Junction_41")
        connect_nodes("Junction_41", "Junction_43")
        connect_nodes("Junction_43", "Junction_42")

        connect_nodes("Junction_32", "Room_110_door")
        connect_nodes("Junction_33", "Reception_door")
        connect_nodes("Junction_34", "Photocopy_Shop_door")
        connect_nodes("Junction_35", "Room_101_door")
        connect_nodes("Junction_36", "Room_102_door")
        connect_nodes("Junction_37", "Room_103_door")
        connect_nodes("Junction_38", "Room_104_door")
        connect_nodes("Junction_39", "Room_105_door")
        connect_nodes("Junction_40", "Room_106_door")
        connect_nodes("Junction_41", "Room_107_door")
        connect_nodes("Junction_43", "Room_108_door")
        connect_nodes("Junction_42", "Culinary_Lab_door")

        connect_nodes("Junction_42", "Junction_32")

        # Remove direct connection between Junction_19 and Junction_31 to prevent unwanted routing
        connect_nodes("Junction_20", "Junction_30")

        # Add direct connection between Principal Office area and Room 2 area
        # This fixes the navigation from Faculty Lounge to Room 2
        connect_nodes("Junction_4", "Junction_1")

        # Increase penalties for paths through Junction_31
        connect_nodes_with_penalty("Junction_35", "2nd_Corridor_Right", 10.0)
        connect_nodes_with_penalty("Junction_36", "2nd_Corridor_Right", 10.0)
        connect_nodes_with_penalty(
            "2nd_Corridor_Right", "Junction_31", 20.0)  # Increased penalty

        connect_nodes("Junction_37", "Junction_36")
        connect_nodes("Junction_36", "Junction_35")
        connect_nodes("Junction_35", "Junction_34")
        connect_nodes("Junction_34", "Junction_31")
        connect_nodes("Junction_31", "2nd_Corridor_Right")

        connect_nodes("Room_103_door", "Junction_36")

        connect_nodes("Junction_38", "Junction_37")
        connect_nodes("Junction_39", "Junction_38")

        connect_nodes_with_penalty("Room_103_door", "2nd_Corridor_Right", 50.0)
        connect_nodes_with_penalty("Room_103_door", "2nd_Corridor_Main", 50.0)
        connect_nodes_with_penalty("Junction_37", "2nd_Corridor_Right", 50.0)
        connect_nodes_with_penalty("Junction_37", "2nd_Corridor_Main", 50.0)
        connect_nodes_with_penalty("Junction_38", "2nd_Corridor_Right", 50.0)
        connect_nodes_with_penalty("Junction_38", "2nd_Corridor_Main", 50.0)
        connect_nodes_with_penalty("Junction_39", "2nd_Corridor_Right", 50.0)
        connect_nodes_with_penalty("Junction_39", "2nd_Corridor_Main", 50.0)

        # Create preferred path from 2nd_Corridor_Right to 2nd_Corridor_Main
        connect_nodes_preferred("2nd_Corridor_Right", "2nd_Corridor_Main", 0.5)

    def find_shortest_path(self, start_name, end_name):
        if start_name not in self.nodes or end_name not in self.nodes:
            return None, float('inf')

        # Dijkstra's algorithm
        distances = {node: float('inf') for node in self.nodes.values()}
        distances[self.nodes[start_name]] = 0
        previous = {node: None for node in self.nodes.values()}
        queue = [(0, self.nodes[start_name])]

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node == self.nodes[end_name]:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in current_node.neighbors.items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        # Reconstruct path
        path = []
        current = self.nodes[end_name]

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        if path[0] != self.nodes[start_name]:
            return None, float('inf')

        return path, distances[self.nodes[end_name]]

    def visualize(self, path=None, ax=None, animate=False):
        """
        Visualizes the graph, optionally showing a path.
        Only door nodes are shown, junction nodes and their connections are hidden.
        Only the red path line and yellow door nodes are displayed.

        Parameters:
        - path: List of nodes representing a path
        - ax: Matplotlib axis to draw on (if None, creates a new figure)
        - animate: Whether to animate the path drawing
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(14, 12), facecolor='#f0f0f8')
            standalone = True
        else:
            standalone = False
            fig = ax.figure

        # Create dictionary mapping locations to their nodes
        clickable_nodes = {}

        # Set background color and remove axes
        ax.set_facecolor('#f0f0f8')
        ax.set_xticks([])
        ax.set_yticks([])

        # Add a subtle drop shadow effect to the map
        ax.imshow(self.bg_img, extent=[0, 900, 0, 600], zorder=0)

        # Add a title background
        title_bg = plt.Rectangle(
            (0, 580), 900, 40, facecolor='#3a506b', alpha=0.7, zorder=30)
        ax.add_patch(title_bg)

        # Plot only door nodes and special nodes (not junctions)
        for name, node in self.nodes.items():
            # Skip all junction nodes
            if "Junction" in name:
                continue

            # Skip nodes that are part of the path (they'll be drawn later)
            if path and node in path:
                continue

            # Only draw door nodes, Main_Entrance, and Corridor nodes
            if "door" in name or name == "Main_Entrance" or "Corridor" in name:
                # Door nodes and special corridor nodes in yellow
                ax.scatter(node.x, node.y, c='#ff9e00', edgecolor='white', linewidth=1,
                           s=40, alpha=0.9, zorder=10)
                # No text labels - show only the nodes
                clickable_nodes[(node.x, node.y)] = name

        # If a path is provided, highlight it
        if path:
            # Create a list of visible nodes (non-junction nodes) in the path
            visible_path_nodes = []

            # First, collect all visible nodes in the path (excluding junction nodes)
            for node in path:
                if "Junction" not in node.name:
                    visible_path_nodes.append(node)

            # We don't need to draw a direct line between visible nodes anymore
            # as it creates an incorrect straight line path
            # The actual path with all nodes (including junctions) will be drawn
            # by the animation function in the interactive mode

            # Draw only non-junction nodes in the path with highlighting
            for i, node in enumerate(visible_path_nodes):

                if i == 0:  # Start node
                    ax.scatter(node.x, node.y, c='#06d6a0', edgecolor='white', linewidth=1.5,
                               s=150, marker='*', zorder=30)
                    ax.text(node.x, node.y - 40, "START", color='white', fontweight='bold',
                            horizontalalignment='center', verticalalignment='center', fontsize=12,
                            bbox=dict(facecolor='#06d6a0', alpha=0.9, edgecolor='white',
                                      boxstyle='round,pad=0.3'),
                            zorder=35)
                elif i == len(visible_path_nodes) - 1:  # End node
                    ax.scatter(node.x, node.y, c='#7209b7', edgecolor='white', linewidth=1.5,
                               s=150, marker='*', zorder=30)
                    ax.text(node.x, node.y - 40, "END", color='white', fontweight='bold',
                            horizontalalignment='center', verticalalignment='center', fontsize=12,
                            bbox=dict(facecolor='#7209b7', alpha=0.9, edgecolor='white',
                                      boxstyle='round,pad=0.3'),
                            zorder=35)
                else:  # Door nodes and special corridor nodes in the path
                    ax.scatter(node.x, node.y, c='#ff9e00', edgecolor='white', linewidth=1,
                               s=60, alpha=1.0, zorder=28)

            # Add a legend to explain the node types if not already added
            if standalone:
                from matplotlib.patches import Patch
                from matplotlib.lines import Line2D

                yellow_patch = Patch(color='#ff9e00', label='Door Nodes')
                red_patch = Patch(color='#e94560', label='Path')
                green_patch = Patch(color='#06d6a0', label='Start')
                purple_patch = Patch(color='#7209b7', label='End')

                fig.legend(handles=[yellow_patch, red_patch, green_patch, purple_patch],
                           loc='lower center', ncol=4, bbox_to_anchor=(0.5, 0), fontsize=10)

                plt.subplots_adjust(bottom=0.15)  # Make room for the legend

            # Set title based on path
            # Find first and last non-junction nodes for the title
            visible_path_nodes = [
                node for node in path if "Junction" not in node.name]
            if len(visible_path_nodes) > 0:
                start_node = visible_path_nodes[0]
                end_node = visible_path_nodes[-1]
                ax.set_title(f"Path from {start_node.name.replace('_door', '').replace('_', ' ')} to {end_node.name.replace('_door', '').replace('_', ' ')}",
                             fontsize=18, color='white', fontweight='bold', pad=10)
        else:
            # Set a default title when no path is shown
            ax.set_title("Department Navigation System", fontsize=18,
                         color='white', fontweight='bold', pad=10)

            # Add a legend to explain the node types
            if standalone:
                from matplotlib.patches import Patch
                from matplotlib.lines import Line2D

                yellow_patch = Patch(color='#ff9e00', label='Door Nodes')

                fig.legend(handles=[yellow_patch],
                           loc='lower center', ncol=1, bbox_to_anchor=(0.5, 0), fontsize=10)

                plt.subplots_adjust(bottom=0.15)  # Make room for the legend

        if standalone:
            ax.grid(False)
        plt.tight_layout()
        plt.show()


class NavigationSystem:
    def __init__(self):
        self.graph = DepartmentGraph()
        # Add all door nodes and the Main Entrance to available destination options
        self.available_rooms = [name.replace(
            "_door", "") for name, node in self.graph.nodes.items() if "door" in name]
        self.available_rooms.append("Main Entrance")

        # For the interactive mode
        self.interactive_mode = False
        self.selected_start = None
        self.selected_end = None
        self.current_animation = None  # Store animation reference

    def display_available_rooms(self):
        print("\nAvailable Rooms:")
        for i, room in enumerate(sorted(self.available_rooms), 1):
            print(f"{i}. {room}")

    def navigate(self, start_room, end_room, animate=False):
        # Handle Main Entrance as a special case
        if start_room == "Main Entrance":
            start_node = "Main_Entrance"
        else:
            start_node = f"{start_room}_door"

        if end_room == "Main Entrance":
            end_node = "Main_Entrance"
        else:
            end_node = f"{end_room}_door"

        path, distance = self.graph.find_shortest_path(start_node, end_node)

        if path is None:
            print(f"No path found between {start_room} and {end_room}")
            return

        print(f"\nNavigation from {start_room} to {end_room}:")

        print("\nPath:")
        for node in path:
            name = node.name.replace(
                "_door", "") if "door" in node.name else node.name.replace("_", " ")
            print(f"  → {name}")

        # Visualize the path with animation if requested
        self.graph.visualize(path, animate=animate)

    def run(self):
        """Main entry point - now just directly launches interactive mode"""
        print("Welcome to the Department Navigation System!")
        print("Click on rooms to navigate between them.")
        print("The program will exit when you close the map window.")
        self.run_interactive_mode()

    def run_interactive_mode(self):
        """Run the interactive click-based mode for selecting rooms with improved UI."""
        self.interactive_mode = True
        self.selected_start = None
        self.selected_end = None

        # Create a figure with a modern style for interactive selection
        plt.style.use('ggplot')
        fig = plt.figure(figsize=(16, 12), facecolor='#f0f0f8')

        # Create a grid layout for a more modern UI
        gs = fig.add_gridspec(20, 20)

        # Main map area (larger)
        ax_map = fig.add_subplot(gs[0:20, 0:16], facecolor='#f0f0f8')

        # Side panel for info and controls
        ax_side = fig.add_subplot(gs[0:20, 16:20], facecolor='#e7ecef')
        ax_side.axis('off')

        # Create dictionary mapping locations to their nodes
        clickable_nodes = {}

        # Function to reset the current view without creating a new window
        def reset_view(event=None):
            # Clear any active animation
            if self.current_animation is not None:
                self.current_animation = None

            # Clear the main map axis
            ax_map.clear()

            # Update the side panel
            ax_side.clear()
            ax_side.axis('off')

            # Add side panel title and instructions
            ax_side.text(0.5, 0.95, "Navigation\nSystem", fontsize=18, fontweight='bold',
                         ha='center', va='top', color='#2b2d42')

            # Reset the selection state
            self.selected_start = None
            self.selected_end = None

            # Redraw the background and nodes
            ax_map.imshow(self.graph.bg_img, extent=[0, 900, 0, 600])

            # Style improvements for better readability
            ax_map.set_xticks([])
            ax_map.set_yticks([])

            # Add a title background for better appearance
            title_bg = plt.Rectangle(
                (0, 580), 900, 40, facecolor='#3a506b', alpha=0.7, zorder=30)
            ax_map.add_patch(title_bg)

            # Clear the clickable_nodes dictionary before repopulating
            clickable_nodes.clear()

            # Plot only door nodes and special nodes (not junctions)
            for name, node in self.graph.nodes.items():
                # Skip all junction nodes
                if "Junction" in name:
                    continue

                # Only draw door nodes, Main_Entrance, and Corridor nodes
                if "door" in name or name == "Main_Entrance" or "Corridor" in name:
                    # Door nodes and special corridor nodes in yellow
                    ax_map.scatter(node.x, node.y, c='#ff9e00', edgecolor='white', linewidth=1,
                                   s=40, alpha=0.9, zorder=10)
                    # No text labels - show only the nodes
                    clickable_nodes[(node.x, node.y)] = name

            ax_map.set_title("Click to select START location",
                             fontsize=18, color='white', fontweight='bold', pad=10)

            fig.canvas.draw()

        # Initial setup
        reset_view()

        # Add interactive buttons to side panel
        button_width = 0.3  # Further reduced width
        button_height = 0.03  # Further reduced height

        # Create a nicer-looking reset button in side panel - moved further left and made smaller
        reset_button_ax = fig.add_axes([0.8, 0.2, button_width/2, button_height],
                                       facecolor='#e7ecef')
        reset_button = plt.Button(
            reset_button_ax, 'Reset', color='#f1faee', hovercolor='#a8dadc')
        reset_button.on_clicked(reset_view)

        # Add a button to exit - moved further left and made smaller
        exit_button_ax = fig.add_axes([0.8, 0.12, button_width/2, button_height],
                                      facecolor='#e7ecef')

        def exit_app(event):
            # Clear any active animation
            if self.current_animation is not None:
                self.current_animation = None
            plt.close(fig)

        exit_button = plt.Button(
            exit_button_ax, 'Exit', color='#f1faee', hovercolor='#e63946')
        exit_button.on_clicked(exit_app)

        # Status text in side panel
        status_text = ax_side.text(0.5, 0.35, "", fontsize=12, fontweight='bold',
                                   ha='center', va='center', color='#2b2d42',
                                   bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))

        # Define function to handle clicks with improved visual feedback
        def on_click(event):
            if not event.inaxes or event.inaxes not in [ax_map]:
                return

            x, y = event.xdata, event.ydata

            # Find the closest node to the click
            closest_node = None
            min_distance = float('inf')

            for (node_x, node_y), node_name in clickable_nodes.items():
                distance = np.sqrt((x - node_x)**2 + (y - node_y)**2)
                if distance < min_distance and distance < 30:  # Click must be within 30 units
                    min_distance = distance
                    closest_node = node_name

            if closest_node:
                if self.selected_start is None:
                    self.selected_start = closest_node
                    display_name = closest_node.replace(
                        "_door", "").replace("_", " ")
                    ax_map.set_title(f"Selected START: {display_name} - Now click to select END location",
                                     fontsize=16, color='white', fontweight='bold', pad=10)

                    # Update side panel status
                    status_text.set_text(
                        f"Start: {display_name}\nEnd: Not Selected")

                    # Highlight the selected start node with better visual
                    start_node = self.graph.nodes[closest_node]
                    ax_map.scatter(start_node.x, start_node.y, c='#06d6a0', edgecolor='white', linewidth=1.5,
                                   s=250, marker='*', zorder=30)
                    ax_map.text(start_node.x, start_node.y - 40, "START", color='white', fontweight='bold',
                                horizontalalignment='center', verticalalignment='center', fontsize=12,
                                bbox=dict(facecolor='#06d6a0', alpha=0.9, edgecolor='white',
                                          boxstyle='round,pad=0.3'),
                                zorder=35)

                    fig.canvas.draw()

                elif self.selected_end is None and closest_node != self.selected_start:
                    self.selected_end = closest_node
                    end_display_name = closest_node.replace(
                        "_door", "").replace("_", " ")
                    start_display_name = self.selected_start.replace(
                        "_door", "").replace("_", " ")

                    # Update side panel status
                    status_text.set_text(
                        f"Start: {start_display_name}\nEnd: {end_display_name}\nCalculating path...")
                    fig.canvas.draw()

                    # Clear the figure for the new path with a small delay for UI feedback
                    time.sleep(0.5)  # Brief delay for UI feedback
                    ax_map.clear()

                    # Display the navigation path
                    start_room = self.selected_start.replace(
                        "_door", "").replace("_", " ")
                    end_room = self.selected_end.replace(
                        "_door", "").replace("_", " ")

                    # Handle Main Entrance as a special case
                    if start_room == "Main Entrance":
                        start_node = "Main_Entrance"
                    else:
                        start_node = self.selected_start

                    if end_room == "Main Entrance":
                        end_node = "Main_Entrance"
                    else:
                        end_node = self.selected_end

                    path, distance = self.graph.find_shortest_path(
                        start_node, end_node)

                    if path:
                        # Update side panel with path info
                        status_text.set_text(
                            f"Start: {start_display_name}\nEnd: {end_display_name}\nShowing route...")

                        # Use animation instead of static display
                        # Create a new axis for the map instead of reusing existing one
                        ax_map.clear()

                        # Plot map background
                        ax_map.imshow(self.graph.bg_img,
                                      extent=[0, 900, 0, 600])
                        ax_map.set_xticks([])  # Remove ticks
                        ax_map.set_yticks([])  # Remove ticks

                        # Add a title background
                        title_bg = plt.Rectangle(
                            (0, 580), 900, 40, facecolor='#3a506b', alpha=0.7, zorder=30)
                        ax_map.add_patch(title_bg)

                        # Don't use the visualize method to draw the path line
                        # as it was creating a direct line between visible nodes
                        # Instead, we'll only use it to set up the map and draw door nodes
                        # The actual path will be drawn by the animation function
                        self.graph.visualize(None, ax=ax_map, animate=False)

                        # Update the title
                        ax_map.set_title(f"Path from {start_display_name} to {end_display_name}",
                                         fontsize=18, color='white', fontweight='bold', pad=10)

                        # Format title
                        title = f"Path from {start_room} to {end_room}"
                        ax_map.set_title(
                            title, fontsize=18, color='white', fontweight='bold', pad=10)

                        # Prepare path coordinates for animation
                        path_x = [node.x for node in path]
                        path_y = [node.y for node in path]

                        # Create empty line for animation with a solid color
                        line, = ax_map.plot([], [], linewidth=5, alpha=0.9, zorder=20,
                                            solid_capstyle='round', color='#e94560')

                        # Make sure the line is empty at the beginning and set flag
                        line.set_data([], [])
                        self._animation_completed = False

                        # Modified animation update function with completion tracking
                        def update(num):
                            # Draw the path up to this segment
                            if num > 0:  # Need at least 2 points to make a line
                                # Update the line data with increasing portions of the path
                                line.set_data(path_x[:num+1], path_y[:num+1])

                                # Highlight the node we just reached
                                if num < len(path):
                                    node = path[num]
                                    if "door" in node.name:
                                        ax_map.scatter(node.x, node.y, c='#ff9e00', edgecolor='white', linewidth=1.5,
                                                       s=100, alpha=1.0, zorder=25)
                                    elif "Junction" in node.name:
                                        # Show junction nodes when they're part of the path with proper highlighting
                                        ax_map.scatter(node.x, node.y, c='#4cc9f0', edgecolor='white', linewidth=1.0,
                                                       s=80, alpha=0.8, zorder=25)

                                        # Extract junction number for cleaner labels
                                        junction_num = node.name.split(
                                            '_')[1] if '_' in node.name else ''
                                        label_text = f"J{junction_num}"

                                        # Add text label with junction number
                                        ax_map.text(node.x, node.y, label_text, color='black',
                                                    fontweight='bold', fontsize=8,
                                                    horizontalalignment='center', verticalalignment='center',
                                                    zorder=26)
                                    elif not "Junction" in node.name:
                                        ax_map.scatter(node.x, node.y, c='#4361ee', edgecolor='white', linewidth=1.5,
                                                       s=100, alpha=1.0, zorder=25)

                            # Mark animation as completed on last frame
                            if num == len(path) - 1:
                                self._animation_completed = True
                                # Ensure the full path is visible
                                line.set_data(path_x, path_y)

                                # Draw all special nodes in the path
                                for node in path:
                                    if "door" in node.name:
                                        ax_map.scatter(node.x, node.y, c='#ff9e00', edgecolor='white', linewidth=1.5,
                                                       s=100, alpha=1.0, zorder=25)
                                    elif "Junction" in node.name:
                                        # Show junction nodes when they're part of the path with proper highlighting
                                        ax_map.scatter(node.x, node.y, c='#4cc9f0', edgecolor='white', linewidth=1.0,
                                                       s=80, alpha=0.8, zorder=25)

                                        # Extract junction number for cleaner labels
                                        junction_num = node.name.split(
                                            '_')[1] if '_' in node.name else ''
                                        label_text = f"J{junction_num}"

                                        # Add text label with junction number
                                        ax_map.text(node.x, node.y, label_text, color='black',
                                                    fontweight='bold', fontsize=8,
                                                    horizontalalignment='center', verticalalignment='center',
                                                    zorder=26)
                                    elif not "Junction" in node.name:
                                        ax_map.scatter(node.x, node.y, c='#4361ee', edgecolor='white', linewidth=1.5,
                                                       s=100, alpha=1.0, zorder=25)

                            return (line,)

                        # Create the animation - use Matplotlib's robust approach to prevent issues
                        self.current_animation = animation.FuncAnimation(
                            fig, update, frames=len(path), interval=300,
                            blit=True, repeat=False)

                        # Define a function to run when animation completes
                        def on_animation_complete(event=None):
                            # Explicitly redraw the full path
                            line.set_data(path_x, path_y)
                            # Manually trigger a redraw
                            fig.canvas.draw_idle()

                        # Add event to be triggered after the last frame (estimated time)
                        timer = fig.canvas.new_timer(
                            interval=300 * len(path) + 100)
                        timer.add_callback(on_animation_complete)
                        timer.start()

                        # Force a draw to ensure animation starts
                        fig.canvas.draw()
                    else:
                        print(
                            f"No path found between {start_room} and {end_room}")
                        # Reset selection to let the user try again
                        self.selected_start = None
                        self.selected_end = None
                        ax_map.set_title("No path found. Click to select START room",
                                         fontsize=16, color='white', fontweight='bold', pad=10)

                        # Update side panel status
                        status_text.set_text(
                            "Error: No path found\nPlease try again")

                        # Restore map view
                        reset_view()

        # Connect the click event to the figure
        cid = fig.canvas.mpl_connect('button_press_event', on_click)

        # Add a title to the window
        fig.canvas.manager.set_window_title('Department Navigation System')

        # Display the UI
        plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
        plt.show()

        # Reset interactive mode
        self.interactive_mode = False
        self.selected_start = None
        self.selected_end = None


if __name__ == "__main__":
    # Set a modern matplotlib style
    plt.style.use('ggplot')

    # Create and run the navigation system
    nav_system = NavigationSystem()
    nav_system.run()

    print("Thank you for using the Department Navigation System!")
    # Program will exit when the interactive map window is closed
