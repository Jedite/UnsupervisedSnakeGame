from NeuralNetwork import *
from Snake import *
from Food import *
from pygame.locals import *

import math
import sys

# Menu is not mandatory
# from Menu import *


class Game:
    def __init__(self):
        pygame.init()

        self.S = Snake()
        self.F = Food()
        # self.M = Menu()

        self.CLOCK = pygame.time.Clock()

        self.reset()

    def reset(self):
        """
        Resets game after one iteration of "run_game" loop
        """
        self.SCREEN = pygame.display.set_mode(WINDOW_SIZE)

        self.S.x = (random.randint(0, 1000) // 40) * 40
        self.S.y = (random.randint(0, 600) // 40) * 40
        self.S.direction = [0] * 4
        self.S.snake_list = [(self.S.x, self.S.y)]

        self.F.x = (random.randint(0, 1000) // 40) * 40
        self.F.y = (random.randint(0, 600) // 40) * 40

        self.food_count = 0
        self.score_requirement = 50
        self.steps = 0
        self.done = False
        self.num_simulations = 5000
        self.game_steps = 300

        self.grid = np.zeros((SCREENTILES[0] + 2, SCREENTILES[1] + 2))

    def get_observation(self, x_increment, y_increment):
        """
        Get observation of snake x and y coordinates

        :param x_increment: adds to x coordinate from snake head
        :param y_increment: adds to y coordinate from snake head
        :return: [1, 0] if body; [0, 1] if food, [0, 0] if nothing
        """
        grid_x = (self.S.x + x_increment) // 40 + 1
        grid_y = (self.S.y + y_increment) // 40 + 1

        max_distance = math.sqrt((SCREENTILES[0] ** 2) + (SCREENTILES[1] ** 2))
        base_distance = math.sqrt((x_increment // 40) ** 2 + (y_increment // 40) ** 2)
        max_x = 28
        max_y = 18

        food = max_distance
        wall = max_distance
        body = max_distance

        distance = 0

        while max_x > grid_x > -1 and max_y > grid_y > -1:
            if self.grid[grid_y, grid_x] == 3:
                body = distance
            elif self.grid[grid_y, grid_x] == 2:
                food = distance
            elif self.grid[grid_y, grid_x] == 4:
                wall = distance
            distance += base_distance
            grid_y += y_increment // 40
            grid_x += x_increment // 40

        return [wall, food, body]

    def reset_grid(self):
        """
        Resets the grid per step
        Resets snake and body movement & food location
        """
        self.grid = np.zeros((SCREENTILES[0] + 2, SCREENTILES[1] + 2))

        self.grid[0, 0:] = 4  # all of first row
        self.grid[17, 0:] = 4  # all of last row
        self.grid[0:, 0] = 4  # all of first column
        self.grid[0:, 27] = 4  # all of last column

        for body in self.S.snake_list[1:]:  # body
            row = body[1] // 40
            column = body[0] // 40
            self.grid[row, column] = 3

        self.grid[self.S.snake_list[0][1] // 40 + 1, self.S.snake_list[0][0] // 40 + 1] = 1  # head
        self.grid[self.F.y // 40 + 1, self.F.x // 40 + 1] = 2  # food

    def observation_update(self):
        """
        Updates previous & current observation
        -1 is snake body; 1 is snake head; 2 is food.

        :return: current_observation
        """
        self.reset_grid()

        current_observation = []

        left = self.get_observation(-40, 0)
        top_left = self.get_observation(-40, -40)
        top_right = self.get_observation(40, -40)
        top = self.get_observation(0, -40)
        bottom_left = self.get_observation(-40, 40)
        bottom_right = self.get_observation(40, 40)
        bottom = self.get_observation(0, 40)
        right = self.get_observation(40, 0)

        current_observation.extend([top_left, top, top_right, left, right, bottom_left, bottom, bottom_right])

        current_observation = np.array([current_observation])
        current_observation.shape = (24,)
        scale = math.sqrt((SCREENTILES[0] ** 2) + (SCREENTILES[1] ** 2))
        current_observation = 1 - 2 * current_observation / scale

        return current_observation

    def show_text(self, msg, x, y, text_color):
        """
        Displays text on pygame window

        :param msg: message needed to display
        :param x: x location of where display occurs
        :param y: y location of where display occurs
        :param text_color: color of message
        """
        font_obj = pygame.font.SysFont("freesans", 32)
        msg_obj = font_obj.render(msg, False, text_color)

        self.SCREEN.blit(msg_obj, (x, y))

    def snake_collision(self):
        """
        Performs all snake collisions with external objects

        :return: True if snake head hits snake body
        """
        # snake and head collision
        # if (self.S.x, self.S.y) in self.S.snake_list[1:]:
        #     return True
        # wraps around walls
        if self.S.x > 1000 or self.S.x < 0 or self.S.y > 600 or self.S.y < 0:
            self.reward = -100
            return True
        # snake and food collision
        if self.S.x == self.F.x and self.S.y == self.F.y:
            self.F.x = (random.randint(0, 1000) // 40) * 40
            self.F.y = (random.randint(0, 600) // 40) * 40

            self.S.snake_list.insert(0, (self.S.x, self.S.y))

            self.food_count += 1
            self.reward = 100
            self.steps = 0

    def handle_events(self):
        """
        Handles game events
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def render(self):
        self.CLOCK.tick(5)

        pygame.display.update()
        self.SCREEN.fill(WHITE)

        self.show_text(f"Steps: {self.steps}", 0, 0, RED)

        self.F.draw(self.SCREEN)
        self.S.draw(self.SCREEN)

    def step(self, action):
        """
        Runs one step of the game loop
        """
        self.reward = 1

        # self.render()

        self.handle_events()

        self.S.check_event(action)

        self.S.snake_list.pop()
        self.S.snake_list.insert(0, (self.S.x, self.S.y))

        if self.snake_collision():
            self.done = True

        self.steps += 1

        return self.observation_update(), self.reward, self.done, self.food_count

    def generate_population(self, model):
        training_data = []

        for games in range(self.num_simulations):
            self.reset()
            game_memory = []
            previous_observation = []
            score = 0

            for _ in range(self.game_steps):
                # self.render()
                if len(previous_observation) == 0:
                    action = random.randint(0, 3)
                else:
                    if not model:
                        action = random.randrange(0, 3)
                    else:
                        prediction = model.predict(previous_observation.reshape(-1, len(previous_observation), 1))
                        action = np.argmax(prediction[0])

                observation, reward, done, info = self.step(action)

                if len(previous_observation) > 0:
                    game_memory.append([previous_observation, action])
                previous_observation = observation

                score += reward

                if done:
                    break

            if score >= self.score_requirement:
                for data in game_memory:
                    action_sample = [0, 0, 0]
                    action_sample[data[1]] = 1
                    training_data.append([data[0], action_sample])

        return training_data

    def eval(self, model):
        scores = []
        choices = []
        for games in range(10):
            score = 0
            game_memory = []
            prev_obs = []
            self.reset()
            for _ in range(self.game_steps):
                self.render()

                if len(prev_obs) == 0:
                    action = random.randrange(0, 3)
                else:
                    prediction = model.predict(prev_obs.reshape(-1, len(prev_obs), 1))
                    action = np.argmax(prediction[0])

                choices.append(action)

                new_observation, reward, done, info = self.step(action)
                prev_obs = new_observation
                game_memory.append([new_observation, action])
                score += reward

                if done:
                    break

                scores.append(score)

        print('Average Score is')
        print('Average Score:', sum(scores) / len(scores))
        print('choice 1:{}  choice 0:{}'.format(choices.count(1) / len(choices), choices.count(0) / len(choices)))