import pygame
from levels import level1, level2, level3
import display_win_or_loss


def main():
    """
    runs all levels in order.
    """
    pygame.init()
    # level 1
    print("Starting Level 1...")
    passed_level1 = level1.level1()

    if not passed_level1:
        print("Level 1 failed!")
        display_win_or_loss.display_loss_screen()
        return

    print("Level 1 completed!")

    # level 2

    print("Starting Level 2")
    passed_level2 = level2.level2()

    if not passed_level2:
        print("Level 2 failed!")
        display_win_or_loss.display_loss_screen()
        return

    print("Level 2 completed!")

    # level 3

    print("starting Level 3")
    passed_level3 = level3.level3()

    if not passed_level3:
        print("Level 3 failed!")
        display_win_or_loss.display_loss_screen()
        return

    print("Level 3 completed!")

    display_win_or_loss.display_win_screen()


if __name__ == "__main__":
    main()
