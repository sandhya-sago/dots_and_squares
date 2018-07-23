
import pygame
from dots_and_squares_game import dots_and_squares_game

def main():
    pygame.init()
    ds_game = dots_and_squares_game()
    while ds_game.status():
        for event in pygame.event.get():
            pygame.display.update()
            try:
                if event.type == pygame.QUIT:
                    ds_game.quit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    ds_game.click(pos)
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    ds_game.mouse(pos)
            except Exception as exp:
                raise(exp)
    return None

if __name__ == "__main__":
    main()
    print ("Good Game!!!")