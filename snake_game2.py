
from tkinter import *
import random
import time
import os
import neat


class gen_counter:
    snake_counter = 0


class gamefield:

    fields = []

    def __init__(self,field_amount_row, field_amount_column, field_x, field_y, border_size):
        self.field_amount_row = field_amount_row
        self.field_amount_column = field_amount_column
        self.bordersize = border_size
        self.field_x = field_x
        self.field_y = field_y
        self.x = field_amount_row * field_x + (field_amount_row * self.bordersize + self.bordersize)
        self.y = field_amount_column * field_y + (field_amount_column * self.bordersize + self.bordersize)
        self.root = Tk()
        self.root.geometry(str(self.x) + 'x' + str(self.y))
        self.canvas = Canvas(self.root, width=self.x, height=self.y)
        self.canvas.pack()
        self.draw_fields()

    def draw_fields(self):
        cur_y = 0
        cur_x = 0
        for c in range(1, self.field_amount_column + 1):
            self.canvas.create_rectangle(cur_x, cur_y, self.x, cur_y + self.bordersize, fill="grey")
            cur_y = cur_y + self.bordersize
            for counter in range(1, self.field_amount_row + 1):
                # create Border
                self.canvas.create_rectangle(cur_x, cur_y, cur_x + self.bordersize, cur_y + self.field_y, fill="grey")
                cur_x = cur_x + self.bordersize
                # create actual field
                self.fields.append([self.canvas.create_rectangle(cur_x, cur_y, cur_x + self.field_x, cur_y + self.field_y, fill="black"),[cur_x, cur_y, cur_x + self.field_x, cur_y + self.field_y]])
                cur_x = cur_x + self.field_x
            # create Border @ the end
            self.canvas.create_rectangle(cur_x, cur_y, cur_x + self.bordersize, cur_y + self.field_y, fill="grey")
            cur_y = cur_y + self.field_y
            cur_x = 0
        self.canvas.create_rectangle(cur_x, cur_y, self.x, cur_y + self.bordersize, fill="grey")
        print(self.fields)



class snake:

    def __init__(self, index, field, snake_x, snake_y, gamefield, food_class):
        self.index = index
        self.field_id = field[0]
        self.field_pos = field[1]
        self.snake_x = snake_x
        self.snake_y = snake_y
        self.gamefield = gamefield
        self.canvas = gamefield.canvas
        self.food_class = food_class
        self.snake_length = 0
        self.snake = []
        self.snake_body_pos = []
        self.alive = True
        self.eaten = False
        self.direction = 'r'
        self.first_dead = True
        self.steps = 70
        self.snake_head = []
        self.previous_snake_body_positions = []
        self.create_snake()

    def create_snake(self):
        self.snake.append(self.canvas.create_rectangle(((self.field_pos[2] - self.field_pos[0]) / 2) + self.field_pos[0],
                                                       ((self.field_pos[3] - self.field_pos[1]) / 2) + self.field_pos[1],
                                                       ((self.field_pos[2] - self.field_pos[0]) / 2) + self.snake_x + self.field_pos[0],
                                                       ((self.field_pos[3] - self.field_pos[1]) / 2) + self.snake_y + self.field_pos[1],
                                                       fill="white"))
        self.snake.append(self.canvas.create_rectangle(((self.field_pos[2] - self.field_pos[0]) / 2)-self.snake_x + self.field_pos[0],
                                                       ((self.field_pos[3] - self.field_pos[1]) / 2) + self.field_pos[1],
                                                       ((self.field_pos[2] - self.field_pos[0]) / 2) + self.field_pos[0],
                                                       ((self.field_pos[3] - self.field_pos[1]) / 2) + self.snake_y + self.field_pos[1],
                                                       fill="white"))
        self.snake.append(self.canvas.create_rectangle(((self.field_pos[2] - self.field_pos[0]) / 2) - (self.snake_x * 2) + self.field_pos[0],
                                                       ((self.field_pos[3] - self.field_pos[1]) / 2) + self.field_pos[1],
                                                       ((self.field_pos[2] - self.field_pos[0]) / 2) - self.snake_x + self.field_pos[0],
                                                       ((self.field_pos[3] - self.field_pos[1]) / 2) + self.snake_y + self.field_pos[1],
                                                       fill="white"))
        self.snake_head = self.canvas.coords(self.snake[0])
        self.snake_length = 3
        for i in self.snake:
            self.snake_body_pos.append(self.canvas.coords(i))

    def check_snake_movement(self):
        for c, food in enumerate(snake_food.food,0):
            if(self.snake_head == self.canvas.coords(food)):
                self.eaten = True
                self.food_class.respawn_food(food)


        if self.snake_head in self.previous_snake_body_positions:
            self.alive = False

        if self.snake_head[2] > self.field_pos[2] or self.snake_head[3] > self.field_pos[3] or self.snake_head[1] < self.field_pos[1] or self.snake_head[0] < self.field_pos[0]:
            self.alive = False




    def snake_move(self, direction = 'r'):
        if(self.alive):
            self.steps = self.steps - 1
            if(direction == 'r' and self.direction != 'l'):
                self.direction = direction
            elif(direction == 'l' and self.direction != 'r'):
                self.direction = direction
            elif(direction == 'u' and self.direction != 'd'):
                self.direction = direction
            elif(direction == 'd' and self.direction != 'u'):
                self.direction = direction

            self.previous_snake_body_positions = []
            for i in self.snake:
                self.previous_snake_body_positions.append(self.canvas.coords(i))

            for c, snake_part in enumerate(self.snake, 0):
                if(c == 0):
                    if self.direction == 'u':
                        self.canvas.move(snake_part,0,-self.snake_y)
                    elif self.direction == 'd':
                        self.canvas.move(snake_part,0,self.snake_y)
                    elif self.direction == 'l':
                        self.canvas.move(snake_part,-self.snake_x,0)
                    else:
                        self.canvas.move(snake_part,self.snake_x,0)
                    self.snake_head = self.canvas.coords(snake_part)
                else:

                    pos_previous_item = self.previous_snake_body_positions[c - 1]
                    x_to_move = pos_previous_item[0] - self.canvas.coords(snake_part)[0]
                    y_to_move = pos_previous_item[1] - self.canvas.coords(snake_part)[1]
                    self.canvas.move(snake_part, x_to_move, y_to_move)


                if (self.eaten):
                    self.eaten = False
                    self.snake_length = self.snake_length +1
                    self.steps += 150
                    self.snake.append(self.canvas.create_rectangle(self.previous_snake_body_positions[len(self.previous_snake_body_positions)-1][0], self.previous_snake_body_positions[len(self.previous_snake_body_positions)-1][1],
                                                                   self.previous_snake_body_positions[len(self.previous_snake_body_positions)-1][2], self.previous_snake_body_positions[len(self.previous_snake_body_positions)-1][3],
                                                                   fill="white"))
                self.snake_body_pos = []
                for i in self.snake:
                    self.snake_body_pos.append(self.canvas.coords(i))
                if(self.steps < 0):
                    self.alive = False

    def snake_dead(self):
        for i in self.snake:
            self.canvas.delete(i)

        self.food_class.delete_food(self.food_class.food_id)
        """
        self.snake_length = 0
        self.snake = []
        self.snake_body_pos = []
        self.alive = True
        self.eaten = False
        self.direction = 'r'
        self.first_dead = True
        self.snake_head = []
        self.previous_snake_body_positions = []
        """


class snake_food:

    food = []

    def __init__(self, color = 'green', gamefield = None, food_x_size = 5, food_y_size = 5, field = None):
        self.color = color
        self.field_id = field[0]
        self.field_pos = field[1]
        self.food_pos = []
        self.food_id = -1
        self.gamefield = gamefield
        self.canvas = gamefield.canvas
        self.food_x_size = food_x_size
        self.food_y_size = food_y_size
        self.spawn_food()


    def spawn_food(self):
        x_random = random.randrange(self.field_pos[0], self.field_pos[2], self.food_y_size)
        y_random = random.randrange(self.field_pos[1], self.field_pos[3], self.food_y_size)
        new_food = self.canvas.create_rectangle(x_random,y_random,x_random+self.food_x_size,y_random+self.food_y_size,fill='green')
        self.food_id = new_food
        self.food.append(new_food)
        self.food_pos = self.canvas.coords(new_food)

    def respawn_food(self, food_eaten = -1):
        if not(food_eaten == -1):
            self.canvas.delete(food_eaten)
            self.food.remove(food_eaten)
        self.spawn_food()

    def delete_food(self, food_eaten_del = -1):
        if not(food_eaten_del == -1):
            self.canvas.delete(food_eaten_del)
            self.food.remove(food_eaten_del)







def eval_genomes(genomes, config):

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    snake_counter_est.snake_counter += 1
    nets = []
    snakes = []
    snake_food_arr = []
    ge = []
    counter = 0
    dead_counter = 0
    running = True
    for genome_id, genome in genomes:
        if (counter <= len(game.fields) - 1):
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            the_snakes_food = snake_food('green',game,5,5,game.fields[counter])
            snakes.append(snake(counter, game.fields[counter],5,5,game,the_snakes_food))
            snake_food_arr.append(the_snakes_food)
            ge.append(genome)
            counter = counter + 1
        else:
            genome.fitness = 0
            print(counter)

    while dead_counter < 80:
        if not running:
            break
        running = False
        for c, snake_sel in enumerate(snakes,0):


            if (snake_sel.alive):
                running = True
                snake_sel_head_pos = snake_sel.snake_head
                snake_sel_field_pos = snake_sel.field_pos
                snake_sel_body_positions = snake_sel.snake_body_pos
                snake_sel_food_pos = snake_sel.food_class.food_pos

                distance_wall_right = snake_sel_field_pos[2] - snake_sel_head_pos[2]
                distance_wall_up = snake_sel_head_pos[1] - snake_sel_field_pos[1]
                distance_wall_down = snake_sel_field_pos[3] - snake_sel_head_pos[3]
                distance_wall_left = snake_sel_head_pos[0] - snake_sel_field_pos[0]

                distance_body_right = distance_wall_right
                distance_body_up = distance_wall_up
                distance_body_down = distance_wall_down
                distance_body_left = distance_wall_left

                for co, i in enumerate(snake_sel_body_positions):
                    if (co != 0):
                        if (snake_sel_head_pos[1] == i[1] and i[0] > snake_sel_head_pos[0] and distance_body_right > (
                                i[0] - snake_sel_head_pos[0])):  # right
                            distance_body_right = i[0] - snake_sel_head_pos[0]

                        if (snake_sel_head_pos[1] == i[1] and i[0] < snake_sel_head_pos[0] and distance_body_left > (
                                snake_sel_head_pos[0] - i[0])):  # left
                            distance_body_left = snake_sel_head_pos[0] - i[0]

                        if (snake_sel_head_pos[0] == i[0] and i[1] < snake_sel_head_pos[1] and distance_body_up > (
                                snake_sel_head_pos[1] - i[1])):  # up
                            distance_body_up = snake_sel_head_pos[1] - i[1]

                        if (snake_sel_head_pos[0] == i[0] and i[1] > snake_sel_head_pos[1] and distance_body_down > (
                                i[1] - snake_sel_head_pos[1])):  # down
                            distance_body_down = i[1] - snake_sel_head_pos[1]

                distance_food_right = distance_wall_right
                distance_food_up = distance_wall_up
                distance_food_down = distance_wall_down
                distance_food_left = distance_wall_left

                food_right = 0
                food_up = 0
                food_down = 0
                food_left = 0

                if (snake_sel_head_pos[0] == snake_sel_food_pos[0]):  # up/down
                    if (snake_sel_head_pos[1] > snake_sel_food_pos[1]):  # up
                        distance_food_up = snake_sel_head_pos[1] - snake_sel_food_pos[1]
                        food_up = 1
                    else:  # down
                        distance_food_down = snake_sel_food_pos[1] - snake_sel_head_pos[1]
                        food_down = 1

                if (snake_sel_head_pos[1] == snake_sel_food_pos[1]):  # left/right
                    if (snake_sel_head_pos[0] > snake_sel_food_pos[0]):  # left
                        distance_food_left = snake_sel_head_pos[0] - snake_sel_food_pos[0]
                        food_left = 1
                    else:  # right
                        distance_food_right = snake_sel_food_pos[0] - snake_sel_head_pos[0]
                        food_right = 1

                output = nets[c].activate((distance_wall_right, distance_wall_left, distance_wall_down, distance_wall_up, distance_body_right, distance_body_left, distance_body_down, distance_body_up, distance_food_right, distance_food_left, distance_food_down, distance_food_up,food_right,food_left,food_down,food_up))


                if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                    snake_sel.snake_move('r')
                elif output[1] > 0.5:
                    snake_sel.snake_move('l')
                elif output[2] > 0.5:
                    snake_sel.snake_move('u')
                elif output[3] > 0.5:
                    snake_sel.snake_move('d')
                else:
                    snake_sel.snake_move('r')

                snake_sel.check_snake_movement()
                #print('moving Snake {}'.format(c))
                if(snake_sel.eaten):
                    ge[c].fitness = ge[c].fitness + 5
                    #print('eaten')
                #ge[c].fitness = ge[c].fitness + 0.1
                #print('gen = {}, dead_counter = {}, alive = {}'.format(snake_counter_est.snake_counter,dead_counter,c))
            else:
                #snakes.pop(c)
                #snake_food_arr.pop(c)
                #nets.pop(c)
                #ge.pop(c)
                if(snake_sel.first_dead):
                    dead_counter = dead_counter + 1
                    snake_sel.first_dead = False
                    snake_sel.snake_dead()
                    #print("gen = {}, dead_counter: {}, dead = {}".format(snake_counter_est.snake_counter,dead_counter, c))
        game.root.update()
        #time.sleep(0.001)

    #print('end')


def run(config_file):


    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.

    winner = p.run(eval_genomes, None)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))












game = gamefield(10,8,100,100,5)
snake_counter_est = gen_counter()

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)


