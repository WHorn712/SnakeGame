import pygame
from logica_negocio import snake_game

pygame.init()



#Main game loop with pygame.
while True:
    display = snake_game.Display(pygame)
    snake = snake_game.Snake(pygame)
    food = snake_game.Food(pygame)
    score_game = snake_game.Score(pygame)
    while True:
        move_new_dir = 0
        ok = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move_new_dir = 1
                if event.key == pygame.K_LEFT:
                    move_new_dir = 2
                if event.key == pygame.K_UP:
                    move_new_dir = 3
                if event.key == pygame.K_DOWN:
                    move_new_dir = 4
                if event.key == pygame.K_q:
                    ok = True
        if ok:
            break
        snake.move_snake(move_new_dir, False)
        snake.update_position()
        done = snake_game.get_is_gameover(snake, display)
        if snake.x == food.x and snake.y == food.y:
            lista = snake_game.position_food(display.display_width, display.display_height, food.block, snake)
            food.x = lista[0]
            food.y = lista[1]
            snake.increase_size()
            score_game.sum_score()

        snake.add_block_in_snake()
        score = score_game.score
        display.update_screen()
        food.draw_food(pygame, display)
        snake.draw_snake(display, pygame)
        score_game.draw_score(display)

        if done:
            snake.x = display.display_width / 2
            snake.y = display.display_height / 2
            snake.length = 1
            snake.snake_list = []
            lista = snake_game.position_food(display.display_width, display.display_height, food.block, snake)
            food.x = lista[0]
            food.y = lista[1]
            score_game.score = 0
        display.update_screen()
        food.draw_food(pygame, display)
        snake.draw_snake(display, pygame)
        score_game.draw_score(display)
        pygame.display.update()
        display.clock.tick(snake.speed)
    pygame.quit()
    quit()

