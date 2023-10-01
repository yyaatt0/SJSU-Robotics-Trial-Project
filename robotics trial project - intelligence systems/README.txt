***THIS CODE WAS DONE THROUGH THE ASSISTANCE OF CHATGPT***

*Initial Steps*
    - I first download the example code to test out and learn the syntax of python
    - Watch tutorial videos on learning the syntax of python
    - Made an endpoint object, similar to the obstacle object, but if the rover hits the endpoint, the program would end
    - Made the user have 2 different options to run manually or autonomously
            i. The manual selection uses the same movemement code from the example code but implemented when the rover hits the, it will end
            ii. Made a randomly generated endpoint

*Steps with CHATGPT*
    - Using the a* search algorithm, I asked CHATGPT to implement the algorithm into my existing code.
    - Created a draw path function to see the path of the rover
        - Copied the manual movement program over to the autonomous location
        - Implemented the draw path function to see the path
    - I run the code and if there were errors, I would debug and correct the errors
        - If I could not, I would ask CHATGPT to fix my code by pasting the entire code over
        - I read what CHATGPT suggest to fix and fix it, but if it does not work, I would repeat the steps
    - I needed to add how many collisions and steps the rover took so I added a variable to count them
        - Placed those variables when in the if statements that checks if it is okay to move or it is a collision
    - I needed to understand the a* algorithm to implement a counter for steps and collisions
        - Asked CHATGPT to explain what each main component of the function was 
        - Figured out how to implement it with a few adjustments of the code
        - Had to check if Python functions can be either pass by value or reference, but learned that it is neither
        - Had the a* function return valeus of the path, number of steps, and number of collisions
    - Adjusted the main function to get the return values by the a* function and implemented a print function to return the values in the console
    - The function would only print the path, not animate the path for the user to see
    - Ask CHATGPT to implement a function to draw an animated path in real time
        - Pasted the code in and tested for it to work
        - If it didn't, I would ask CHATGPT the same question with the same code provided till something worked
    - Rewrote and simplified the autonomous program in the main function
        - Wrote when the program was drawing the path and when it hits the endpoint, it will end the while loop and print in the console the rover's stats

    - If something doesn't work or something I did not understand, I would ask CHATGPT to explain the code of a snippet I pasted in

*Example Questions + Response from CHATGPT*
    - Question: Fix the animate function where the program can draw the path in real time.
        Response: # Animates the path on the grid
                    def animate_path(path, rover, obstacles, endpoint):
                        for node in path:
                            new_x, new_y = node
                            dx = new_x - rover.x
                            dy = new_y - rover.y

                            if 0 <= new_x < NUM_COLS and 0 <= new_y < NUM_ROWS and not is_collision(Rover(new_x, new_y), obstacles):
                                rover.move(dx, dy)

                            screen.fill(WHITE)
                            draw_grid()
                            draw_obstacles(obstacles)
                            rover.draw()
                            endpoint.draw()
                            draw_path(path)  # Redraw the entire path in each frame
                            pygame.display.flip()
                            clock.tick(5)

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    return

    - Question: Fix my code so a* algorithm works.
        Response: "I've reviewed your code and identified a couple of issues that need to be fixed to make the A* algorithm work correctly:
                    The main issue is that the heuristic function is trying to access attributes x and y of the Node object, but the Node class doesn't have these attributes. You should modify the heuristic function to work with the state of the nodes, which is a tuple representing the position (x, y).
                    You need to add logic to skip nodes that are already in the closed set when expanding neighbors in the A* algorithm.
                    Here's the modified code with these issues fixed:"

                    # Modify the heuristic function to work with node states
                    def heuristic(node, endpoint):
                        return abs(node.state[0] - endpoint.x) + abs(node.state[1] - endpoint.y)

                    # ...

                    def astar(start, goal, obstacles):
                        open_list = []
                        closed_set = set()

                        start_node = Node(start, None)
                        start_node.g = 0
                        start_node.h = heuristic(start_node, goal)  # Pass the node to the heuristic function
                        start_node.f = start_node.g + start_node.h

                        heapq.heappush(open_list, start_node)

                        while open_list:
                            current_node = heapq.heappop(open_list)

                            if current_node.state == goal:
                                path = []
                                while current_node:
                                    path.append(current_node.state)
                                    current_node = current_node.parent
                                return path[::-1]  # Reverse the path to the start of the beginning

                            closed_set.add(current_node.state)

                            # Checks around for neighbors
                            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                                new_x, new_y = current_node.state[0] + dx, current_node.state[1] + dy
                                new_state = (new_x, new_y)

                                if (
                                    0 <= new_x < NUM_COLS
                                    and 0 <= new_y < NUM_ROWS
                                    and new_state not in closed_set  # Check if the new state is not in the closed set
                                    and not is_collision(Rover(new_x, new_y), obstacles)
                                ):
                                    neighbor_node = Node(new_state, current_node)
                                    neighbor_node.g = current_node.g + 1
                                    neighbor_node.h = heuristic(neighbor_node, goal)  # Pass the node to the heuristic function
                                    neighbor_node.f = neighbor_node.g + neighbor_node.h

                                    heapq.heappush(open_list, neighbor_node)

                        return None

    Question: What is the purpose of the Node class in the code above?
    Response: The Node class in the A* algorithm implementation serves as a data structure to represent nodes in the search graph. Each node in the graph corresponds to a state, which could be a particular position in a grid, for example. The purpose of the Node class is to encapsulate information about a state, its parent (the state that led to the current state), the cost to reach that state from the start, and the heuristic estimate of the cost from that state to the goal.

                Here's a breakdown of the key attributes and purposes of the Node class:

                state: This attribute represents the state associated with the node. In the context of pathfinding, this state could be a position (e.g., (x, y) coordinates) on a grid, representing where the search algorithm currently is.
                parent: The parent attribute points to the node that led to the current node in the search. This is used to reconstruct the path once the goal state is reached. By tracing back from the goal node to the start node through the parent pointers, you can determine the sequence of states that make up the optimal path.
                cost: The cost attribute represents the cumulative cost to reach the current state from the start state. In pathfinding, this cost often represents the distance or cost associated with moving from the start state to the current state. It is typically the sum of the edge costs encountered along the path.
                heuristic: The heuristic attribute represents an estimate of the cost from the current state to the goal state. This estimate guides the A* algorithm in selecting which nodes to explore next. It encourages the algorithm to prioritize nodes that seem promising in terms of reaching the goal quickly. The choice of heuristic can significantly affect the algorithm's efficiency.
                In summary, the Node class bundles together essential information about a state and its associated costs and is used to keep track of the search progress, construct the optimal path, and make informed decisions about which states to explore next during the A* search.

*Reflection*
    With an AI tool, it helps people who are interested in doing something and help them actively do so. I first did not know how to write Python,
    but using CHATGPT helped me gain of scope and familiarity of writing the Python's syntax. Python, being an open-source language, makes it easy to pull
    and implement a variety of different functions, but concepts differ from other languages, like Java and C++. CHATGPT helps answer questions and writes
    a blueprint for the user to add themselves to their code. There has to be a tweak or two made by the programmer, which helps users get hands-on learning
    of something new. From CHATGPT, it is not perfect, so asking multiple times will eventually lead to a close enough solution for the user to use. 
    CHATGPT also help implement and teach me new algorithms that I was unfamiliar with. When actively reading the algorithm and asking CHATGPT
    what each part meant, helped me learn the process of the program.