# University Department Navigation System

This navigation system provides visual pathfinding between different rooms in the department using the department's floor plan.

## Features

- Interactive CLI interface for room selection
- Visual representation of the shortest path between rooms
- Display of the complete department map with all rooms and connections
- Distance calculation between locations

## Requirements

- Python 3.6+
- Required Python packages:
  - matplotlib
  - numpy
  - networkx

## Installation

1. Make sure you have Python 3.6 or higher installed
2. Install the required packages:

```bash
pip install matplotlib numpy networkx
```

3. Make sure the following files are in the same directory as the navigation_system.py script:
   - DSA_MAP.png (Department floor plan)
   - connections_graph.jpg (Used for reference during development)
   - demo.jpg (Used for reference during development)

## Usage

1. Run the program:

```bash
python navigation_system.py
```

2. The system will display a list of available rooms
3. Choose an option:
   - Option 1: Find the shortest path between two rooms
   - Option 2: View the complete department map
   - Option 3: Exit the program

4. When finding a path, select the starting room and destination room by entering their corresponding numbers

## Room Navigation

The system uses Dijkstra's algorithm to find the shortest path between rooms, considering:
- Room entrances (doors)
- Hallway junctions
- The walkable purple area shown in the floor plan

The navigation highlights the path on the department map and displays:
- Start and end points
- Path segments
- Total distance

## Notes

- Blue dots represent rooms
- Green dots represent doors and hallway junctions
- When a path is displayed, red dots and lines highlight the navigation route 