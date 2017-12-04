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

barriers = {"wall": (158,158,158), "door": (77,58,52),"desk": (167,147,127),"desk1": (150,132,114),"computer": (158,139,139),
            "blanket": (33,54,69),"bed": (59,76,171),"bed1": (63,81,181),"bed2": (72,89,184),"bed3": (96,125,139),"bedFrame": (63,81,181),
            "counter": (122,117,113),"can": (230,219,209),"Stove": (74,72,71),"Stove1": (160,48,48),
            "fridge" :(209,208,207),"sink":(225,225,225),"table_chair_drawer":(186,160,139),"stool": (153,110,75), "Coffee Table":(199,184,171),
            "Couch": (121,146,184),"Couch1": (144,169,186),"Blanket": (194,75,75),"blanket1": (199,116,120),
            "cabnit": (147,148,129),"car": (174,174,174),"car1": (111,111,111),"Car3": (156,156,156),}


##def draw_characters(character_dict, screen, screen_x,screen_y,frame_count):
##    for characters in character_dict:
##        if characters["hero"]
##        character = screen_x/2 - 900
##        character = screen_y/2 - 500       
##        screen.blit(hero[frame_number%len(hero)], hero_rect.center)
##        if characters["safe"]
##            if character_data["safe"][VISIBLE]:
##            screen.blit(character_data["safe"][IMAGE], character_data["safe"][RECT])
##        
##    return

def speed_from_terrain(hero_rect, world_map,screen_x,screen_y,tile_size):
    return
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
    screen_x,screen_y = (world_size)
    
    # Define where the hero is positioned on the big map
    screen_x, screen_y = (1800,900)
    center_x, center_y = (screen_x-1035,screen_y-630)
    
    # The map rect is basically the whole screen, and we will draw to it to fill the background with the image
    world_rect = world.get_rect()
    #print(world_rect)


    print(world_rect)
    
    # create the window the same size as the map image
    screen = pygame.display.set_mode([1500,1500])
 #   screen = pygame.display.set_mode(world_size)

    map_tile_width = 30
    map_tile_height = 20
    tile_size = 32
#    screen_size = width, height = (map_tile_width*tile_size, map_tile_height*tile_size)
    screen_size = width, height = (500, 500)
    #print(screen_size)
    
    # Get a font
    myfont = pygame.font.SysFont("monospace", 24)
    
    # create the hero character
    # We treat the hero differently than all the other sprite characters as it doesn't move
    hero = load_piskell_sprite("Items/Hero",12)
    hero_rect = hero[0].get_rect()
    #print(hero_rect)
    
    # Place the hero at the center of the screen
    hero_rect.center = (width/2, height/2)
    #print(hero_rect.center)
    mini_map = pygame.image.load("Rooms/minimap.png").convert_alpha()
    
    # Put all the characters in a dictionary so we can pass to functions easily
    character_data = {}


    # Add All Characters

    #Safe
    safe_image = pygame.image.load("Items/Safe.png").convert_alpha()
    safe_rect = safe_image.get_rect()
    safe_pos = (-387,0)
    safe = {IMAGE:safe_image, RECT:safe_rect, POSITION:safe_pos, VISIBLE:True, PHRASE:"You got the front door"} 
    character_data["safe"] = safe
    #key
    key_image = pygame.image.load("Items/Key.png").convert_alpha()
    character_data["key"] = {IMAGE:key_image, RECT:key_image.get_rect(), POSITION:(500,500), VISIBLE:True, PHRASE:"You got the key to the kitchen and living room!"}
    #key 2
    key2_image = pygame.image.load("Items/Key.png").convert_alpha()
    character_data["key2"] = {IMAGE:key2_image, RECT:key2_image.get_rect(), POSITION:(300,300), VISIBLE:True, PHRASE:"You got the key to the garage!"}
    #key 3
    key3_image = pygame.image.load("Items/Key.png").convert_alpha()
    character_data["key3"] = {IMAGE:key3_image, RECT:key3_image.get_rect(), POSITION:(300, 900), VISIBLE:False, PHRASE:"You got the key to the front door!"}



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
    
    
    # capture ghost variable
    game_state = {}
    
    # Need to set all state variables here so that they are in the dictionary
    game_state["Got a key"] = False
    game_state["Got a garage key"] = False
    game_state["Safe is open!"] = False
    game_state["Got the front door key!"] = False

    # Define where the hero is positioned on the big map
    screen_x, screen_y = (1800,900)
    center_x, center_y = (screen_x-1035,screen_y-630)

    frame_number = 0

    
    # Loop while the player is still active
    while playing:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                
        # Set the speed of the hero, which is the speed the screen corner moves.
        speed = 5

        #Suppose to get the color pixel the hero is on top of
        colliding = world.get_at((center_x, center_y))

        moved = False

        keys = pygame.key.get_pressed()
        # Allow continuous motion on a held-down key
        if keys[pygame.K_LEFT]:
            moved = True                    
            is_facing_right = False
            pass_check = True
            frame_number +=1
            for colors in barriers:
                if world.get_at((center_x-speed-1, center_y)) == barriers[colors]:
                    print("pass_check False")
                    pass_check = False
            if pass_check == True:
                screen_x += speed
                center_x -= speed
                print(screen_x)
        if keys[pygame.K_RIGHT]:
            moved = True                    
            is_facing_right = True
            pass_check = True
            frame_number +=1
            for colors in barriers:
                if world.get_at((center_x+speed+1, center_y)) == barriers[colors]:
                    print("pass_check False")
                    pass_check = False
            if pass_check == True:        
                screen_x -= speed
                center_x += speed
        if keys[pygame.K_UP]:
            moved = True
            pass_check = True
            frame_number +=1
            for colors in barriers:
                if world.get_at((center_x, center_y-speed-1)) == barriers[colors]:
                    print("pass_check False")
                    pass_check = False                    
            if pass_check == True:
                screen_y += speed
                center_y -= speed
        if keys[pygame.K_DOWN]:
            moved = True
            pass_check = True
            frame_number +=1
            for colors in barriers:
                if world.get_at((center_x, center_y+speed+1)) == barriers[colors]:
                    print("pass_check False")
                    pass_check = False
            if pass_check == True:
               screen_y -= speed
               center_y += speed
                        
        #if moved == True:                
#            print("Colliding Color: ",colliding)
            #print("Hero Color: ",world.get_at(hero_rect.center))
            #print("screen x: ",screen_x)
            #print("screen y: ",screen_y)
            #print("world size: ",world.get_size())
            #print("World Color: ",world.get_at((center_x, center_y)))
            #print("Hero Position: ", center_x, ", ", center_y)
            #print("World Position: ", world_rect.center)
        
        
        
        world_rect[0] = screen_x - 2317
        world_rect[1] = screen_y - 900

        # scale down from position on the big map to pixel on the minimap
        #minimap_offset_x, minimap_offset_y =  map_position_to_minimap_index( (screen_x, screen_y), tile_size)
                    
        #Map 1
        #pygame.draw.circle(world, [255,0,0], [screen_x-1800, screen_y-900],5)
        screen.blit(world, world_rect)
        
        #Key 1:Bed Room
        character_data["key"][POSITION] = (character_data["key"][POSITION][0], character_data["key"][POSITION][1])


        
        character_data["key"][RECT].center = (character_data["key"][POSITION][0]-screen_x+1700, character_data["key"][POSITION][1]-screen_y+700)
        print("Second: ",screen_x)
        print(character_data["key"][RECT].center)
        print(screen.blit(character_data["key"][IMAGE], character_data["key"][RECT]))
        if character_data["key"][VISIBLE]:
            screen.blit(character_data["key"][IMAGE], character_data["key"][RECT])
##        if character_data["key"][VISIBLE] and hero_rect.colliderect(character_data["key"][RECT]):
##            character_data["key"][VISIBLE] = False;
##            say_phrases.append((character_data["key"][PHRASE], frame_count + 150))
##            game_state["Got a key"] = True # Not really used in the starter code

        #Key2: Living Room
        character_data["key2"][RECT].center = (character_data["key2"][POSITION][0]-screen_x+1500, character_data["key2"][POSITION][1] - screen_y+700)
        if character_data["key2"][VISIBLE]:
            screen.blit(character_data["key2"][IMAGE], character_data["key2"][RECT])
        if character_data["key2"][VISIBLE] and hero_rect.colliderect(character_data["key2"][RECT]):
            character_data["key2"][VISIBLE] = False;
            say_phrases.append((character_data["key2"][PHRASE], frame_count + 150))
            game_state["Got a garage key"] = True # Not really used in the starter code


        #Safe
        
        character_data["safe"][RECT].center = (character_data["safe"][POSITION][0] - screen_x, character_data["safe"][POSITION][1] - screen_y)
        if character_data["safe"][VISIBLE]:
            screen.blit(character_data["safe"][IMAGE], character_data["safe"][RECT])

        # interact with safe
        if character_data["safe"][VISIBLE] and hero_rect.colliderect(character_data["safe"][RECT]):
            character_data["safe"][VISIBLE] = False;
            character_data["key3"][VISIBLE] = True;
            say_phrases.append((character_data["safe"][PHRASE], frame_count + 150))
            game_state["Safe is open!"] = True # Not really used in the starter code

        #Key 3: To the Front Door
        character_data["key3"][RECT].center = (character_data["key3"][POSITION][0] - screen_x, character_data["key3"][POSITION][1] - screen_y)
        if character_data["key3"][VISIBLE]:
            screen.blit(character_data["key2"][IMAGE], character_data["key3"][RECT])
        if character_data["key3"][VISIBLE] and hero_rect.colliderect(character_data["key3"][RECT]):
            character_data["key3"][VISIBLE] = False;
            say_phrases.append((character_data["key3"][PHRASE], frame_count + 150))
            game_state["Got the front door key!"] = True # Not really used in the starter code




        # The hero stays in the center of the screen
        hero_sprite = hero[frame_count%len(hero)]
        if is_facing_right:
            hero_sprite = pygame.transform.flip(hero_sprite, True, False)
        screen.blit(hero_sprite, hero_rect)
        
        
        screen.blit(mini_map,(300,1))

        
        fps = clock.get_fps()
        # Render text to the screen
        label = myfont.render("FPS:" + str(int(fps)), True, (255,255,0))
        screen.blit(label, (20,20))
            
        render_phrases(say_phrases, frame_count, screen, myfont)


        # Bring drawn changes to the front
        pygame.display.update()


        frame_count += 1
            
        screen.fill((0,0,0))


        #Where all the characters besides the hero(I think) are suppose to be drawn
        #draw_characters(character_data,screen,screen_x,screen_y,frame_count)           

        # 60 fps
        clock.tick(60)

    # loop is over    
    pygame.quit()
    sys.exit()




# Start the program
main()
