# Example string input. Use it to test your code.
example_input="John is connected to Bryant, Debra, Walter.\
John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
Bryant is connected to Olive, Ollie, Freda, Mercedes.\
Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
Mercedes is connected to Walter, Robin, Bryant.\
Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
Olive is connected to John, Ollie.\
Olive likes to play The Legend of Corgi, Starfleet Commander.\
Debra is connected to Walter, Levi, Jennie, Robin.\
Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.\
Walter is connected to John, Levi, Bryant.\
Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.\
Levi is connected to Ollie, John, Walter.\
Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.\
Ollie is connected to Mercedes, Freda, Bryant.\
Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.\
Jennie is connected to Levi, John, Freda, Robin.\
Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.\
Robin is connected to Ollie.\
Robin likes to play Call of Arms, Dwarves and Swords.\
Freda is connected to Olive, John, Debra.\
Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."


def create_data_structure(string_input):
    '''Parses a block of text and stores relevant information into a data structure.
    
    Arguments: 
        string_input: block of text containing the network information
    
    Returns:
        The newly created network data structure
	'''
    network = {}
    list_input = string_input.split('.')
    for data in list_input:
        user_name = data[0:data.find(' ')]
        if user_name not in network:
            network[user_name] = [[], []]
        information = data[data.find('to') + 3:].split(', ')
        if 'play' in information[0] != -1:
            information[0] = information[0][information[0].find('play') + 5:]
            for game in information:
                network[user_name][1].append(game)
        else:
            for connection in information:
                network[user_name][0].append(connection)
    return network

def get_connections(network, user):
    '''Returns a list of all connections that user have

    Arguments: 
        network: the gamer network data structure
        user: a string containing the name of the user
 
    Return: 
        A list of all connections the user has.

    - If the user has no connections, returns an empty list.
    - If the user is not in network, returns None.
    '''
    if user in network:
        return network[user][0]
    else:
        return None

def get_games_liked(network,user):
    '''Returns a list of all games that user likes

    Arguments: 
        network: the gamer network data structure
        user:    a string containing the name of the user

    Return: 
        A list of all games the user likes.
    
    - If the user likes no games, returns an empty list.
    - If the user is not in network, returns None.
    '''
    if user in network:
        return network[user][1]
    else:
        return None

def add_connection(network, user_A, user_B):
    '''Adds a connection from user_A to user_B. 
    It means that user_B adds to list of connections user_A.

    Arguments: 
        network: the gamer network data structure 
        user_A:  a string with the name of the user the connection is from
        user_B:  a string with the name of the user the connection is to

    Return: 
        The updated network with the new connection added.
    
    - If a connection already exists from user_A to user_B, returns network unchanged.
    - If user_A or user_B is not in network, returns False.
    '''
    if user_A in network and user_B in network:
        if user_B not in network[user_A][0]:
            network[user_A][0].append(user_B)
        return network
    else:
        return False

def add_new_user(network, user, games):
    '''Creates a new user profile and adds that user to the network, along with 
    any game preferences specified in games. Assumed that the user has no connections to begin with.
    
    Arguments:
        network: the gamer network data structure
        user: a string containing the name of the user to be added to the network
        games: a list of strings containing the user's favorite games, e.g.:
               ['Ninja Hamsters', 'Super Mushroom Man', 'Dinosaur Diner']
    
    Returns: 
        The updated network with the new user and game preferences added. The new user should have no connections.
    
    - If the user already exists in network, returns network unchanged (do not change the user's game preferences)
    '''
    if user not in network:
        network[user] = [[], games]
        return network
    else:
        return network

def get_secondary_connections(network, user):
    '''Finds all the secondary connections (i.e. connections of connections) of a given user.
    
    Arguments: 
        network: the gamer network data structure
        user:    a string containing the name of the user
    
    Return: 
        A list containing the secondary connections (connections of connections).
    
    - If the user is not in the network, returns None.
    - If a user has no primary connections to begin with, returns an empty list.
    '''
    if user in network:
        secondary_connections = []
        for connections in network[user][0]:
            for connections_of_connections in network[connections][0]:
                if connections_of_connections not in secondary_connections:
                    secondary_connections.append(connections_of_connections)
        return secondary_connections
    else:
        return None

def count_common_connections(network, user_A, user_B):
    '''Finds the number of people that user_A and user_B have in common.
    Common is people that exists in user_A and user_B connections.

    Arguments: 
        network: the gamer network data structure
        user_A: a string containing the name of user_A
        user_B: a string containing the name of user_B
    
    Return: 
        The number of connections in common (as an integer).
    
    - If user_A or user_B is not in network, return False.
    '''
    if user_A in network and user_B in network:
        common = 0
        for user in network[user_A][0]:
            if user in network[user_B][0]:
                common = common + 1
        return common
    else:
        return False

def find_path_to_friend(network, user_A, user_B, searched=None):
    '''Finds a connections path from user_A to user_B.
    NOTE: it's existing path, not the shortest one.

    Arguments:
        network: The network you created with create_data_structure. 
        user_A:  String holding the starting username ("Abe")
        user_B:  String holding the ending username ("Zed")
    
    Return:
        A list showing the path from user_A to user_B.
        - If such a path does not exist, return None.
        - If user_A or user_B is not in network, return None.
    
    Sample output:
        print find_path_to_friend(network, "Abe", "Zed")
        >>> ['Abe', 'Gel', 'Sam', 'Zed']
        
        This implies that Abe is connected with Gel, who is connected with Sam, 
        who is connected with Zed.
    '''
    if user_A not in network or user_B not in network:
        return None
    searched = searched or []
    searched.append(user_A)
    result = [user_A]
    if user_B in network[user_A][0]:
        return result + [user_B]
    for user in network[user_A][0]:
        if user not in searched:
            newpath = find_path_to_friend(network, user, user_B, searched)
            if newpath:
                return result + newpath
        else:
            continue
    return None

network = create_data_structure(example_input)
