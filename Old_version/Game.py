import numpy as np
import random

# Find all available sites for the executive
def find_avail_points(board, executive):
	directions = np.array([[0, 1], [0, -1], [ 1, 0], [-1,  0],
							[1, 1], [1, -1], [-1, 1], [-1, -1]])
	possible_move = {}

	for row in range(8):
		for column in range(8): 
			psb = False         
			if board[row][column] == 0:  		# Available place
				temp_pts = []                   # Temporary changed pieces
				# Loop through all directions
				for dirc in directions:
					dirc_pts = []
					checkr, checkc = row + dirc[0], column + dirc[1]

					if checkr < 0 or checkr > 7 or checkc < 0 or checkc > 7:
						continue
					# If there is a opposite pieces at one direction, check the piece after that.
					while board[checkr][checkc] == -executive:
						dirc_pts.append([checkr, checkc])
						checkr, checkc = checkr + dirc[0], checkc + dirc[1]
							
						if checkr < 0 or checkr > 7 or checkc < 0 or checkc > 7 or board[checkr][checkc] == 0:
							break		
						# If there is another executive's piece at this direction, record the site 
						# and sites to be reversed
						if board[checkr][checkc] == executive:
							psb = True
							temp_pts.extend(dirc_pts)
							break
			# Build dictionary				
			if psb:	
				possible_move[(row, column)] = temp_pts		

	return possible_move

# Define the priority of sites
def priority():
	priority_dict = {}
	pri_0 = [(0, 1), (1, 0), (1, 1), (0, 6), (1, 7), (1, 6), (6, 0), (7, 1), (6, 1), (6, 7), (7, 6), (6, 6)]
	pri_3 = [(0, 0), (0, 7), (7, 0), (7, 7)]
	for i in range(8):
		for j in range(8):
			priority_dict[(i, j)] = 1
			# Try to put piece at boundaries
			if i == 0 or i == 7 or j == 0 or j == 7:
				priority_dict[(i, j)] = 2
			# Always try not to put piece next to corner	
			if (i, j) in pri_0: 
				priority_dict[(i, j)] = 0
			# Always try to put piece at corner
			if (i, j) in pri_3 :
				priority_dict[(i, j)] = 3
	return priority_dict

# The AI function, returns a site and sites to be reversed
def computer_player(board, executive, priority_dict):
	possible_move = find_avail_points(board, executive)
	change_pieces = 0
	priority = 0
	move_list = []
	choose_site = []

	# Find sites with highest priority
	for key in possible_move.keys():
		if priority_dict[key] > priority:
			move_list = []
			move_list.append(key)
			priority = priority_dict[key]
		elif priority_dict[key] == priority:
			move_list.append(key)

	# Find sites reverse most pieces
	for move in move_list:
		reverse_number = len(possible_move[move])
		if reverse_number > change_pieces:
			choose_site = []
			choose_site.append(move)
			change_pieces = reverse_number
		elif reverse_number == change_pieces:
			choose_site.append(move)

	# Randomly choose one site if there are multiple sites
	# If no possible site, return None
	if len(choose_site) > 0:
		site = random.choice(choose_site)
		reverse_site = possible_move[site]
		return site, reverse_site
	else:
		return None, None
