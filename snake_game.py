""" Snake Game """

import pygame
import pygame_menu
import colors
import sys
from random import randint


SIZE_BLOCK = 20
COUNT_BLOCKS = 20
GAP = 1
BORDER = 20
HEADER_MARGIN = 70
width = SIZE_BLOCK * COUNT_BLOCKS + GAP * (COUNT_BLOCKS + 1) + BORDER * 2
height = width + HEADER_MARGIN
size_window = (width, height)


class SnakeBlock:
    """ The body of snake """

    def __init__(self, x: int, y: int):
        """ Block coordinates """
        self.x = x
        self.y = y

    def is_inside(self):
        """ Checks if the point is on the playing field """
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        """ Let compare the snake head and the apple """
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color: tuple, row: int, col: int):
    """ Draws blocks of playing field, snake and apples """
    x = SIZE_BLOCK * col + GAP * (col + 1) + BORDER
    y = SIZE_BLOCK * row + GAP * (row + 1) + BORDER + HEADER_MARGIN
    pygame.draw.rect(screen, color, (x, y, SIZE_BLOCK, SIZE_BLOCK))


def start_the_game():
    """ Starts the game """

    def get_random_empty_block() -> SnakeBlock:
        """ Get random place where the apple appears """
        x = randint(0, COUNT_BLOCKS - 1)
        y = randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = randint(0, COUNT_BLOCKS - 1)
            empty_block.y = randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row, buf_col = -1, 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row, buf_col = 1, 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row, buf_col = 0, -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row, buf_col = 0, 1

        """ Header of game """
        screen.fill(colors.QUICK_SILVER)
        pygame.draw.rect(screen, colors.DARK_LIVER_1, (0, 0, size_window[0], HEADER_MARGIN))
        text_total = courier_font.render(f'Total: {total}', 1, colors.BONE)
        text_speed = courier_font.render(f'Speed: {speed}', 1, colors.BONE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (text_total.get_rect().width + SIZE_BLOCK * 3, SIZE_BLOCK))

        """ Playing field """
        for row in range(COUNT_BLOCKS):
            for col in range(COUNT_BLOCKS):
                if (row + col) % 2 == 0:
                    color = colors.BONE
                else:
                    color = colors.ISABELLINE
                draw_block(color, row, col)

        draw_block(colors.WILD_ORCHID, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(colors.RAISIN_BLACK, block.x, block.y)
        pygame.display.flip()
        head = snake_blocks[-1]
        if not head.is_inside(): break

        if apple == head:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)
        if new_head in snake_blocks: break
        snake_blocks.append(new_head)
        snake_blocks.pop(0)
        timer.tick(2 + speed)


if __name__ == '__main__':
    pygame.init()
    bg_image = pygame.image.load('snake.jpg')
    screen = pygame.display.set_mode(size_window)
    pygame.display.set_caption('Snake')
    timer = pygame.time.Clock()
    courier_font = pygame.font.SysFont('courier', 36)

    main_theme = pygame_menu.themes.THEME_DARK.copy()
    main_theme.set_background_color_opacity(0.6)
    menu = pygame_menu.Menu('Snake game', 400, 220,
                            theme=main_theme)
    menu.add.text_input('Name: ', default='Gamer1')
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:
        screen.blit(bg_image, (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()
