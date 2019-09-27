# Tacocat is the puuuurveyor of palindromes.  She loves palindrome numbers
# which is why she insisted on many here.
# Rooms is a list of dictionaries with room information.
# We chose to use a list because its mutable and can be altered after its creation. We also wanted to store a lot of data in it.
# Each room is a dictionary because so we can easily access all the values on it without having to map through anything.

import random 


class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y

    def __str__(self):
        s_to = self.s_to
        if s_to:
            s_to = self.s_to.id
        e_to = self.e_to
        if e_to:
            e_to = self.e_to.id
        w_to = self.w_to
        if w_to:
            w_to = self.w_to.id
        n_to = self.n_to
        if n_to:
            n_to = self.n_to.id


        return f"name:{self.name}, description:{self.description}, id:{self.id}, s_to:{s_to}, e_to:{e_to}, w_to:{w_to}, n_to:{n_to},  x:{self.x}, y:{self.y}"

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1 # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west
        hDirection = 1 # 1: north, -1: south  To break the 'zig-zag' pattern


        # Cats are the theme and inspiration
        kittyAdj = ["carpeted", "comfortable", "dank", "palatial", "rambling", "snug", "sprawling",
                  "stark", "vaulted", "warm", "ruined", "modest", "lofty", "handsome",
                  "furnished", "secure", "well-appointed", "desirable", "huge", "narrow",
                  "oceanfront", "private", "quiet", "safe", "tasteful", "stuffy" ]
        kittyRooms = ["Den", "Livingroom", "Garage", "Pantry", "Sewing room", "Hallway",
                    "Kitchen", "Bedroom", "Laundry room", "Entertainment room", "Bathroom",
                    "Patio", "Dining room"]

        # Kool kitty scenarios
        kittyMovement = ["Kitty quietly slinks her way toward the", "Kitty leaps into the", "Kitty rushes into the", 
                          "Kitty meows walking into the", "Kitty hits the ball and it goes into the"]
        kittyExperience = ["Ewww...a dog was in here!", "OMG catnip and tunafish!", "Look at that! Mouse droppings!",
                           "If only there was a bird in here.", "This place needs a pillow",
                           "I think I could nap here for a while", "I wonder what the poor cats are doing today?",
                           "There's no one here to pet me.", "Oh, only dry food here. Pass.", "My toy isn't in here.",
                           "This would be a good place to admire me.", "MEOW!", "Ewww...a human was in here" ]

        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Process for adjusting room direction. Depending on the randon integer 
            newDirection = random.randint(0, 11)
            north = hDirection >= 0
            south = hDirection <= 0

            # depending on the number picked by randint, it will dictate whether the room generation goes
            # north, south, east, or west.

            # Example. If the random int is 9, and we're going south and 
            if newDirection > 7  and south and not self.grid[y-1][x] and y > 1:
                room_direction = "s"
                hDirection = -1
                y -= 1
            elif direction > 0 and x < size_x - 1:
                room_direction = "e"
                hDirection = 0
                x += 1
            elif direction < 2 and x > 0 and not self.grid[y][x-1]:
                hDirection = 0
                room_direction = "w"
                x -= 1
            elif x > 1 and newDirection > 11 and north:
                room_direction = "n"
                hDirection = 1
                y += 1
            else:
                # If we hit a wall, turn north and reverse direction
                if self.grid[y+1][x]:
                    while self.grid[y+1][x]:
                        y += 1
                        previous_room = self.grid[y][x]
                y += 1
                room_direction = "n"
                hDirection = 1
                direction *= -1

            # results ready to print out to user.  An example may read "Kitty leaps into the Bedroom. My toy isn't here."
            kittyRoom = random.choice(kittyAdj) + " " + random.choice(kittyRooms) #name 
            roomOutput = random.choice(kittyMovement) + " " + kittyRoom + ". " + random.choice(kittyExperience) #description

            # results passed to constructor
            room = Room(title=kittyRoom, description=roomOutput, x=x, y=y)
            room.save()
            print(room)
            
            self.grid[y][x] = room

            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)
            if newDirection < 6 and y > 2 and self.grid[y-1][x]:
                room.connect_rooms(self.grid[y-1][x], "s")
            
            previous_room = room
            room_count += 1


    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 101
width = 11
height = 11
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
