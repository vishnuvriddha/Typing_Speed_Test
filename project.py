
import sys
import time
import random
import pygame
from pygame.locals import *


# In[2]:


class Game:
    
    def __init__(self):
        self.w = 750      #width of game box is 750
        self.h = 500      #height of game boc is 500
        
        self.inputs = ''   #taking input 
        self.words = ''
        
        self.start_time = 0   #measuring time at beginning
        self.total_time = 0   #measuring end time 
        
        self.end = False     # to show results at end and calculate time (total_time-start_time if end=true)
        self.reset=True      # will be used for resetting 
        self.active = False  #used to reset the timer and click 
        
        self.accuracy = '0%'                        #intializing accuracy (count/len(self.words)*100)
        self.results = 'Time:0 Accuracy:0 % Wpm:0 ' #will display results
        self.wpm = 0                                #initializing wpm = correct charx100/total chars
        
        
        self.chead = (255,213,102)  # the tuples assigned are rgb values of the respective colours
        self.ctext = (240,240,240)
        self.cresult = (255,70,70)
        
        
        pygame.init()               #initialize all imported pygame modules
        
        self.open_img = pygame.image.load('opening.png')                       #opening image & transform size
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))
        
        self.bg = pygame.image.load('bkg.jpg')               #game background image
        self.bg = pygame.transform.scale(self.bg, (500,750))
        
        self.screen = pygame.display.set_mode((self.w,self.h))  #This function will create a display Surface  
        
        pygame.display.set_caption('Typing Speed Time')   #creates a caption on the display window

        
        


    # In[3]:


    #in order to draw further on the scren we will use a text_drawing method
    #the argument takes the input screen, message, font size, y cordinate, colour of font

    def text_drawing(self, screen, msg, yaxis, font_s, color):
        
        font = pygame.font.Font(None, font_s)  #create a new  Font object
        
                                                        # create a text surface object,
                                                        # on which text is drawn on it.
        text = font.render(msg, 1,color)
        
        
        text_rect = text.get_rect(center=(self.w/2, yaxis)) # put text rectangle at desired centre 

        screen.blit(text, text_rect)                    # draw text at text_rect place
        
        
        pygame.display.update()                       #update and show the following changes on the screen


    # In[4]:


    #The get_sentence() method will open up the file and return a random sentence from the list



    def get_sentence(self):
        
        
        
        #split the whole txt file sentence list through the \n character to get sentence

        
        froms= open('fillers.txt').read()
        fillers = froms.split('\n')
        sentence = random.choice(fillers)
        return sentence
                        
     


    # In[5]:


    def results_display(self,screen):
        
        if(not self.end):      #self.end initialized as false, ie not end = true, till that time calculate
            
            self.total_time = time.time() - self.start_time  #calculating time 
            
            #Calculating accuracy 
            
            counter = 0                            #initialize a counter 
            for i,tu in enumerate(self.words):      # we will use words to get the sentence, then enumerate it
                                                   # from 0-n , then check whether letter i of input matches
                                                   #the letter c , ie of c=i position of enumerated sentence.
                    
                
                #since the user may type an incorrect character at desired place, we will use the try and except
                #command in order to make sure that we bypass all errors, otherwise 'if' would be fine
                
                try:
                    if self.inputs[i] == tu:        
                        counter += 1              #increase counter for each instance when i and c matches
                                                  #if all are correct then counter=len(self.words)
                except:
                    pass
            self.accuracy = counter/len(self.words)*100    #accuracy formula
            
            #Calculating wpm = words per minute 
            
            self.wpm = len(self.inputs)*60/(5*self.total_time)  #this is the given formula
            self.end = True             #end was initialized as false earlier,by setting it true, means that it has taken time
            print(self.total_time)
            
            #making the standard results format ie:: 'Time:0 Accuracy:0 % Wpm:0 '
            
            self.results = 'Time:'+str(round(self.total_time)) +" secs Accuracy:"+ str(round(self.accuracy)) + "%" + ' Wpm: ' + str(round(self.wpm))
                
            
             # drawing the icon image
                
            self.newimg = pygame.image.load('icons.png')
            self.newimg = pygame.transform.scale(self.newimg, (150,150))
            
            
            screen.blit(self.newimg, (self.w/2-75,self.h-140))   
            self.text_drawing(screen,"Reset", self.h - 70, 26, (100,100,100))
            
            #update and display the results
            print(self.results)
            pygame.display.update()

        


    # In[6]:


    # we will create a method here called reset_game in order to reset all the variables used here
    # we would also need to run a loop in order to capture events committed by mouse and keyboards
    def run(self): 
        
        self.reset_game()    # we will call this method right here in order to reset all variables at the beginning
                             # the reset_game() method will be defined in the next block
            
        self.running=True    #initializing variable for the 'while' loop
        
        while(self.running):
            
            clock = pygame.time.Clock()  #initialize the clock
            
            self.screen.fill((0,0,0), (50,250,650,50))
            pygame.draw.rect(self.screen,self.chead, (50,250,650,50), 2)   #drawing the header
            
            
            # updating user input based text
            self.text_drawing(self.screen, self.inputs, 274, 26,(250,250,250))
            pygame.display.update()
            
            
            for event in pygame.event.get():
                
                if event.type == QUIT:     #mode of exiting the sequence
                    self.running = False
                    sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONUP:   #receives the position of the box of mouseclick
                    x,y = pygame.mouse.get_pos() 
                    
                    # position of input box
                    
                    if(x>=50 and x<=650 and y>=250 and y<=300):  #check whether mouseclick pos lies in input box position
                        self.active = True
                        self.inputs = ''
                        self.start_time = time.time()
                        
                     # position of reset box
                    
                    if(x>=310 and x<=510 and y>=390 and self.end): #check whether mouseclick pos lies in reset box position
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()
                        
                        
                elif event.type == pygame.KEYDOWN:  #checks whether a key has been pressed
                    
                    if self.active and not self.end: #self.active= true means that typing has begun and
                                                     #self.end= false means that typing has not ended.
                            
                        if event.key == pygame.K_RETURN:  #if a key is pressed then print the result on screen
                            
                            print(self.inputs)
                            self.results_display(self.screen)
                            print(self.results)
                            self.text_drawing(self.screen, self.results,350, 28, self.cresult) #call function to display text
                            self.end = True                            #self.end = true means timer ends here
                        
                        elif event.key == pygame.K_BACKSPACE:      #if backspace is pressed then inputs will go one lesser
                            
                            self.inputs = self.inputs[:-1]
                            
                        else:                            #using try and pass inorder to bypass any erros and allow smooth run
                            try:
                                self.inputs += event.unicode  #recognize special characters like ',".;@#$% etc
                            except:
                                pass
                            
            pygame.display.update() #after taking above commands, allows screen to be available to user 
            
        clock.tick(60)        #allows 60 frames per second


    # In[7]:


    def reset_game(self):

        self.screen.blit(self.open_img, (0,0)) #reopen opening image
        pygame.display.update()                #readjust display
        time.sleep(1)                          # delays further execution by one second, ie allows opening image for 1 sec

        self.inputs=''                           # initializing inputs the way it was in __init__(self)
        self.words = ''

        self.start_time = 0                  # intializing time the way it was in __init__(self)
        self.total_time = 0
        self.wpm = 0


        self.reset=False
        self.end = False
        self.active=False


        # Getting a random sentence again
        self.words = self.get_sentence()
        if (not self.words): self.reset_game()

        #drawing the heading again


        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))


        msg = "Typing Speed Test"

        self.text_drawing(self.screen, msg,80, 80,self.chead)

        # draw the rectangle for input box
        pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)

        # draw the sentence string
        self.text_drawing(self.screen, self.words,200, 28,self.ctext)
        pygame.display.update()


    # In[8]:


Game().run()
