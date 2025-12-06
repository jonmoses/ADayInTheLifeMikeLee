import pygame

is_playing = True


def display_loss_screen():
    pygame.init()

    # Define the screen
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    score_font = pygame.font.SysFont('monospace', 50)
    # Create a clock to help compute a consistent frame rate
    clock = pygame.time.Clock()

    # Main part of the game
    is_playing = True
    while is_playing:  # while is_playing is true, repeat
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
        screen.fill((0, 0, 0))  # fill the window with a colo
        # Bring all the changes to the screen into view
        clock.tick(60)
        label = score_font.render("YOU LOSE", True, (255, 255, 255))
        screen.blit(label, (width / 2 - 150, height / 2 - 30))
        pygame.display.update()

    # Once the game loop is done, close the window and quit.
    pygame.quit()


def display_win_screen():
    pygame.init()

    # Define the screen
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    score_font = pygame.font.SysFont('monospace', 50)
    # Create a clock to help compute a consistent frame rate
    clock = pygame.time.Clock()

    # Main part of the game
    is_playing = True
    while is_playing:  # while is_playing is true, repeat
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
        screen.fill((0, 0, 0))  # fill the window with a colo
        # Bring all the changes to the screen into view
        clock.tick(60)
        label = score_font.render("YOU WIN!", True, (255, 255, 255))
        screen.blit(label, (width / 2 - 150, height / 2 - 30))
        pygame.display.update()
