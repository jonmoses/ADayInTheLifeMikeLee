import pygame
import sys
import random


def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check if the non-transparent pixels of one mask contacts the non-transparent pixels of another.
    """
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))

    return overlap != None


def level3():
    pygame.init()
    frame_count = 0
    clock = pygame.time.Clock()
    message_font = pygame.font.SysFont('monospace', 24)
    time_font = pygame.font.SysFont('monospace', 50)
    start_time = pygame.time.get_ticks()

    # making the background for this level
    capitol = pygame.image.load("/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/Capitol.png")
    map_size = capitol.get_size()
    map_rect = capitol.get_rect()
    screen = pygame.display.set_mode(map_size)
    capitol = capitol.convert_alpha()
    capitol.set_colorkey((255, 255, 255))

    # making mike
    mike_lee_running1 = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/MikeLeeRunning1.png").convert_alpha()
    mike_lee_running1 = pygame.transform.smoothscale(mike_lee_running1, (200, 240))
    mike_lee_running1_rect = mike_lee_running1.get_rect()
    mike_lee_running1_rect.center = (200, 380)
    mike_lee_running3_mask = pygame.mask.from_surface(mike_lee_running1)

    mike_lee_running2 = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/MikeLeeRunning2.png").convert_alpha()
    mike_lee_running2 = pygame.transform.smoothscale(mike_lee_running2, (225, 215))
    mike_lee_running2_rect = mike_lee_running2.get_rect()
    mike_lee_running2_rect.center = (190, 380)
    mike_lee_running3_mask = pygame.mask.from_surface(mike_lee_running2)

    mike_lee_running3 = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/MikeLeeRunning3.png").convert_alpha()
    mike_lee_running3 = pygame.transform.smoothscale(mike_lee_running3, (200, 240))
    mike_lee_running3_rect = mike_lee_running3.get_rect()
    mike_lee_running3_rect.center = (200, 380)
    mike_lee_running3_mask = pygame.mask.from_surface(mike_lee_running3)

    mike_lee_jump = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/MikeLeeJump.png").convert_alpha()
    mike_lee_jump = pygame.transform.smoothscale(mike_lee_jump, (200, 240))
    mike_lee_jump_rect = mike_lee_jump.get_rect()
    mike_lee_jump_rect.center = (200, 380)

    # Making the objects to be avoided - load images once
    responsibilities_img = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/Responsibilities.png").convert_alpha()
    responsibilities_img = pygame.transform.smoothscale(responsibilities_img, (200, 100))
    responsibilities_mask = pygame.mask.from_surface(responsibilities_img)

    criticalthinking_img = pygame.image.load(
        "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/CriticalThinking.png").convert_alpha()
    criticalthinking_img = pygame.transform.smoothscale(criticalthinking_img, (200, 100))
    criticalthinking_mask = pygame.mask.from_surface(criticalthinking_img)

    # Lists to store multiple objects streaming across screen
    obstacles = []

    # Obstacle spawning settings
    spawn_timer = 0
    spawn_interval = 60
    # speed is in pixels a second
    obstacle_speed = 14
    min_height = 100
    max_height = 500

    # This dictionary holds all of the different images for the running animation. we switch between them later. the first index
    # is the image and the second object is the rect. image number 5 is the jumping animation and holds an extra variable
    # that is used as the direction of travel variable to calculate the motion path
    mike_lee_running_dict = {1: [mike_lee_running1, mike_lee_running1_rect],
                             2: [mike_lee_running2, mike_lee_running2_rect],
                             3: [mike_lee_running3, mike_lee_running3_rect],
                             4: [mike_lee_running2, mike_lee_running2_rect], 5: [mike_lee_jump, mike_lee_jump_rect, 0]}
    # These handle how and when to exit the game
    is_alive = True
    level_completed = False
    # This variable handles which image is displayed so mike is not running in mid air
    mike_jumping = False
    # This sets out first image of mike

    current_mike = 1
    while is_alive:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # space bar to close the level
                    level_completed = True
                    is_alive = False
                # This checks if the up key is pressed to start jumping, it also checks if the character is already jumping
                # and doesnt let it restart the jump if so
                if event.key == pygame.K_w and mike_lee_running_dict[5][1].centery > 390:
                    mike_jumping = True
                    mike_lee_running_dict[5][1].centery = 390
                    mike_lee_running_dict[5][2] = 1

        if mike_lee_running_dict[current_mike][1].centery > 380:
            mike_lee_running_dict[current_mike][1].centery = 380
            mike_jumping = False
            current_mike = 1
        else:
            # This controls the jump physics. the index [2] holds the direction of travel variable. we subtract .04 off
            # of that each loop. That direction of travel variable is multiplied by a larger value (35 right now) to
            # decide the height of the jump. The values -35 and .04  make it possible to avoid all the obstacles
            mike_lee_running_dict[5][1].centery = mike_lee_running_dict[5][1].centery + mike_lee_running_dict[5][2] * (
                -35)
            mike_lee_running_dict[5][2] -= .04

        if frame_count % 15 == 0 and not mike_jumping:
            if current_mike == 4:
                current_mike = 1
            else:
                current_mike += 1

        if mike_jumping:
            current_mike = 5

        # This section is obstacle spawning happens. The spawn timer controls the flow. Can adjust the spawn frequency
        # at the top to change the frequency of spawning
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            # this is where the type of obstacle that is spawned is chosen
            obstacle_type = random.choice(['responsibilities', 'criticalthinking'])
            # choose the height randomly
            spawn_y = random.randint(min_height, max_height)
            # make the obstacle spawn a little off screen so we cant see it
            spawn_x = map_size[0] + 100

            # This section is where we define the new obstacles that are spawning
            # Used Google Gemini to brainstorm this solution of storing obstacles as a dictionary in our obstacles list. This
            # approach avoids a lot of the issues i was having with some other methods i was trying where I was trying to
            # use the same object in two different locations
            if obstacle_type == 'responsibilities':
                obstacle_rect = responsibilities_img.get_rect()
                obstacle_rect.center = (spawn_x, spawn_y)
                obstacles.append({
                    'type': 'responsibilities',
                    'image': responsibilities_img,
                    'rect': obstacle_rect,
                    'mask': responsibilities_mask
                })
            # second obstacle type
            else:
                obstacle_rect = criticalthinking_img.get_rect()
                obstacle_rect.center = (spawn_x, spawn_y)
                obstacles.append({
                    'type': 'criticalthinking',
                    'image': criticalthinking_img,
                    'rect': obstacle_rect,
                    'mask': criticalthinking_mask
                })

        # This changes the position of all the objects in the obstacles list
        for obstacle in obstacles:
            obstacle['rect'].x -= obstacle_speed

            # delete the obstacles that are off screen
            if obstacle['rect'].right < 0:
                obstacles.remove(obstacle)

        # Get current mike's mask
        current_mike_mask = pygame.mask.from_surface(mike_lee_running_dict[current_mike][0])
        current_mike_rect = mike_lee_running_dict[current_mike][1]

        # Check collision with each obstacle. im just using the collision detection function from the example
        # level. It works pretty well
        for obstacle in obstacles:
            if pixel_collision(current_mike_mask, current_mike_rect, obstacle['mask'], obstacle['rect']):
                print("Collision detected! Game Over!")
                is_alive = False
                level_completed = False

        screen.fill((150, 150, 150))
        screen.blit(capitol, map_rect)

        # Draw all obstacles in the obstacles list
        for obstacle in obstacles:
            screen.blit(obstacle['image'], obstacle['rect'])

        # Draw Mike Lee
        screen.blit(mike_lee_running_dict[current_mike][0], mike_lee_running_dict[current_mike][1])

        # Add some instructions
        instructions = [
            "Try to avoid critical thinking and",
            "your responsibilities!"
            "\n ",
            "survive for 20 seconds to pass"
        ]
        if (pygame.time.get_ticks() - start_time) // 1000 > 20:
            return True
        line_counter = 0
        for text in instructions:
            if text:
                label = message_font.render(text, True, (0, 0, 0))
                screen.blit(label, (20, 20 + line_counter * 25))
                line_counter += 1
        screen.blit(time_font.render(str((pygame.time.get_ticks() - start_time) // 1000), True, (0, 0, 0)),
                    (screen.get_width() / 2, 50))
        pygame.display.update()
        clock.tick(60)
        frame_count += 1

    return False
