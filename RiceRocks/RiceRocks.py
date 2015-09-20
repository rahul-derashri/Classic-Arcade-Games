# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            center = [0,0]
            center[0] = self.image_center[0] + self.image_size[0]
            center[1] = self.image_center[1]
            canvas.draw_image(self.image ,center ,self.image_size, self.pos, self.image_size, self.angle )
        else:
            canvas.draw_image(self.image ,self.image_center ,self.image_size, self.pos, self.image_size, self.angle )

    def update(self):
        self.angle += self.angle_vel
        
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * 0.1
            self.vel[1] += forward[1] * 0.1
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.pos = [self.pos[0] % WIDTH , self.pos[1] % HEIGHT]
        
    
    def update_anguler_vel(self , direction):
        if direction == "LEFT":
            self.angle_vel = -0.1
        elif direction == "RIGHT":
            self.angle_vel = 0.1
        else:
            self.angle_vel = 0
     
    def update_thrust(self , flag):
        self.thrust = flag
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
    
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
           
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            index = (self.age % self.lifespan)/1
            new_center = [self.image_center[0] + index * self.image_size[0],self.image_center[1]]
            canvas.draw_image(self.image ,new_center ,self.image_size, self.pos, self.image_size, self.angle )
        else:
            canvas.draw_image(self.image ,self.image_center ,self.image_size, self.pos, self.image_size, self.angle )
            
        
    
    def update(self):
        
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos = [self.pos[0] % WIDTH , self.pos[1] % HEIGHT]
        
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
        
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self , other_object):
        other_pos = other_object.get_position()
        distance = math.sqrt(math.pow(self.pos[0]-other_pos[0],2)+math.pow(self.pos[1]-other_pos[1],2))
        if distance < self.radius + other_object.get_radius():
            #explosion_sound.rewind()
            #explosion_sound.play()
            return True
        else:
            return False

def group_group_collide( group1 , group2):
    count = 0
    for item in set(group1):
        if group_collide(group2 , item):
            count += 1
            group1.discard(item)
    
    return count
        

def group_collide(group , other_object):
    global explosion_group
    for item in set(group):
        if item.collide(other_object):
            explosion = Sprite(item.get_position(), [0,0], 0, 0, explosion_image, explosion_info , explosion_sound)
            explosion_group.add(explosion)
            group.remove(item)
            return True
    
    return False
            
        
def click(pos):
    global started, lives, score,soundtrack
    center = [WIDTH/2, HEIGHT/2]
    size = splash_info.get_size()
    if pos[0] > (center[0] - size[0]/2) and pos[0] < (center[0] + size[0]/2) and pos[1] > (center[1] - size[1]/2) and pos[1] < (center[1] + size[1]/2):
        started = True
        lives = 3
        score = 0
        soundtrack.play()
    
def draw(canvas):
    global time, started, rock_group, lives, score, missile_group,explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if group_collide( rock_group , my_ship ):
        lives -= 1
        
    if lives <= 0:
        started = False
        rock_group = set()
        explosion_group = set()
        soundtrack.pause()
        soundtrack.rewind()
    
    score += group_group_collide(rock_group ,missile_group)
    
    process_sprite_group(canvas, explosion_group)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas ,missile_group )
    
    # draw ship and sprites
    my_ship.draw(canvas)
    #a_rock.draw(canvas)
    #a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
    #a_missile.update()
    
    # Updated scores and Lives
    canvas.draw_text("Lives: "+str(lives) , [20, 20] , 20 , "White")
    canvas.draw_text("Score: "+str(score) , [WIDTH-100, 20] , 20 , "White")
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2), splash_info.get_size())
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    
    if started and len(rock_group) < 12:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .8, random.random() * .6 - .8]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        
        ship_pos = my_ship.get_position()
        distance = math.sqrt(math.pow(rock_pos[0]- ship_pos[0],2) + math.pow(rock_pos[1] - ship_pos[1],2))
        if distance > a_rock.get_radius() + my_ship.get_radius() + 5:
            rock_group.add(a_rock)
        

# draw and update rocks on the canvas        
def process_sprite_group(canvas , rock_set):
    for item in set(rock_set):
        item.draw(canvas)
        if item.update():
            rock_set.remove(item)
    

# generate random position
def generate_random_pos():
    X = random.randint(10 ,WIDTH-10 )
    start = random.choice([0,HEIGHT-50])
    Y = 0
    if X <= 50 or X >= WIDTH - 50:
        Y = random.randint(10 ,HEIGHT-10 )
    else:
        Y = random.randint( start , start+50)
    
    return [X,Y]
    
# key down handler
def key_down(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.update_anguler_vel("LEFT")
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.update_anguler_vel("RIGHT")
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        

# key up handler
def key_up(key):
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.update_anguler_vel("NONE")
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(False)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

