import pygame
import sys
import colors


def check_win(mas: list, sign: str):
    """ Checking win combination """
    win_text = f'"{sign.title()}" won!'
    zeroes = 0
    for row in mas:
        zeroes += row.count(0)
        if row.count(sign) == 3:
            return win_text
    for col in range(3):
        if mas[0][col] == mas[1][col] == mas[2][col] == sign:
            return win_text
    if mas[0][0] == mas[1][1] == mas[2][2] == sign or \
            mas[0][2] == mas[1][1] == mas[2][0] == sign:
        return win_text
    if zeroes == 0:
        return 'Remis!'
    return False


def tic_tac_toe():
    """ Tic Tac Toe game, 3x3, for restart press Space """
    pygame.init()
    size_block = 100
    margin = 15
    width = height = size_block * 3 + margin * 4
    size_window = (width, height)
    screen = pygame.display.set_mode(size_window)
    pygame.display.set_caption('tic-tac-toe')

    mas = [[0] * 3 for i in range(3)]
    query = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                column = x_mouse // (margin + size_block)
                row = y_mouse // (margin + size_block)
                if mas[row][column] == 0:
                    if query % 2 == 0:
                        mas[row][column] = 'x'
                    else:
                        mas[row][column] = 'o'
                    query += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_over = False
                mas = [[0] * 3 for i in range(3)]
                query = 0
                screen.fill(colors.BLACK)

        if not game_over:
            for row in range(3):
                for col in range(3):
                    if mas[row][col] == 'x':
                        color = colors.WILD_ORCHID
                    elif mas[row][col] == 'o':
                        color = colors.LIVER
                    else:
                        color = colors.GHOST_WHITE

                    x = size_block * col + margin * (col + 1)
                    y = size_block * row + margin * (row + 1)
                    pygame.draw.rect(screen, color, (x, y, size_block, size_block))
                    if color == colors.WILD_ORCHID:
                        pygame.draw.line(screen, colors.LIVER, (x + 10, y + 10),
                                         (x + size_block - 10, y + size_block - 10), 15)
                        pygame.draw.line(screen, colors.LIVER, (x + size_block - 10, y + 10),
                                         (x + 10, y + size_block - 10), 15)
                    elif color == colors.LIVER:
                        pygame.draw.circle(screen, colors.WILD_ORCHID, (x + size_block // 2, y + size_block // 2),
                                           size_block // 2 - 10, 10)

        if (query - 1) % 2 == 0:
            game_over = check_win(mas, 'x')
        else:
            game_over = check_win(mas, 'o')

        if game_over:
            screen.fill(colors.BLACK)
            font = pygame.font.SysFont('arial', 80)
            game_over_text = font.render(game_over, True, colors.GHOST_WHITE)
            text_size = game_over_text.get_rect()
            text_coord_x = screen.get_width() / 2 - text_size.width / 2
            text_coord_y = screen.get_height() / 2 - text_size.height / 2
            screen.blit(game_over_text, [text_coord_x, text_coord_y])

        pygame.display.update()


if __name__ == '__main__':
    tic_tac_toe()
