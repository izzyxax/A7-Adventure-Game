# Starter code for an adventure type game.
# University of Utah, David Johnson, 2017.
# This code, or code derived from this code, may not be shared without permission.

import sys, pygame, math

# Define some words to act as a key into a dictionary of character-related data. I could
# use "image" as a key, but sometimes it is nice to avoid "".
IMAGE = 0
RECT = 1
POSITION = 2
VISIBLE = 3
PHRASE = 4

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frame_counts = []
    padding = math.ceil(math.log(number_of_frames-1,10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding,'0') +".png"
        frame_counts.append(pygame.image.load(folder_and_file_name).convert_alpha())
                             
    return frame_counts

# Check for overlap between non-transparent pixels in sprite and the pixels in image that are
# in the rectangle and a certain color.
def pixel_collision( sprite, sprite_rect, image, color):
    # Figure out where the upper-left corner of the sprite_rect is
    x_offset, y_offset = sprite_rect.topleft
    for row_pos in range(sprite.get_height()):
        for col_pos in range(sprite.get_width()):
            if sprite.get_at((col_pos, row_pos))[3] > 0 and image.get_at((col_pos+x_offset,row_pos+y_offset)) == color:
                return True
    return False

# Take an x,y pos on the map and return a (x_index, y_index) tuple that says which pixel index they would be over
def map_position_to_minimap_index( pos, tile_size ):
    return (int(pos[0]/tile_size), int(pos[1]/tile_size))

# Simple way of getting some character phrases on the screen. The go away when the frame count is higher than
# the phrase's count. say_phrases is a list of the form [("phrase", cutoff_frame_count)]
def render_phrases( say_phrases, frame_count, screen, myfont):
    phrase_position = screen.get_height() - 80
    for index in range(len(say_phrases)):
        if say_phrases[index][1] > frame_count:
            label = myfont.render(say_phrases[index][0], True, (255,255,0))
            screen.blit(label, (screen.get_width()//2 - 100, phrase_position))
            phrase_position += 20

barriers = {"wall": (158,158,158), "door": (77,58,52),"desk_chair": (99,99,99),"desk": (82,67,52),
            "blanket": (33,54,69),"bed_frame": (130,109,88),"counter": (77,73,71),"can": (158,138,120),
            "fridge" :(168,167,165),"sink":(189,188,187),"table_chair_drawer":(64,57,51),"stool": (153,110,75), "Testing Wall":(184,158,136,225)}






# The main loop handles most of the game    
def main():
    
    
    frame_number = 0
    # Initialize pygame                                 
    pygame.init()


    

    #MUSIC
#    pygame.mixer.music.load("Stardew-Valley - Fall (Raven's Descent).mp3")
#    pygame.mixer.music.play(-1)

    
    # Load in the background image
    world = pygame.image.load("Rooms/Rooms.png")
    Big_rect = world.get_rect()

    # Store window width and height in different forms for easy access
    world_size = world.get_size()
    #print(world_size)
    Wsize_x,Wsize_y = (world_size)
    

    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    world_rect = world.get_rect()
    #print(world_rect)
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode(world_size)

    map_tile_width = 30
    map_tile_height = 20
    tile_size = 32
    screen_size = width, height = (map_tile_width*tile_size, map_tile_height*tile_size)
    
    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)
    
    # create the hero character
    # We treat the hero differently than all the other sprite characters as it doesn't move
    hero = load_piskell_sprite("Items/Hero",12)
    hero_rect = hero[0].get_rect()
    
    # Place the hero at the center of the screen
    hero_rect.center = (width/2, height/2)

    # Put all the characters in a dictionary so we can pass to functions easily
    character_data = {}

    # Add All Characters

    #Safe
    safe_image = pygame.image.load("Items/Safe.png")
    safe_rect = safe_image.get_rect()
    safe_pos = (800,800)

    safe = {IMAGE:safe_image, RECT:safe_rect, POSITION:safe_pos, VISIBLE:True, PHRASE:"You got the key to the Front Door!"}
    character_data["safe"] = safe
    


    # This is our standard character data - it is a dictionary of
    # an {IMAGE, RECT, POSITION, VISIBLE, optional PHRASE}. The ALL CAPS keys are defined at
    # the top of this file. They are really numbers. Words make more sense to read but I get
    # frustrated having to put quotes around the words. So the variables act as the word and the
    # value in the variable acts as the key.

    # add in a treasure item
    #treasure_image = pygame.image.load("images/treasurechest.png").convert_alpha()
    # Note that we can add characters to the character dictionary without making a lot of variables
    #character_data["treasure"] = {IMAGE:treasure_image, RECT:treasure_image.get_rect(), POSITION:(1000, 500), VISIBLE:False, PHRASE:"Spend your coin wisely!"}


    # Add a place to hold screen phrases
    say_phrases = []
    
    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Counts how many times the game loop has repeated. Used to animate sprites
    frame_count = 0;

    # variable to show if we are still playing the game
    playing = True

    # variable to show which way I am moving
    is_facing_right = True # False means left
    is_faceing_up = True #False means down
    
    # capture ghost variable
    game_state = {}
    
    # Need to set all state variables here so that they are in the dictionary
    game_state["got ghost"] = False
    game_state["Safe is open!"] = False

    # Define where the hero is positioned on the big map
    screen_x, screen_y = (1200,1200)

    
    
    # Loop while the player is still active
    while playing:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                
        # Set the speed of the hero, which is the speed the screen corner moves.
        speed = 10

        colliding = world.get_at(hero_rect.center)
        #print(colliding)
        #print(barriers)
        for colors in barriers:
            #print(colors)
            if colliding != barriers[colors]:
            # Allow continuous motion on a held-down key
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    is_facing_right = False
                    pass_check = True
                    for colors in barriers:
                        hero_x, hero_y = hero_rect.center
                        if world.get_at((hero_x + speed, hero_y)) == barriers[colors]:
                            print("pass_check False")
                            pass_check = False
                    if pass_check == True:
                        screen_x += speed
                if keys[pygame.K_RIGHT]:
                    is_facing_right = True
                    screen_x += -speed
                if keys[pygame.K_UP]:
                    screen_y += speed
                if keys[pygame.K_DOWN]:
                    screen_y += -speed
        #This keeps pikachu in the middle
        world_rect[0] = screen_x/2 - 900
        world_rect[1] = screen_y/2 - 500
               
        # The hero stays in the center of the screen
        hero_sprite = hero[frame_count%len(hero)]
        if is_facing_right:
            hero_sprite = pygame.transform.flip(hero_sprite, True, False)
        
        fps = clock.get_fps()
        # Render text to the screen
        label = myfont.render("FPS:" + str(int(fps)), True, (255,255,0))
        screen.blit(label, (20,20))
            
        render_phrases(say_phrases, frame_count, screen, myfont)


        
        # The ghost moves across the map by adding 1 to the x coordinate. Since POSITION is a tuple, we
        # cannot modify just the x coordinate, we need to rebuild the tuple.
        
        #Safe
        character_data["safe"][POSITION] = (character_data["safe"][POSITION][0] + 1, character_data["safe"][POSITION][1])
        character_data["safe"][RECT].center = (character_data["safe"][POSITION][0] - screen_x, character_data["safe"][POSITION][1] - screen_y)
        if character_data["safe"][VISIBLE]:
            screen.blit(character_data["safe"][IMAGE], character_data["safe"][RECT])

        # interact with ghost
        if character_data["safe"][VISIBLE] and hero_rect.colliderect(character_data["safe"][RECT]):
            character_data["safe"][VISIBLE] = False;
            say_phrases.append((character_data["safe"][PHRASE], frame_count + 150))
            game_state["Safe is open!"] = True # Not really used in the starter code

        # Bring drawn changes to the front
        pygame.display.update()


        frame_count += 1
            
        screen.fill((0,0,0))
        #Map 1
        screen.blit(world, world_rect)
        #print("last",world, world_rect)
        screen.blit(hero[frame_number%len(hero)], hero_rect)
            

        # 60 fps
        clock.tick(60)

    # loop is over    
    pygame.quit()
    sys.exit()




# Start the program
main()
