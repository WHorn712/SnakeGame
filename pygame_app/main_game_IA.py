import pygame
from logica_negocio import agent, snake_game

pygame.init()

#Main game loop with pygame.
while True:
    record = 0
    agent = agent.Agent()
    display = snake_game.Display(pygame)
    snake = snake_game.Snake(pygame)
    food = snake_game.Food(pygame)
    score_game = snake_game.Score(pygame)
    frame_iteraction = 0
    while True:
        last_distance = snake_game.distance_snake_food(snake, food)
        frame_iteraction += 1
        # get old state
        state_old = agent.get_state(display, snake, food)

        # get move
        final_move = agent.get_action(state_old, record)

        snake.move_snake(final_move, True)
        snake.update_position()
        done = snake_game.get_is_gameover(snake, display)
        reward = 0
        if snake_game.check_colision(snake, food):
            lista = snake_game.position_food(display.display_width, display.display_height, food.block, snake=snake)
            food.x = lista[0]
            food.y = lista[1]
            snake.increase_size()
            score_game.sum_score()
            reward = 10
        else:
            reward = snake_game.get_reward(last_distance, snake, food, done, frame_iteraction, display.display_width, display.display_height)
        snake.add_block_in_snake()
        score = score_game.score
        display.update_screen()
        food.draw_food(pygame, display)
        snake.draw_snake(display, pygame)
        score_game.draw_score(display)

        # perform move and get new state
        state_new = agent.get_state(display, snake, food)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            frame_iteraction = 0
            snake.x = display.display_width / 2
            snake.y = display.display_height / 2
            snake.length = 1
            snake.snake_list = []
            lista = snake_game.position_food(display.display_width, display.display_height, food.block, snake=snake)
            food.x = lista[0]
            food.y = lista[1]
            score_game.score = 0
            agent.n_game += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_game, 'Score', score, 'Record', record)
        ok = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    ok = True
        if ok:
            break
        display.update_screen()
        food.draw_food(pygame, display)
        snake.draw_snake(display, pygame)
        score_game.draw_score(display)
        pygame.display.update()
        display.clock.tick(snake.speed)
    pygame.quit()
    quit()