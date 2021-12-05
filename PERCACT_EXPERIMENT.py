### IMPORTING NECESSARY PACKAGES:
from psychopy import visual, core, event, gui, data, sound   
import pandas as pd 
import glob 
import random 

#Initialize dialogue box
Dialoguebox = gui.Dlg(title = "funky problem spice(ALSO CALLLED BEST GRP EVERZZZ)")
Dialoguebox.addField("Participant ID (just make up one):")
Dialoguebox.addField("Age:")
Dialoguebox.addField("Gender:", choices = ["Female","Male","Other"])
Dialoguebox.addField("Condition:(Researcher chooses)", choices = ["0","1"])
Dialoguebox.show()

#Save data from dialoguebox
if Dialoguebox.OK:
    ID = Dialoguebox.data[0]
    Age = Dialoguebox.data[1]
    Gender = Dialoguebox.data[2]
    Condition = Dialoguebox.data[3]
elif Dialoguebox.Cancel:
    core.quit()


#getting the date and timestamp to make an unique logfile name we will remember
date = data.getDateStr()

#setting the variables of the data 
columns = ["Timestamp","ID","Age","Gender","Condition","ReactionTime", "Colourtask", "Colourrating", "Stimulus"]
DATA = pd.DataFrame(columns = columns)


#VARIABLER
#defining stop watch
stopwatch = core.Clock()
#ad a certain point we would like to reset - in the beginning of a new stimuli eg.
stopwatch.reset()

#### --- MAKING TEXTS USED IN THE EXPERIMENT: ---#####
txt_introduction_taste = '''
Welcome to our experiment!\n\n
In a moment, you will see a grid of 8 x 6 coloured circles .\n\n
The grid will contain either a yellow or red circle.
In every trial you have to answer if the grid contains a red circle (r)or a yellow circle (y). You submit your response by pressing either r (for red) or y (for yellow) on the keyboard.\n\n\n
Press any key when you are ready to continue. '''

txt_instruction = '''
Before you start the experiment, we will ask to give you a piece of hard candy.\n\n
We will ask you to close your eyes as we put the candy into your mouth.\n\n
You will have to keep the candy in your mouth and suck on it continuingly throughout the experiment.\n\n
Remember that for each trial you have to answer if the grid contains a red circle (r)or a yellow circle (y).\n\n\n
Press any key when you are ready to start the experiment.
'''


txt_introduction_control =  ''' 
Welcome to our experiment!\n\n
In a moment, you will see a grid of 8 x 6 coloured circles .\n\n
The grid will contain either a yellow or red circle.
In every trial you have to answer if the grid contains a red circle (r)or a yellow circle (y). You submit your response by pressing either r (for red) or y (for yellow) on the keyboard.\n\n\n
Press any key when you are ready to continue.
'''

# potential middle pause new taste text:
txt_break = ''' new taste will be given to you '''

txt_bye = '''
The experiment is done. Thank you for your participation'''

txt_finish_colour = '''You are now done with the first part of the experiment. \n
You are now to rate the colour of the taste you were given: \n
A color spectrum and a scale will be shown to you shortly,  \n
Click with the mouse which colour on the scale you found to be the best match to your taste.  \n \n
Press space to continue.'''


texts = []
texts.append(txt_introduction_taste)
texts.append(txt_introduction_control)


###defining the image:
stimuli = glob.glob("/Users/laura/Google Drev/UNI 3.0/Perception and Action/EXAM/stimuli/stimulus*.jpg")

##FUNCTION TEXT
## function for showing text and waiting for key press
def msg_func(txt):
    message = visual.TextStim(win, text = txt, height = 0.05)
    message.draw()
    win.flip()
    event.waitKeys(keyList=["space"])

#Initialize window 
win = visual.Window(fullscr = True, units = "pix", color = "Black")
### SHOW INTRODUCTION 

#msg_func(txt_introduction_control)

for i in texts:
    if Condition == "0":
        msg_func(texts[0])
    else:
        msg_func(texts[1])

msg_func(txt_instruction)



### show and press yellow or red and save time
suc_count = 0
while suc_count < 5:
    #Cross
    cross = visual.ShapeStim(win, vertices=((0,-50),(0,50),(0,0),(-50,0),(50,0)), lineWidth = 2, closeShape = False, lineColor = "White")
    cross.draw()
    win.flip()
    core.wait(1)
    image = stimuli[random.randint(0,4)]
    img = visual.ImageStim(win, image = image)
    img.draw()
    stopwatch.reset()
    win.flip()
    key = event.waitKeys(keyList = ["y","r","escape"])
    reaction_time = stopwatch.getTime()
    if image[-5] == "y" and key[0] == "y" or image[-5] == "r" and key[0] == "r":
        suc_count = suc_count + 1 
    elif key[0] == "escape":
        core.quit()
        win.close()
    else:
        suc_count = 0
    DATA = DATA.append({
        "Timestamp":date,
        "ID": ID,
        "Age":Age,
        "Gender": Gender,
        "Condition": Condition,
        "Colourtask": key,
        "Stimulus": img,
        "ReactionTime": reaction_time}, ignore_index = True)



msg_func(txt_finish_colour)


### ---- COLOUR RATING ---- ####
# making window:
win_color = visual.Window(color = "black", fullscr = True)
#Defining stimulus image
color_stimuli= visual.ImageStim(win_color,image="/Users/laura/Desktop/GitHub PercAct/colour_spectrum.jpg",pos = [0,0.3],size=(1.2,2))



#Defining scale function
ratingScale = visual.RatingScale(win_color, 
scale = None,          #This makes sure there's no subdivision on the scale.
low = 1,               #This is the minimum value I want the scale to have.
high = 20,             #This is the maximum value of the scale.
singleClick = True,    #This allows the user to submit a rating by one click.
showAccept = False,    #This shows the user's chosen value in a window below the scale.
markerStart = 10,       #This sets the rating scale to have its marker start on 5.
#labels = ['Negative Emotion', 'Positive Emotion'], #This creates the labels.
pos = [0, -0.6],
size = 2)      #This sets the scale's position.


while ratingScale.noResponse:
    color_stimuli.draw()
    ratingScale.draw() 
    win_color.flip()
    rating = ratingScale.getRating()
    print(rating)

win_color.close()


DATA = DATA.append({
    "Colourrating": rating
    }, ignore_index = True)


msgg = visual.TextStim(win, text = txt_bye, height = 0.05)
msgg.draw()
core.wait(2)
win.close()


## saving data
#make logfile name
logfilename = "/Users/laura/Desktop/GitHub PercAct/logfiles/logfile_{}_{}_{}.csv".format(ID, date, Condition)
DATA.to_csv(logfilename)