# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0,0]
paddle1_pos = (HEIGHT/2)-HALF_PAD_HEIGHT
paddle2_pos = (HEIGHT/2)-HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
color = "Green"

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global RIGHT
    
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = -random.randrange(1, 2)
    else:
        ball_vel[0] = -random.randrange(2, 4)
        ball_vel[1] = -random.randrange(1, 2)
    


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global LEFT, score1, score2, ball_vel, HEIGHT, HALF_PAD_HEIGHT, color
    score1 = 0
    score2 = 0
    paddle1_pos = (HEIGHT/2)-HALF_PAD_HEIGHT
    paddle2_pos = (HEIGHT/2)-HALF_PAD_HEIGHT
    color = random.choice(["Red" , "White" , "Green" , "Blue" , "Yellow"])
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, color
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    
    ball_pos[0] += ball_vel[0]        
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            ball_vel[0] += (ball_vel[0] * 0.1)
            ball_vel[0] = - ball_vel[0]
        else:
            spawn_ball(RIGHT)
            score2 += 1
    elif ball_pos[0] >= (WIDTH-1) - BALL_RADIUS - PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            ball_vel[0] += (ball_vel[0] * 0.1)
            ball_vel[0] = - ball_vel[0]
        else:
            spawn_ball(LEFT)
            score1 += 1
    elif ball_pos[1] <= BALL_RADIUS + PAD_WIDTH:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT-1) - BALL_RADIUS - PAD_WIDTH:
        ball_vel[1] = - ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 3, color, color)
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel + PAD_HEIGHT <= HEIGHT and paddle1_pos + paddle1_vel >= 0:
        paddle1_pos += paddle1_vel
    
    if paddle2_pos + paddle2_vel + PAD_HEIGHT <= HEIGHT and paddle2_pos + paddle2_vel >= 0:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line([ HALF_PAD_WIDTH,paddle1_pos] , [HALF_PAD_WIDTH ,paddle1_pos+PAD_HEIGHT] ,PAD_WIDTH, color )
    canvas.draw_line([ WIDTH-HALF_PAD_WIDTH,paddle2_pos] , [WIDTH-HALF_PAD_WIDTH ,paddle2_pos+PAD_HEIGHT] ,PAD_WIDTH, color )
    
    # determine whether paddle and ball collide  
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, HEIGHT/5], 60, 'Red')
    canvas.draw_text(str(score2), [3*WIDTH/4, HEIGHT/5], 60, 'Red')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP['s']:  
        paddle1_vel = 3
    elif key == simplegui.KEY_MAP['up']:  
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP['down']:  
        paddle2_vel = 3
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:  
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:  
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:  
        paddle2_vel = 0

def restart():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart" , restart, 100)


# start frame
new_game()
frame.start()

