import pygame
import random


# Starter code for an adventure game. Written by David Johnson for CS 1400 University of Utah.

# Finished game authors:
#
#

def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check if the non-transparent pixels of one mask contacts the non-transparent pixels of another.
    """
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap != None


def create_constituent(image_name):
    constituent = pygame.image.load(
        f"/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/{image_name}.png").convert_alpha()
    constituent = pygame.transform.smoothscale(constituent, (200, 110))
    constituent_rect = constituent.get_rect()
    constituent_rect.center = (random.randint(400, 800), random.randint(100, 600))
    constituent_mask = pygame.mask.from_surface(constituent)
    # Referenced this stack overflow post to learn about the random.choice method https://stackoverflow.com/questions/46820182/randomly-generate-1-or-1-positive-or-negative-integer
    # This returns the image, rect, and mask for the new constituent. It also returns two integers, either 1 or
    # negative 1 that will be used later to define the random movement of the NPC around the map
    return [constituent, constituent_rect, constituent_mask, random.choice((-1, 1)), random.choice((-1, 1))]


def level1():

    # setup
    pygame.init()
    frame_count = 0
    clock = pygame.time.Clock()
    message_font = pygame.font.SysFont('monospace', 24)

    # Load the map up
    utah = pygame.image.load("/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/UtahMap.png")
    map_size = utah.get_size()
    map_rect = utah.get_rect()
    screen = pygame.display.set_mode(map_size)
    utah = utah.convert_alpha()
    utah.set_colorkey((255, 255, 255))
    map_mask = pygame.mask.from_surface(utah)

    # Create the player
    player = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/MikeLee.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (70, 70))
    player_rect = player.get_rect()
    player_rect.center = (650, 250)
    player_mask = pygame.mask.from_surface(player)

    # Creating Landmarks
    # Zion National Park
    zion = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/Zion.png").convert_alpha()
    zion = pygame.transform.smoothscale(zion, (150, 100))
    zion_rect = zion.get_rect()
    zion_rect.center = (550, 550)
    zion_mask = pygame.mask.from_surface(zion)

    # Uinta
    uinta = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/Uinta.png").convert_alpha()
    uinta = pygame.transform.smoothscale(uinta, (100, 100))
    uinta_rect = uinta.get_rect()
    uinta_rect.center = (850, 220)
    uinta_mask = pygame.mask.from_surface(uinta)

    # Wasatch
    wasatch = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/Wasatch.png").convert_alpha()
    wasatch = pygame.transform.smoothscale(wasatch, (100, 100))
    wasatch_rect = wasatch.get_rect()
    wasatch_rect.center = (650, 250)
    wasatch_mask = pygame.mask.from_surface(wasatch)

    # Create the donors
    donors = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/BlackstoneGroup.png").convert_alpha()
    donors = pygame.transform.smoothscale(donors, (400, 100))
    donors_rect = donors.get_rect()
    donors_rect.center = (1100, 150)
    donors_mask = pygame.mask.from_surface(donors)

    # Making all the states. Each of the parks has a state and the donor money collected has a state
    sold_zion = False
    sold_uinta = False
    sold_wasatch = False
    is_alive = True

    # Make the NPC's
    # Storing the npcs in a list to make it easier to update the random movement
    constituents = []
    for index in range(1, 10):
        if index % 2 == 1:
            constituents.append(create_constituent('UtahGirl'))
        else:
            constituents.append(create_constituent('UtahGuy'))

    # Hiding the mouse
    pygame.mouse.set_visible(False)

    # GAME LOOP
    while is_alive:
        # EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False

        # Game loop updates
        # Update player position to mouse location
        pos = pygame.mouse.get_pos()
        player_rect.center = pos

        # This update controls the random movement of the NPC's
        for utahn in constituents:
            if utahn[1].left < 300:
                utahn[3] = 1
            elif utahn[1].left > 800:
                utahn[3] = -1
            if utahn[1].top < 50:
                utahn[4] = 1
            elif utahn[1].top > 580:
                utahn[4] = -1
            utahn[1].left += utahn[3]
            utahn[1].top += utahn[4]

        # Checking for the win condition.
        if sold_zion and sold_uinta and sold_wasatch and pixel_collision(player_mask, player_rect, donors_mask,
                                                                         donors_rect):
            # Returning true if the player collides with the donor mask
            return True

        # Park collisions
        if not sold_zion and pixel_collision(player_mask, player_rect, zion_mask, zion_rect):
            sold_zion = True

        if not sold_uinta and pixel_collision(player_mask, player_rect, uinta_mask, uinta_rect):
            sold_uinta = True

        if not sold_wasatch and pixel_collision(player_mask, player_rect, wasatch_mask, wasatch_rect):
            sold_wasatch = True

        # Check constituent collisions (game over if touched)
        for utahn in constituents:
            if pixel_collision(player_mask, player_rect, utahn[2], utahn[1]):
                is_alive = False

        # Updating the park image to the sold sign after the player touches it
        if sold_zion:
            zion = pygame.image.load(
                "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/ForSale.png").convert_alpha()
            zion = pygame.transform.smoothscale(zion, (100, 100))
            zion_rect = zion.get_rect()
            zion_rect.center = (550, 550)
            zion_mask = pygame.mask.from_surface(zion)

        if sold_uinta:
            uinta = pygame.image.load(
                "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/ForSale.png").convert_alpha()
            uinta = pygame.transform.smoothscale(uinta, (100, 100))
            uinta_rect = uinta.get_rect()
            uinta_rect.center = (850, 230)
            uinta_mask = pygame.mask.from_surface(uinta)

        if sold_wasatch:
            wasatch = pygame.image.load(
                "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/ForSale.png").convert_alpha()
            wasatch = pygame.transform.smoothscale(wasatch, (100, 100))
            wasatch_rect = wasatch.get_rect()
            wasatch_rect.center = (650, 250)
            wasatch_mask = pygame.mask.from_surface(wasatch)

        # DRAWING
        # Draw background
        screen.fill((150, 150, 150))
        screen.blit(utah, map_rect)

        # Draw game objects
        screen.blit(donors, donors_rect)
        screen.blit(zion, zion_rect)
        screen.blit(uinta, uinta_rect)
        screen.blit(wasatch, wasatch_rect)

        # Draw constituents
        for utahn in constituents:
            screen.blit(utahn[0], utahn[1])

        # Draw player
        screen.blit(player, player_rect)

        # This draws the text to explain the level to the player
        # I used Google Gemini to brainstorm the best way to display the text here.
        # All the instruction are stored in a list, where each entry is a length where it doesn't overlap the map
        # then the for loop goes over each line and prints it to the screen with the line counter
        # being used to correctly space each new label
        instructions = [
            "Help Senator Mike Lee sell ",
            "our public lands!",
            "\n",
            "you'll be able to collect",
            "donations from your",
            "out of state donors",
            "and move on to ",
            "the next level when you ",
            "sell all of the parks",
            "on the map",
            "\n",
            "Make sure to avoid your",
            "constituents!"
        ]
        line_counter = 0
        for text in instructions:
            if text:  # Don't render empty strings
                label = message_font.render(text, True, (0, 0, 0))
                screen.blit(label, (20, 20 + line_counter * 20))
                line_counter += 1

        # Frame counter
        frame_count += 1
        pygame.display.update()
        clock.tick(30)

    # Return false, meaning the level was failed
    return False
