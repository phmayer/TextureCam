import pygame
import vkeyboard
import keyboard
import pygame_textinput

from app_buttons import Button


#constants:
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480


#functions:
#button:
def button_action():
    print("Button released - Function executed!")
    overlay_screen.fill("green")
    pygame.display.flip()
    kb.start()

    while running:
        events = pygame.event.get()

        # Feed it with events every frame
        textinput_gdrive.update(events)
        # Blit its surface onto the screen
        overlay_screen.blit(textinput_gdrive.surface, (400, 200))
        pygame.display.update()

        for event in events:
            if event.type == pygame.QUIT:
                exit()
        clock.tick(30)

    


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


#keyboard setup
kb = vkeyboard.VirtualKeyboard()
kb.engine()



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


