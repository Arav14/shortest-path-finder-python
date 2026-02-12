import curses               # For terminal handling
from curses import wrapper  # To initialize and clean up the terminal
import queue                # For implementing BFS ( Breadth-First Search )
import time                 # For adding delays


maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def print_maze(maze, stdscr, path=[]):  # Function to print the maze on the terminal
    # Define color pair for blue text on black background
    BLUE = curses.color_pair(1)
    # Define color pair for red text on black background
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):  # Iterate through each row of the maze
        for j, value in enumerate(row):  # Iterate through each cell in the row
            if (i, j) in path:  # If the cell is part of the path
                # Print the path with red color
                stdscr.addstr(i, j*2, "X", RED)
            else:
                # Print the cell value at the correct position
                stdscr.addstr(i, j*2, value, BLUE)


def find_start(maze, start):  # Function to find the starting point in the maze
    for i, row in enumerate(maze):  # Iterate through each row of the maze
        for j, value in enumerate(row):  # Iterate through each cell in the row
            if value == start:  # If the cell matches the starting point
                return (i, j)  # Return the coordinates of the starting point
    return None  # If not found, return None


def find_path(maze, stdscr):  # Function to find the shortest path in the maze using BFS
    start = "O"  # Starting point in the maze
    end = "X"  # Ending point in the maze
    start_pos = find_start(maze, start)  # If the starting point is found

    q = queue.Queue()  # Create a queue for BFS
    q.put((start_pos, [start_pos]))  # Enqueue the starting position and path

    visited = set()  # Set to keep track of visited positions

    while not q.empty():  # While there are positions to explore
        current_pos, path = q.get()  # Dequeue the next position and path
        row, col = current_pos  # Get the current row and column

        stdscr.clear()  # Clear the terminal screen
        print_maze(maze, stdscr, path)  # Print the maze with the current path
        time.sleep(0.2)  # Add a delay to visualize the pathfinding process
        stdscr.refresh()  # Refresh the screen to show changes

        if maze[row][col] == end:  # If the current position is the end point
            return path  # Return the path to the end point

        # Find valid neighboring positions
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:  # Iterate through each neighbor
            if neighbor in visited:  # If the neighbor has already been visited, skip it
                continue  # Skip to the next neighbor

            r, c = neighbor  # Get the row and column of the neighbor
            if maze[r][c] == "#":  # If the neighbor is a wall, skip it
                continue

            # Create a new path including the neighbor
            new_path = path + [neighbor]
            # Enqueue the neighbor and the new path
            q.put((neighbor, new_path))
            visited.add(neighbor)  # Mark the neighbor as visited

# Function to find valid neighboring positions in the maze


def find_neighbors(maze, row, col):
    neighbors = []  # List to store valid neighboring positions

    if row > 0:
        neighbors.append((row - 1, col))  # UP
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))  # DOWN
    if col > 0:
        neighbors.append((row, col - 1))  # LEFT
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))  # RIGHT

    return neighbors  # Return the list of valid neighbors


def main(stdscr):  # Main function to run the program, stdscr is the standard screen object from curses
    # Define color pair for blue text on black background
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # Red text on black background
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    blue_and_black = curses.color_pair(1)  # Store the color pair for later use

    find_path(maze, stdscr)  # Call the function to find the path in the maze
    stdscr.getch()  # Wait for user input


wrapper(main)  # Initialize curses and call the main function
