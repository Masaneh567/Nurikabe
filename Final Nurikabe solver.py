#!/usr/bin/env python
# coding: utf-8

# In[22]:


#Putting all the functions together: 
import copy


# In[1]:


def setup_nurikabe(clues,n):

   #Takes Nurikabe as a 1D list of clues. Returns it in 2D list in nxn form. 
    
    
    puzzle = [[-1 for j in range(n)] for j in range(n)]  # sets up puzzle so undetermined cells are represented as -1
    
    for i in range(len(clues)):
        row = i // n
        col = i % n
        if clues[i] != 0:  
            puzzle[row][col] = clues[i]
    
    return puzzle


# In[2]:


setup_nurikabe([0,0,0,0,0,0,0,0,0,0,0,5,0,2,0,0,3,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,5,0,0,0],6)


# In[3]:


def island_of_one(puzzle,n): 
    #islands of one are simply a simple clue of 1 given in the grid means adjacent cells should be water and marked as 0. 
    
    for row in range(1,len(puzzle)-1,1): 
        for col in range(1,len(puzzle)-1,1): 
            if puzzle[row][col] == 1:  # this section deals with islands of one that are not on edges of the grid and confirms the 4 adjacent cells as water by making them 0. 
                puzzle[row][col-1] = 0 
                puzzle[row][col+1] = 0 
                puzzle[row-1][col] = 0 
                puzzle[row+1][col] = 0 
                #works up to this point 
                #now to confirm the edge islands of one 
                
                #first confirming islands of one on the top row and bottom row. (excluding if the island of one is in corners.)
    for i in range(1,n-1): 
        if puzzle[0][i] == 1: 
            puzzle[0][i-1] = 0 
            puzzle[0][i+1] = 0 
            puzzle[1][i] = 0  
        # bottom row now excluding corners
        if puzzle[n-1][i] == 1: 
            puzzle[n-1][i-1] = 0 
            puzzle[n-1][i+1] = 0 
            puzzle[n-2][i] = 0 
         
        # now to do the same with first column 
        if puzzle[i][0] == 1: 
            puzzle[i-1][0] = 0 
            puzzle[i+1][0] = 0 
            puzzle[i][1] = 0 
        # and last column 
        
        if puzzle[i][n-1] == 1: 
            puzzle[i-1][n-1] = 0 
            puzzle[i+1][n-1] = 0 
            puzzle[i][n-2] = 0 
            
    # now to do the same for the 4 corner cells if they are an island of one 
    if puzzle[0][0]==1: #top left
        puzzle[0][1]=0 
        puzzle[1][0]=0 
        
    if puzzle[0][n-1]== 1: #top right
        puzzle[0][n-2]=0 
        puzzle[1][n-1]=0 
    
    if puzzle[n-1][0]==1: #bottom left
        puzzle[n-2][0]=0 
        puzzle[n-1][1]=0 
        
    if puzzle[n-1][n-1]==1: #bottom right
        puzzle[n-2][n-1]=0 
        puzzle[n-1][n-2]=0 
    
    return puzzle
                


# In[4]:


def clues_separated_by_one(puzzle,n):
    

    for row in range(n):
        for col in range(1, n-1):  
            if puzzle[row][col] == -1:  # Check if the cell is undetermined and see if it seperates clues horizontally.
                if puzzle[row][col-1] > 0 and puzzle[row][col+1] > 0:
                    puzzle[row][col] = 0

    # Vertical check
    for col in range(n):
        for row in range(1, n-1):  
            if puzzle[row][col] == -1:  
                if puzzle[row-1][col] > 0 and puzzle[row+1][col] > 0:
                    puzzle[row][col] = 0
    
    return puzzle


# In[5]:


def diagonal_clues(puzzle,n): 
    #if 2 clues are diagonally adjacent then the cells which touch both clues must be water 
    # this function will check diagonals from top left down to bottom right and start with these diagonalls leading from the cells in the first row. 
    #it will then continue and do this checking diagonalls from top left to bottom right starting with cells in the first column, except the first cell which was alsready checked. 
    #after it will check diagonals from top right to bottom left in the same way.  
    
    #checking the diagonals starting in first row, from top left to bottom right iterating. 
    for starting_cell in range(n-1): 
        for i in range(0,n-starting_cell-1): 
            if puzzle[i][starting_cell+i] > 0 and puzzle[i+1][starting_cell+i+1] > 0 : 
                puzzle[i][starting_cell+i+1]=0 #makes cell to the right of the first checked clue water
                puzzle[i+1][starting_cell+i]=0 #makes the cell below water
    
    #checking the diagonals starting in the first column from left to right downwards. the logic is the same. 
    for starting_cell in range(1, n-1):  # Start from 1 so dont repeat the first diagonal
        for i in range(n - starting_cell - 1):
            if puzzle[starting_cell + i][i] > 0 and puzzle[starting_cell + i + 1][i + 1] > 0:
                puzzle[starting_cell + i + 1][i] = 0
                puzzle[starting_cell + i][i + 1] = 0
                
    #checking the diagonals from down from right to left starting from row one second column
    for starting_cell in range(1, n):  # iterated over columns from the second to the last
        for i in range(starting_cell):
            if puzzle[i][starting_cell - i] > 0 and puzzle[i + 1][starting_cell - i - 1] > 0:
                puzzle[i + 1][starting_cell - i] = 0
                puzzle[i][starting_cell - i - 1] = 0 
                
    #diagonals from right most column down and left diagonally iterating
    for starting_cell in range(1,n-1): 
        for i in range(n - starting_cell -1): 
            if puzzle[starting_cell +i][n-i-1] > 0 and puzzle[starting_cell+i +1][n-i-2] > 0 : 
                    puzzle[starting_cell +i][n-i-2]= 0 
                    puzzle[starting_cell +i+1][n-i-1]= 0 
                    
                
    return puzzle
                


# In[6]:


def surrounded_square(puzzle,n): 
    for row in range(1,len(puzzle)-1,1): # checks if squares not on the edges of the grid are surrounded by water and if so confirms this squ as water
        for col in range(1,len(puzzle)-1,1): 
            if puzzle[row][col] == -1 and puzzle[row][col-1]== 0 and puzzle[row][col+1]== 0 and puzzle[row-1][col]== 0 and puzzle[row+1][col]== 0: 
                puzzle[row][col]= 0 
    
    #now checking the edges excluding corners 
    #top row
    for i in range(1,n-1): 
        if puzzle[0][i] == -1 and puzzle[0][i-1] == 0 and puzzle[0][i+1] == 0 and puzzle[1][i] == 0: 
                puzzle[0][i]=0 
             
             
              
        # bottom row now excluding corners
        if puzzle[n-1][i] == -1 and puzzle[n-1][i-1] == 0 and puzzle[n-1][i+1]== 0 and puzzle[n-2][i]== 0:  
            puzzle[n-1][i]=0
            
              
        # now to do the same with first column 
        if puzzle[i][0] == -1 and puzzle[i-1][0] == 0 and puzzle[i+1][0] == 0 and puzzle[i][1] == 0: 
             puzzle[i][0]= 0
             
             
             
        # and last column 
        
        if puzzle[i][n-1] == -1 and puzzle[i-1][n-1] == 0 and puzzle[i+1][n-1] == 0 and puzzle[i][n-2] == 0:  
            puzzle[i][n-1] = 0 
             
             
    
    # now to do the same for the 4 corner cells if they are surrounded by water 
    if puzzle[0][0]== -1 and puzzle[0][1]==0 and puzzle[1][0]==0: #top left 
        puzzle[0][0]= 0 
         
         
        
    if puzzle[0][n-1]== -1 and puzzle[0][n-2]==0 and puzzle[0][n-2]==0 and puzzle[1][n-1]==0: #top right 
        puzzle[0][n-1]=0
         
         
    
    if puzzle[n-1][0]== -1 and puzzle[n-2][0]==0 and puzzle[n-1][1]==0: #bottom left  
        puzzle[n-1][0]= 0
        
         
         
        
    if puzzle[n-1][n-1]== -1 and puzzle[n-2][n-1]==0 and puzzle[n-1][n-2]==0: #bottom right
         puzzle[n-1][n-1]= 0
         
    
    return puzzle


# In[7]:


def expand_water(puzzle, n): 
    
    updated_puzzle = [row[:] for row in puzzle]

    for row in range(n):
        for col in range(n):
            if puzzle[row][col] == 0:
                blocked_sides = 0
                expand_to = None  
                
                if row > 0: #makes sure to not check above if we are in the top row as that would be out of index
                    if puzzle[row - 1][col] > 0:
                        blocked_sides += 1
                    elif puzzle[row - 1][col] == -1:
                        expand_to = (row - 1, col)
                else: # if we are in the top row row =  0 then increment blocked sides by 1 as this is essentially blocked
                    blocked_sides += 1

                # same applies for checking below you must ensure not in the bottom row 
                if row < n - 1: 
                    if puzzle[row + 1][col] > 0:
                        blocked_sides += 1
                    elif puzzle[row + 1][col] == -1:
                        expand_to = (row + 1, col)
                else:
                    blocked_sides += 1

                # check left 
                if col > 0:
                    if puzzle[row][col - 1] > 0:
                        blocked_sides += 1
                    elif puzzle[row][col - 1] == -1:
                        expand_to = (row, col - 1)
                else:
                    blocked_sides += 1

                # finally check right
                if col < n - 1:
                    if puzzle[row][col + 1] > 0:
                        blocked_sides += 1
                    elif puzzle[row][col + 1] == -1:
                        expand_to = (row, col + 1)
                else:
                    blocked_sides += 1

                # Expand water if three sides are blocked
                if blocked_sides == 3 and expand_to is not None:
                    updated_puzzle[expand_to[0]][expand_to[1]] = 0

    return updated_puzzle


# In[8]:


#Now logical filling of cells is at and end and the beginnng of the backtracker 


# In[9]:


def find_adjacent_undetermined(puzzle, n): #this is to determine cells in a more intuative way.
    # First pass: look for undetermined cells adjacent to islands
    for i in range(n):
        for j in range(n):
            if puzzle[i][j] == -1:
                # Check if adjacent to an island cell
                adjacent_to_island = False
                directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]  # Right, Down, Up, Left
                for di, dj in directions:
                    ni, nj = i + di, j + dj  # New indices
                    if 0 <= ni < n and 0 <= nj < n and isinstance(puzzle[ni][nj], tuple):
                        adjacent_to_island = True
                        break
                if adjacent_to_island:
                    return (i, j)
    
    # Second pass: look for any undetermined cell if no adjacent ones found
    for i in range(n):
        for j in range(n):
            if puzzle[i][j] == -1:
                return (i, j)
    
    return None

# Use this modified function in your backtracker


# In[10]:


# new initialisation function to get ready for backtracking:  
# This initialisation was later realised that it is essential in order to implement a backtracker as i needed some way to identify if islands with the same clue do not merge together by accident. 
# a rule of nurikabe is that different islands cannot be touching, with my initial set up two islands with clues of the same number could be touching without recognition as the same number wouldnt flag up seperate islands next to one another. 
def assign_unique_ids(puzzle, n):
    unique_id_counter = 1  # Start with 1 for the first unique ID
    
    for i in range(n):
        for j in range(n):
            if isinstance(puzzle[i][j], int) and puzzle[i][j] > 1:  #theres an island clue present 
                # the islands pf 1 dont need to have ID as they are surrounded by water in logical stages 
                # assign a unique number ID alongside the clue number 
                puzzle[i][j] = (puzzle[i][j], unique_id_counter)
                unique_id_counter += 1  # Prepare the next unique ID for the next island clue
                
    return puzzle


# In[11]:


def are_islands_adjacent(puzzle, n):
    
    #Checks if any two different islands (identified by unique IDs) are improperly adjacent to each other.
    
    
    for i in range(n):
        for j in range(n):
            current_cell = puzzle[i][j]
            # Only interested in island cells (ignore water and undetermined cells)
            if isinstance(current_cell, tuple):
                current_id = current_cell[1]  # get the unique ID
                # check adjacent cells right and down to avoid double checks 
                 
                 
                
                if j < n - 1: # only check adjacent cell on the right if it is within bounds 
                    right_cell = puzzle[i][j+1] 
                    #print(right_cell)
                    if isinstance(right_cell, tuple) and right_cell[1] != current_id: #comparing the cell to the rights ID to current
                        return False 
                
                if i < n - 1: #only check down if cell below is within bounds 
                    down_cell = puzzle[i+1][j] 
                    #print(down_cell)
                    if isinstance(down_cell, tuple) and down_cell[1] != current_id: 
                        return False    
                ''''    
                if j == n-1: # if in final col then check down only
                    if isinstance(down_cell, tuple) and down_cell[1] != current_id: 
                        return False '''
                    
                
                    
                    
    
    return True  # No adjacent islands found


# In[12]:


def check_islands_overfilled(puzzle, n): # the next 3 functions work together to validate if islands are overfull or disconnected. 
    island_counts = {}  # Maps unique_id to count of cells
    island_sizes = {}  # Maps unique_id to the island's clue number (expected size)

    for i in range(n):
        for j in range(n):
            cell = puzzle[i][j]
            if isinstance(cell, tuple):  # If the cell is part of an island
                clue_number, unique_id = cell
                island_counts[unique_id] = island_counts.get(unique_id, 0) + 1
                island_sizes[unique_id] = clue_number # assigns the value of clue_number to the key unique_id within the island_sizes dictionary.

    # Check if any island's cell count exceeds its clue number
    for unique_id, count in island_counts.items():
        if count > island_sizes[unique_id]:
            return False  # Island is overfilled

    return True  # No islands are overfilled


# In[13]:


def dfs(puzzle, n, i, j, visited, unique_id):
    if i < 0 or i >= n or j < 0 or j >= n:  # Out of bounds
        return
    if visited[i][j] or not isinstance(puzzle[i][j], tuple):  # Already visited or not part of an island
        return
    if puzzle[i][j][1] != unique_id:  # Different island
        return
    
    visited[i][j] = True  # Mark as visited
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]  # Right, Down, Up, Left
    for di, dj in directions:
        dfs(puzzle, n, i + di, j + dj, visited, unique_id)

def are_islands_connected(puzzle, n):
    visited = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cell = puzzle[i][j]
            if isinstance(cell, tuple) and not visited[i][j]:  # If it's an unvisited island cell
                unique_id = cell[1]
                dfs(puzzle, n, i, j, visited, unique_id)
                # After DFS, check if there are any unvisited cells with the same unique_id
                for x in range(n):
                    for y in range(n):
                        if isinstance(puzzle[x][y], tuple) and puzzle[x][y][1] == unique_id and not visited[x][y]:
                            return False  # Found an unvisited cell of the same island, so it's not fully connected
    return True


# In[14]:


def dfs_water(puzzle, n, i, j, visited):
    #DFS to explore water connectivity 
    
    # Base conditions: Check if the current cell is out of bounds or already visited
    if i < 0 or i >= n or j < 0 or j >= n or visited[i][j]:
        return
    
    # Mark the current cell as visited
    visited[i][j] = True
    
    # Continue only if the current cell is water
    if puzzle[i][j] == 0 or puzzle[i][j] == -1:
        # Explore adjacent cells: up, down, left, right
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for di, dj in directions:
            dfs_water(puzzle, n, i + di, j + dj, visited)

def is_water_connected(puzzle, n):
    
    #Checks if all water cells in the puzzle are connected.
    
  
    
    
    visited = [[False for _ in range(n)] for _ in range(n)]
    
    # Find the first water cell to start the DFS
    found_water = False
    for i in range(n):
        for j in range(n):
            if puzzle[i][j] == 0:
                dfs_water(puzzle, n, i, j, visited)
                found_water = True
                break
        if found_water:
            break
    
    # If no water cell is found, then it's considered connected by default
    if not found_water:
        return True
    
    # Check if there are any unvisited water cells after the DFS
    for i in range(n):
        for j in range(n):
            if puzzle[i][j] == 0 and not visited[i][j]:
                # Found an unvisited water cell, indicating disconnected water regions
                return False
                
    return True  # All water cells are connected


# In[15]:


def island_options(puzzle, n): # makes 0 the final index of the island options list. 
    list_cell_guesses = []  # Start with an empty list for island cells
    
    # Collect island cell guesses first
    for i in range(n):
        for j in range(n):
            cell = puzzle[i][j]
            if isinstance(cell, tuple):  # If the cell is part of an island
                # Add island cells (tuples) to the list of guesses
                list_cell_guesses.append(cell)
    
    # Append water cell (0) as the last option
    list_cell_guesses.append(0)
    
    return list_cell_guesses


# In[16]:


def backtrack(puzzle,guesses,n): 
    puzzle_copy = copy.deepcopy(puzzle)
    #guesses = island_options(puzzle,n) 
    #find = find_cell(puzzle,n) 
    find = find_adjacent_undetermined(puzzle, n)
    if not find: 
        return True, puzzle
    else: 
        row, col = find 
        
    for guess in guesses: 
        puzzle_copy = copy.deepcopy(puzzle) 
        if is_it_valid2(puzzle_copy, guess, (row,col),n) is True: 
            puzzle[row][col]= guess 
            #print(puzzle) 
            
            if backtrack(puzzle,guesses,n): 
                return True
            
            puzzle[row][col] = -1 # resets if path isnt found. 
            
    return False 


# In[17]:


# need a function to count the number of each cell unique ID and also count the number of undetermined cells. 

def check_islands_underfilled(puzzle, n):
    island_counts_2 = {}  # Maps unique_id to count of cells belonging to the island
    island_sizes_2 = {}  # Maps unique_id to the island's clue number (expected size)
    undetermined_cells_count = 0  # Count of undetermined cells
    
    # Iterate through the puzzle to populate island_counts and island_sizes
    for i in range(n):
        for j in range(n):
            cell = puzzle[i][j]
            if isinstance(cell, tuple):  # If the cell is part of an island
                clue_number, unique_id = cell
                island_counts_2[unique_id] = island_counts_2.get(unique_id, 0) + 1
                if unique_id not in island_sizes_2:
                    island_sizes_2[unique_id] = clue_number
            elif cell == -1:  # If the cell is undetermined
                undetermined_cells_count += 1

    # Check if any island is underfilled
    for unique_id, clue_number in island_sizes_2.items():
        island_count = island_counts_2[unique_id]
        # The sum of island cells and undetermined cells should not be less than the clue number
        if clue_number > island_count + undetermined_cells_count:
            return False  # It's impossible to complete the island with the remaining cells

    return True  # It's still possible to complete all islands

            
check_islands_underfilled([[0, 0, 1, 0, 0], [0, (3, 1), 0, (2, 2), 0], [0, (3, 1), 0, 0, 0], [0, (3, 1), 0, (2, 3), 0], [0, 0, 0, (2, 3), 0]],5)            
            


# In[18]:


def is_it_valid2(puzzle, guess, position ,n): 
    
    # inputting the guess 
    temp_puzzle = copy.deepcopy(puzzle)
    row,col = position 
    #copy 
    temp_puzzle[row][col] = guess
    
    #NO 2X2 AREA OF BLACK CHECKER 
    
    # Iterate through the grid, stopping before the last row and column
    # to ensure we don't go out of bounds when checking 2x2 areas.
    for row in range(n - 1):
        for col in range(n - 1):
            # Check the current 2x2 square
            if temp_puzzle[row][col] == 0 and                temp_puzzle[row][col + 1] == 0 and                temp_puzzle[row + 1][col] == 0 and                temp_puzzle[row + 1][col + 1] == 0:
                return "2x2 black" , False  # Found a 2x2 area of 0s, not a valid configuration 
            
    # ARE ISLANDS OVERFILLED 
    island_counts = {}  # Maps unique_id to count of cells
    island_sizes = {}  # Maps unique_id to the island's clue number (expected size)

    for i in range(n):
        for j in range(n):
            cell = temp_puzzle[i][j]
            if isinstance(cell, tuple):  # If the cell is part of an island
                clue_number, unique_id = cell
                island_counts[unique_id] = island_counts.get(unique_id, 0) + 1
                island_sizes[unique_id] = clue_number # assigns the value of clue_number to the key unique_id within the island_sizes dictionary.

    # Check if any island's cell count exceeds its clue number
    for unique_id, count in island_counts.items():
        if count > island_sizes[unique_id]:
            return "overfilled island", False  # Island is overfilled  
        
        
    
    # ARE THERE TOUCHING ISLANDS OF DIFF ID 
    for i in range(n):
        for j in range(n):
            current_cell = temp_puzzle[i][j]
            # Only interested in island cells (ignore water and undetermined cells)
            if isinstance(current_cell, tuple):
                current_id = current_cell[1]  # get the unique ID
                # check adjacent cells right and down to avoid double checks 
                 
                 
                
                if j < n - 1: # only check adjacent cell on the right if it is within bounds 
                    #print('cell on right checked')
                    right_cell = temp_puzzle[i][j+1] 
                    #print(right_cell)
                    if isinstance(right_cell, tuple) and right_cell[1] != current_id: #comparing the cell to the rights ID to current
                        return False, "touching"
                
                if i < n - 1: #only check down if cell below is within bounds 
                    #print('cell below checked')
                    down_cell = temp_puzzle[i+1][j] 
                    #print(down_cell)
                    if isinstance(down_cell, tuple) and down_cell[1] != current_id: 
                        return False, "touching" 
        
    
    # ARE ISLANDS CONNECTED 
    
    visited = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cell = temp_puzzle[i][j]
            if isinstance(cell, tuple) and not visited[i][j]:  # If it's an unvisited island cell
                unique_id = cell[1]
                dfs(temp_puzzle, n, i, j, visited, unique_id)
                # After DFS, check if there are any unvisited cells with the same unique_id
                for x in range(n):
                    for y in range(n):
                        if isinstance(temp_puzzle[x][y], tuple) and temp_puzzle[x][y][1] == unique_id and not visited[x][y]:
                            return "disconnected island", False  # Found an unvisited cell of the same island, so it's not fully connected
        
    # IS WATER CONNECTED 
    visited_water = [[False for _ in range(n)] for _ in range(n)]
    
    # Find the first water cell to start the DFS
    found_water = False
    for i in range(n):
        for j in range(n):
            if temp_puzzle[i][j] == 0:
                dfs_water(temp_puzzle, n, i, j, visited_water)
                found_water = True
                break
        if found_water:
            break
    
    # If no water cell is found, then it's considered connected by default
    if not found_water:
        return True
    
    # Check if there are any unvisited water cells after the DFS
    for i in range(n):
        for j in range(n):
            if temp_puzzle[i][j] == 0 and not visited_water[i][j]:
                # Found an unvisited water cell, indicating disconnected water regions
                return False 
    
    #ARE ISLANDS UNDERFILLED 
    
    island_counts_2 = {}  # Maps unique_id to count of cells belonging to the island
    island_sizes_2 = {}  # Maps unique_id to the island's clue number (expected size)
    undetermined_cells_count = 0  # Count of undetermined cells
    
    # Iterate through the puzzle to populate island_counts and island_sizes
    for i in range(n):
        for j in range(n):
            cell = temp_puzzle[i][j]
            if isinstance(cell, tuple):  # If the cell is part of an island
                clue_number, unique_id = cell
                island_counts_2[unique_id] = island_counts_2.get(unique_id, 0) + 1
                if unique_id not in island_sizes_2:
                    island_sizes_2[unique_id] = clue_number
            elif cell == -1:  # If the cell is undetermined
                undetermined_cells_count += 1

    # Check if any island is "undefilled"
    for unique_id, clue_number in island_sizes_2.items():
        island_count = island_counts_2[unique_id]
        # The sum of island cells and undetermined cells should not be less than the clue number
        if clue_number > island_count + undetermined_cells_count:
            return False  # It's impossible to complete the island with the remaining cells

    
    
    return True # if it passes all tests


# In[19]:


# function to take the tuples and just rewrap them and single value entries without unique ID after function has solved 
def rewrap(puzzle,n): 
    for row in range(n): 
        for col in range(n): 
            cell = puzzle[row][col]
            if isinstance(cell,tuple) :  
                cell_value = cell[0] 
                puzzle[row][col] = cell_value 
    return puzzle


# In[20]:


# now to put all of it together: 

def solve(clues,n): # input a 1d list of clues, and size of nurikabe grid edge n  
    #logical water fill in from clues 
    puzzle = setup_nurikabe(clues,n) 
    puzzle = island_of_one(puzzle,n)  
    puzzle = clues_separated_by_one(puzzle,n) 
    puzzle = diagonal_clues(puzzle,n) 
    puzzle = surrounded_square(puzzle,n) 
    puzzle = expand_water(puzzle, n) 
    #initialise the puzzle into tuple data format in order to work with backtracking algorithm 
    puzzle = assign_unique_ids(puzzle, n) 
    guesses = island_options(puzzle,n)
    #print(puzzle)
    backtrack(puzzle,guesses,n) 
    rewrap(puzzle,n)
    return puzzle
    
    
    


# In[23]:


#5x5 solved
solve([3,0,0,0,1,0,0,0,0,0,0,2,0,2,0,0,0,0,0,0,3,0,0,0,1],5) #5x5 solved


# In[24]:


#6x6 solved
solve([0,0,0,0,0,0,0,1,0,0,0,0,5,0,3,0,0,0,0,0,0,0,0,0,0,0,2,0,0,6,0,0,0,0,0,0],6) 


# In[25]:


#7x7 solved
solve([0,0,4,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,4,0,2,0,0,0,0,0,3,0,0,5,0,0,0,0,2,0,0,0,0,0,0],7) 


# In[26]:


#7x7 solved almost instantly
solve([0,0,2,0,2,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,4,0,0],7)


# In[28]:


puzzle = [
    [-1, -1, -1, -1, 1, -1],
    [-1, -1, 3, -1, -1, -1],
    [-1, 2, -1, 2, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [2, -1, 2, -1, 4, -1],
    [-1, -1, -1, -1, -1, -1]
] 

island_of_one(puzzle,6) 
clues_separated_by_one(puzzle,6) 
diagonal_clues(puzzle,6)

print(puzzle)


# In[ ]:




