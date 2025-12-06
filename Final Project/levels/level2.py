import pygame
import sys
import random

pygame.init()
frame_count = 0
clock = pygame.time.Clock()

message_font = pygame.font.SysFont('monospace', 24)
score_font = pygame.font.SysFont('monospace', 50)

# set up the screen
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
key_size = (200, 200)
key_position = (250, 330)
# State Variables

# Define the arrow keys
up_key = pygame.image.load(
    "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/UpArrow.png").convert_alpha()
up_key = pygame.transform.smoothscale(up_key, key_size)
up_key_rect = up_key.get_rect()
up_key_rect.center = key_position
up_key_mask = pygame.mask.from_surface(up_key)

down_key = pygame.image.load(
    "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/DownArrow.png").convert_alpha()
down_key = pygame.transform.smoothscale(down_key, key_size)
down_key_rect = down_key.get_rect()
down_key_rect.center = key_position
down_key_mask = pygame.mask.from_surface(down_key)

left_key = pygame.image.load(
    "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/LeftArrow.png").convert_alpha()
left_key = pygame.transform.smoothscale(left_key, key_size)
left_key_rect = left_key.get_rect()
left_key_rect.center = key_position
left_key_mask = pygame.mask.from_surface(left_key)

right_key = pygame.image.load(
    "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/RightArrow.png").convert_alpha()
right_key = pygame.transform.smoothscale(right_key, key_size)
right_key_rect = right_key.get_rect()
right_key_rect.center = key_position
right_key_mask = pygame.mask.from_surface(right_key)

# Making Mike Lee
mike_lee = pygame.image.load(
    "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/MikeLee.png").convert_alpha()
mike_lee = pygame.transform.smoothscale(mike_lee, (450, 430))
mike_lee_rect = mike_lee.get_rect()
mike_lee_rect.center = (770, 380)

mike_lee_left = pygame.image.load(
    "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/MikeLeeLeft.png").convert_alpha()
mike_lee_left = pygame.transform.smoothscale(mike_lee_left, (450, 430))
mike_lee_left_rect = mike_lee_left.get_rect()
mike_lee_left_rect.center = (770, 380)

mike_lee_right = pygame.image.load(
    "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/MikeLeeRight.png").convert_alpha()
mike_lee_right = pygame.transform.smoothscale(mike_lee_right, (450, 430))
mike_lee_right_rect = mike_lee_right.get_rect()
mike_lee_right_rect.center = (770, 380)

# Make the phone screen
phone_screen = pygame.image.load(
    "/Users/jonmoses/PycharmProjects/CS1400/Final Project/image_assets/PhoneScreen.png").convert_alpha()
phone_screen = pygame.transform.smoothscale(phone_screen, (900, 550))
phone_screen_rect = phone_screen.get_rect()
phone_screen_rect.center = (250, 300)

# storing image groups in dictionaries to make it easy to change which one we display. Two entries in the mike lee dictionary
# are the same image of him looking straight to make that one more likely
mike_is_a_dict = {1: [mike_lee, mike_lee_rect], 2: [mike_lee_left, mike_lee_left_rect],
                  3: [mike_lee_right, mike_lee_right_rect], 4: [mike_lee, mike_lee_rect]}
arrows_dict = {1: [up_key, up_key_rect], 2: [down_key, down_key_rect], 3: [left_key, left_key_rect],
               4: [right_key, right_key_rect]}


def level2():
    frame_count = 0
    is_playing = True
    has_started_minigame = True
    passed_level = False
    target_arrow = 1
    display_mike = 1
    score = 0
    start_time = pygame.time.get_ticks()
    elapsed_time = 0
    while is_playing:
        current_arrow = None

        # EVENT LOOP - handle all events in one place
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
            if event.type == pygame.MOUSEBUTTONUP:
                has_started_minigame = True
            # Check for key press events only when minigame is active
            if has_started_minigame and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    current_arrow = 1
                elif event.key == pygame.K_s:
                    current_arrow = 2
                elif event.key == pygame.K_a:
                    current_arrow = 3
                elif event.key == pygame.K_d:
                    current_arrow = 4

        # Check if correct key was pressed and update score
        if has_started_minigame and current_arrow == target_arrow:
            score += 1
            target_arrow = random.randint(1, 4)

        if frame_count % 100 == 0:
            display_mike = random.randint(1, 4)

        # Define when to turn off is playing
        if score > 30:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            if elapsed_time <= 30:
                passed_level = True
            is_playing = False
        # Define the win condition

        # Draw objects
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (155, 255, 255), (200, 150, 100, 50))
        screen.blit(phone_screen, phone_screen_rect)
        screen.blit(score_font.render("Score", True, (255, 100, 100)), (420, 400))
        screen.blit(score_font.render("Time", True, (255, 100, 100)), (425, 250))
        # I used this stack overflow post to better understand the way pygame prints text onto the screen https://stackoverflow.com/questions/19117062/how-to-add-text-into-a-pygame-rectangle
        screen.blit(score_font.render(str(score), True, (255, 100, 100)), (470, 450))
        screen.blit(score_font.render(str((pygame.time.get_ticks() - start_time) // 1000), True, (255, 100, 100)),
                    (470, 300))
        screen.blit(arrows_dict[target_arrow][0], arrows_dict[target_arrow][1])
        screen.blit(mike_is_a_dict[display_mike][0], mike_is_a_dict[display_mike][1])
        instructions = [
            "Press the arrow key on the phone screen ",
            "to help mike lee scroll on Twitter!",
            "\n",
            "\n",
            "Scroll 30 times",
            "under 20 in",
            "seconds to ",
            "progress!"
        ]

        line_counter = 0
        for text in instructions:
            if text:  # Don't render empty strings
                label = message_font.render(text, True, (255, 255, 255))
                screen.blit(label, (width / 2 - 100, 20 + line_counter * 20))
                line_counter += 1

        pygame.display.update()
        clock.tick(60)
        frame_count += 1

    if not passed_level:
        return False
    return True
