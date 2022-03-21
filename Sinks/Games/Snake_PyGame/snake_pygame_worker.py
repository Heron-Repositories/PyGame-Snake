
# This is the code of the worker part of the Sink Operation. Here the user needs to write most of the code in order to
# define the Operation's functionality.

# <editor-fold desc="The following 6 lines of code are required to allow Heron to be able to see the Operation without
# package installation. Do not change.">
import sys
from os import path

current_dir = path.dirname(path.abspath(__file__))
while path.split(current_dir)[-1] != r'Heron':
    current_dir = path.dirname(current_dir)
sys.path.insert(0, path.dirname(current_dir))
# </editor-fold>

# <editor-fold desc="Extra imports if required">
import pygame
import random
import threading

from Heron.communication.socket_for_serialization import Socket
from Heron import general_utils as gu
# </editor-fold>

# <editor-fold desc="Global variables if required. Global variables operate obviously within the scope of the process
# that is running when this script is called so they pose no existential threats and are very useful in keeping state
# over different calls of the work function (see below).">
need_parameters = True
speed: float
direction: str
previous_direction: str
game_over: bool

# </editor-fold>


# The initialise function is called when the worker process is fired up from the com process and it gets called
# as long as it is returning False. It gets passed the worker_object which carries the parameters from the GUI so it is
# used to initialise the parameters values in the worker process (and of course for any other initialisation required,
# eg. initialising a driver or starting a thread). Here is also where the initialisation of the Visualisation object
# needs to happen because it needs the Node's name and index that are carried in the worker object
def initialise(_worker_object):
    global need_parameters
    global speed
    global direction
    global previous_direction

    # put the initialisation of the Node's parameter's in a try loop to take care of the time it takes for the GUI to
    # update the SinkWorker object.
    try:
        parameters = _worker_object.parameters
        speed = parameters[0]
    except:
        return False

    direction = 'UP'
    previous_direction = 'UP'

    pg_thread = threading.Thread(group=None, target=pygame_thread)
    pg_thread.start()

    return True


def pygame_thread():
    global speed
    global direction
    global previous_direction
    global game_over

    pygame.init()

    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    dis_width = 600
    dis_height = 400

    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Snake Game by Edureka')

    clock = pygame.time.Clock()

    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)

    def Your_score(score):
        value = score_font.render("Your Score: " + str(score), True, yellow)
        dis.blit(value, [0, 0])

    def our_snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])

    def gameLoop():
        global direction
        global previous_direction
        global speed

        game_over = False
        game_close = False

        snake_block = 10
        snake_speed = speed

        x1 = dis_width / 2
        y1 = dis_height / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        while not game_over:

            while game_close == True:
                dis.fill(blue)
                message("You Lost! Press C-Play Again or Q-Quit", red)
                Your_score(Length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                '''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0
                '''

            if direction == 'UP' and not previous_direction == 'UP':
                y1_change = -snake_block
                x1_change = 0
            if direction == 'DOWN' and not previous_direction == 'DOWN':
                y1_change = snake_block
                x1_change = 0
            if direction == 'LEFT' and not previous_direction == 'LEFT':
                x1_change = -snake_block
                y1_change = 0
            if direction == 'RIGHT' and not previous_direction == 'RIGHT':
                x1_change = snake_block
                y1_change = 0
            previous_direction = direction

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            our_snake(snake_block, snake_List)
            Your_score(Length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1

            clock.tick(snake_speed)

        pygame.quit()
        #quit()

    gameLoop()


def work_function(data, parameters):
    global speed
    global direction

    # If any parameters need to be updated during runtime then do that here, e.g.
    # Also update the visualisation parameter. This allows to turn on and off the visualisation window during
    # run time
    try:
        speed = parameters[0]
    except:
        pass
    # In the case of multiple inputs the topic will tell you which input the message has come from. The topic is a
    # string that is formatted as follows:
    # previous_node_name##previous_node_index##previous_node_output_name -> this_none_name##this_node_index##this_node_input_name
    # so you can see which input the data is coming from by looking at the ##this_node_input_name part. Also although
    # the names of the inputs and outputs can have spaces, these become underscores in the names of the topics.
    topic = data[0]

    # The message is a numpy array send in two parts, a header dic (as bytes0 with the array's info and list of bytes
    # that carry the array's payload.
    message = data[1:]
    message = Socket.reconstruct_array_from_bytes_message(message)[0]  # This is needed to reconstruct the message
    # that comes in into the numpy array that it is.

    try:
        angle = int(message)

        if angle < 90 and angle > 45:
            direction = 'UP'
        if angle < 45 and angle > 0:
            direction = 'LEFT'
        if angle < 0 and angle > -45:
            direction = 'DOWN'
        if angle < -45 and angle > -90:
            direction = 'RIGHT'

        print(angle, direction)
    except:
        pass

    # This function does not return anything.


# The on_end_of_life function must exist even if it is just a pass
def on_end_of_life():
    global game_over

    game_over = True


# This needs to exist. The worker_function and the end_of_life function must be defined and passed. The initialisation_
# function is optional.
if __name__ == "__main__":
    worker_object = gu.start_the_sink_worker_process(work_function=work_function,
                                                     end_of_life_function=on_end_of_life,
                                                     initialisation_function=initialise)
    worker_object.start_ioloop()