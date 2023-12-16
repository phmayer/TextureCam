import pygame

import pygame_textinput
from pygame_vkeyboard import *

from app_buttons import Button


#constants:
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480

#global variables:
textinput1 = ''


#functions:

def consumer(text):
    textinput1 = '%s' % text
    print('Current text : %s' % text)

#button:
def button_action():
    print("Button released - Function executed!")
    overlay_screen.fill("white")
    pygame.display.flip()
    #kb.start() #TODO probably get rid of that on screen bs keybaord shit

    # Initializes and activates vkeyboard
    layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
    keyboard = VKeyboard(overlay_screen, consumer, layout)

    #create some text field bullshit:
    font = pygame.font.Font('freesansbold.ttf', 32)
    

    while running:
        events = pygame.event.get()

        keyboard.update(events)
        keyboard.draw(overlay_screen)
        # Feed it with events every frame
        #textinput_gdrive.update(events)
        # Blit its surface onto the screen
        #overlay_screen.blit(textinput_gdrive.surface, (400, 200))


        text = font.render(textinput1, True, "black", "pink")
        textfield = text.get_rect() #TODO HOW THE FUCK DO I MAKE THIS UPDATE ITSELF?????
        textfield.center = (400, 100)
        overlay_screen.blit(text,textfield)


        pygame.display.update() #WHAT TGE FUKC which one do i need?
        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                exit()
        #clock.tick(30) #TODO what the hell am i supposed to put here do it need this?
        # i hate pygame

    


# pygame setup
pygame.init()
clock = pygame.time.Clock()
pygame_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
overlay_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#your button parameters
cameraButton_up = pygame.image.load("buttonUP.png")  
cameraButton_down = pygame.image.load("buttonDOWN.png")  
#(dont touch,x position, y position, imageUP,imageDOWN, the what button do)
camera_button  = Button(pygame_screen,200,200,cameraButton_up,cameraButton_down, action = button_action)

# Create TextInput-object
textinput_gdrive = pygame_textinput.TextInputVisualizer()




running = True

while running:
    pygame_screen.fill("pink")
	
    camera_button.draw()
    pygame.display.flip()
	
	


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
			
        camera_button.handle_event(event)


pygame.quit()


