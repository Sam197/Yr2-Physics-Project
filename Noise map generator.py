import random
import pygame
import customRando


SCREENX = 1000
SCREENY = 403
BLACK = (0,0,0)
WHITE = (255,255,255)


def randy(screen):
    '''
    Using a custom implentation of the Cliff PRNG, the colours for each pixel are pre-calcuated, in constast to below.
    This is for performance reasons
    '''
    lent = SCREENX*SCREENY
    colours = [round(x) for x in customRando.randomFloats(lent)]
    outstr = ""
    for colour in colours: outstr += str(colour)
    #print(outstr)
    x = 0
    y = 0
    for pixel, colour in enumerate(colours):
        if colour == 0:
            pygame.draw.rect(screen, BLACK, ((x,y), (1,1)))
        else:
            pygame.draw.rect(screen, WHITE, ((x,y), (1,1)))
        x += 1
        if x > SCREENX:
            x = 0
            y+= 1

def randofiy(screen):
    '''
    Uses the built in random library to produce the noise map, as this PRNG is much more efficient time wise, the
    colours do not need to be pre-calcuated
    '''
    for y in range(SCREENY):
        for x in range(SCREENX):
            pygame.draw.rect(screen, (round(255*random.random()),round(255*random.random()), round(255*random.random())), ((x,y), (1,1)))

def randification(screen):
    import tkinter as tk
    from tkinter import messagebox, filedialog
    import pickle
    def get_data():
        root = tk.Tk()
        #root.withdraw()
        root.filename = filedialog.askopenfile(mode='r')
        try:
            with open(root.filename.name, 'rb') as ins:
        
                data = pickle.load(ins)
            messagebox.showinfo('Loaded', 'Loaded Sucessfully')
        except:
            messagebox.showinfo("Did Not Load", "Unspecified Error") 
        root.destroy()
        return data
    x, y = zip(*get_data())
    data = x+y
    x, y = (0,0)
    foo = ""
    for datum in data:
        random.seed(datum)
        col = round(random.random())
        foo += str(col)
        if col == 0:
            pygame.draw.rect(screen, BLACK, ((x,y), (1,1)))
        else:
            pygame.draw.rect(screen, WHITE, ((x,y), (1,1)))
        x += 1
        if x > SCREENX:
            x = 0
            y += 1
        if x > SCREENX and y > SCREENY:
            break
    print(foo)


def main():

    screen = pygame.display.set_mode((SCREENX, SCREENY))
    randification(screen)
    running = True
    saveNum = 1  #Used to not overwrite image saves

    while running:

        pygame.display.flip()

        for event in pygame.event.get():  #Some pygame boiler plate
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  #Produce a new noise map when enter key pressed
                    pygame.image.save(screen, f'RandomPend{saveNum}.png')  #Takes the screen and saves to a .png
                    saveNum += 1
                    print("Randifiying")
                    randofiy(screen)
                    print("Randified")

if __name__ == "__main__":
    main()
