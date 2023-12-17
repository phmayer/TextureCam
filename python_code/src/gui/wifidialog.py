import pygame

import pygame_textinput
from pygame_vkeyboard import *

from app_buttons import Button


#constants:
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480
TEXTLABEL1 = 'Input 1:'
TEXTLABEL2 = 'Input 2:'

#global variables:
textinput1 = ''
textinput2 = ''
active_textinput = 1


#functions:
def reset_input_fields(): #TODO probably never need this -> if so remove!
    global textinput1
    global textinput2
    textinput1 = ''
    textinput2 = ''

#this function puts virtual keyboard inputs into the variables
def consumer(text):
    print("text: " + text)
    global active_textinput
    if active_textinput==1:
        global textinput1
        textinput1 = '%s' % text
    elif active_textinput==2:
        global textinput2
        textinput2 = '%s' % text

#gets calles when we click on the input rect
def textinput1_activate():
    global active_textinput
    active_textinput=1
    keyboard.set_text(textinput1)
    print("input 1 active")
    
#gets calles when we click on the input rect
def textinput2_activate():
    global active_textinput
    active_textinput=2
    keyboard.set_text(textinput2)
    print("input 2 active")


#this gets called when the button on the first screen is pressen, it creates a new screen
def button_action():
    global overlay_running
    overlay_running = True
    overlay_screen.fill("black")
    pygame.display.flip()

    # Initializes and activates vkeyboard
    layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
    global keyboard
    keyboard = VKeyboard(overlay_screen, consumer, layout)

    #create font for text fields
    font = pygame.font.Font('freesansbold.ttf', 32)

    while overlay_running:
        events = pygame.event.get()

        #add keyboard
        keyboard.update(events)
        keyboard.draw(overlay_screen)

        #add label 1
        label1=font.render(TEXTLABEL1, True, "white")
        overlay_screen.blit(label1, (350, 10))
        #add text display for input variable 1
        text1=font.render(textinput1, True, "white")
        rect1 = pygame.Rect(200, 45, 400, 40)
        #TODO maybe rust redraw whole screen each time? how do i do that?
        overlay_screen.blit(text1, rect1)
        pygame.draw.rect(overlay_screen, (255,255,255),rect1,2)

        #add label 2
        label2=font.render(TEXTLABEL2, True, "white")
        overlay_screen.blit(label2, (350, 100))
        #add text display for input variable 2
        text2=font.render(textinput2, True, "white")
        rect2 = pygame.Rect(200, 135, 400, 40)
        overlay_screen.blit(text2, rect2)
        pygame.draw.rect(overlay_screen, (255,255,255),rect2,2)

        #draw buttons
        back_button.draw()
        enter_button.draw()

        pygame.display.update()
        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect1.collidepoint(event.pos):
                    #input 1 selected
                    textinput1_activate()
                if rect2.collidepoint(event.pos):
                    #input 2 selected
                    textinput2_activate()
            back_button.handle_event(event)
            enter_button.handle_event(event)
        #clock.tick(30) #TODO what the hell am i supposed to put here do it need this?


def back_button_action():
    #print("hit back button")
    global overlay_running
    overlay_running = False

def enter_button_action():
    #print("hit enter button")
    global overlay_running
    
    #TODO:  HERE WE THEN CAN CALL WHATEVER LOGIC OR FUNCTION WE WANT TO CALL AFTER USER HAS ENTERED THE STUFF

    overlay_running = False



# pygame setup
pygame.init()
clock = pygame.time.Clock()
pygame_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
overlay_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#your button parameters
button_1_up = pygame.image.load("buttonUP.png")  
button_1_down = pygame.image.load("buttonDOWN.png")  
#(dont touch,x position, y position, imageUP,imageDOWN, the what button do)
button_1  = Button(pygame_screen,200,200,button_1_up,button_1_down, action = button_action)

backButton_up = pygame.image.load("goback_button_up.png")  
backButton_down = pygame.image.load("goback_button_down.png")  
#(dont touch,x position, y position, imageUP,imageDOWN, the what button do)
back_button  = Button(pygame_screen,10,10,backButton_up,backButton_down, action = back_button_action)

enterButton_up = pygame.image.load("enter_button_up.png")  
enterButton_down = pygame.image.load("enter_button_down.png")  
#(dont touch,x position, y position, imageUP,imageDOWN, the what button do)
enter_button  = Button(pygame_screen,350,180,enterButton_up,enterButton_down, action = enter_button_action)


# Create TextInput-object
#textinput_gdrive = pygame_textinput.TextInputVisualizer()

#main loop:
running = True
while running:
    pygame_screen.fill("pink")
	
    button_1.draw()
    pygame.display.flip()
	

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
			
        button_1.handle_event(event)


pygame.quit()


