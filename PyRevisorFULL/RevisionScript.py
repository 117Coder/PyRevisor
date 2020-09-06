import os
import sys
import random
import re
import time
from datetime import datetime
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, inch, mm, pica, toLength
from fpdf import FPDF

import PySimpleGUI as sg



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


holding_dict = {}
DONOTDESTROYONLOAD = {}
review_bank = {}
final_score = ''

layout =    [[sg.Text("SELECT NOTE FILE", font='Arial 60')],[sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False)],
            [sg.FileBrowse(target='_FILEBROWSE_', size=(20,20), font="Arial 20")]]

window = sg.Window('Find File').Layout(layout)

           
event, values = window.Read()

print(str(values['Browse']))

window.close()
file = values['Browse']
#file = sys.argv[1]

file = str(file)




q_counter = -1
alternator = 1

def populate_dict(file):
    global alternator
    global q_counter
    with open(file, 'r') as f:
    #regex = r"([\w\d \/\^\*\(\)\<\>]*)\?([\w\d \/\^\*\(\)\<\>]*)"
        for line in f:
            if line.strip():
                if alternator == 1:
                    #query = re.search(regex, line)
                    question = line.strip()
                    alternator += 1
                elif alternator == 2:
                    answer = line.strip()
                    holding_dict[question] = answer
                    DONOTDESTROYONLOAD[question] = answer
                    q_counter += 1
                    alternator = 1
        

def ask_away(bank,top_index):
    global review_bank
    global final_score
    start_qs = top_index + 1
    
    q_num = 1
    correct_qs = 0
    while bank != {}:
        index = random.randint(0,top_index)
        bank_of_qs = list(bank.keys())
        ask_q = bank_of_qs[index]
        ask_a = bank[ask_q]
        del bank[ask_q]
        top_index -= 1
        thepercent = 0
        if q_num-1 == 0:
            thepercent=0
        else:
            thepercent=int(((correct_qs/(q_num-1))*100))
        layout = [  [sg.Text("Q{}".format(q_num), font='Arial 60')],
            [sg.Multiline('QUESTION {}: {}'.format(q_num, ask_q), font='50',size=(40,15), auto_size_text=True, disabled=True, background_color='#63778D', text_color='white', autoscroll=True, border_width=0)],
            [ sg.InputText(size=(50,30),font="100")],
            [sg.Button('Ok', size=(5,2))],[sg.Text("Question {}  of  {}".format(q_num, start_qs),font='50',size=(50,1), auto_size_text=True)],
            [sg.Text("{} correct questions out of {} answered".format(correct_qs, q_num-1),font='50',size=(50,1), auto_size_text=True)],
            [sg.Text("{}% success so far".format(thepercent),font='50',size=(50,1), auto_size_text=True)]]
        print(start_qs)
      
        window = sg.Window("QUESTION{}".format(q_num), layout, size=(400,500))
        event, values = window.read()
        print("")
        print("{}----------Q{}----------{}".format(bcolors.WARNING,q_num,bcolors.ENDC))
        print("{}QUESTION {}:{} {}".format(bcolors.WARNING,q_num,bcolors.ENDC, ask_q))
        #user_answer = input("")
        user_answer = values[1]
        print(user_answer)
        print(event)
        window.close()
        if user_answer.upper() == ask_a.upper():
            layout = [  [sg.Text("Correct!", font='Arial 60', background_color='green')],
            [sg.Multiline('QUESTION {}: {}'.format(q_num, ask_q), font='50',size=(40,20), auto_size_text=True, background_color='green', disabled=True, text_color='white', autoscroll=True, border_width=0)],
            [ sg.Text("ANSWER: " + ask_a,font='50',size=(20,5),background_color='green', auto_size_text=True)],
             ]
            window = sg.Window("QUESTION{}".format(q_num), layout, background_color='green', auto_close=True,auto_close_duration=2, size=(400,500))
            event, values = window.read()
            
            window.close()
            print("")
            print("{}~~CORRECT!~~{}".format(bcolors.BOLD,bcolors.ENDC))
            print("{}+1{} score".format(bcolors.HEADER,bcolors.ENDC))
            correct_qs += 1
            review_bank[ask_q] = "CORRECT"
        elif user_answer.upper() != ask_a.upper():

            layout = [  [sg.Text("INCORRECT", font='Arial 60', background_color='red')],
            [sg.Multiline('You said: {}'.format(user_answer), font='50',size=(40,1), auto_size_text=True, background_color='red', disabled=True, text_color='white', autoscroll=True, border_width=0)],
            [sg.Multiline('The correct answer was: {}'.format(ask_a), font='50',size=(40,8), auto_size_text=True, background_color='black', disabled=True, text_color='green', autoscroll=True, border_width=0)],
            [sg.Text('Was your answer close enough? Do you want to override?', font='Arial 12',size=(50,7), auto_size_text=True, background_color='red')],
            [sg.Button('Yes', size=(5,2)),sg.Button('No', size=(5,2))] ]
            window = sg.Window("Incorrect", layout, background_color='red', size=(400,500))
            event, values = window.read()
            print(event)
            
            window.close()
            print("")
            print("{}~~INCORRECT~~{}".format(bcolors.FAIL, bcolors.ENDC))
            print("")
            print("{}The correct answer was:{} {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.UNDERLINE,ask_a,bcolors.ENDC))
            print("")
            print("")
            print("{}Was your answer close enough? Do you want to manual override?{}".format(bcolors.OKBLUE,bcolors.ENDC))
            print("")
            #override_opt = input("{}yes or no: {}".format(bcolors.OKBLUE,bcolors.ENDC))
            if event.upper() == "YES":
                layout = [  [sg.Text("Correct!", font='Arial 60', background_color='green')],
                [sg.Multiline('QUESTION {}: {}'.format(q_num, ask_q), font='50',size=(40,20), auto_size_text=True, background_color='green', disabled=True, text_color='white', autoscroll=True, border_width=0)],
                [ sg.Text("ANSWER: " + ask_a,font='50',size=(20,5),background_color='green', auto_size_text=True)],
                 ]
                window = sg.Window("QUESTION{}".format(q_num), layout, background_color='green', auto_close=True,auto_close_duration=2, size=(400,500))
                event, values = window.read()
            
                window.close()
                print("")
                print("{}<<OVERRIDEN>>{}".format(bcolors.BOLD,bcolors.ENDC))
                print("{}~~CORRECT!~~{}".format(bcolors.BOLD,bcolors.ENDC))
                print("{}+1{} score".format(bcolors.HEADER,bcolors.ENDC))
                correct_qs += 1
                review_bank[ask_q] = "CORRECT"
            else:
                review_bank[ask_q] = "INCORRECT"
        q_num += 1
    print("")
    print("")
    print("")
    print("")
    print("{}----------COMPLETE!----------{}".format(bcolors.OKBLUE,bcolors.ENDC))
    print("{}Your score was:{} {} / {}".format(bcolors.HEADER,bcolors.ENDC,correct_qs,q_num-1))
    print("")
    print("")
    print("")
    print("")

    
    final_score = str(correct_qs) + " / " + str(q_num-1)
    print(int((correct_qs/(q_num-1))*100))
    layout = [  [sg.Text("FINISHED!".format(q_num), font='Arial 60')],
            [sg.Text('Your score is: {}'.format(final_score), font='50',size=(50,15), auto_size_text=True)],
            [sg.Text('Your percentage is: {}%'.format(int((correct_qs/(q_num-1))*100)), font='50',size=(50,6), auto_size_text=True)],
            [sg.Button('Ok', size=(5,2))] ]
    window = sg.Window("DONE".format(q_num), layout, size=(400,500))
    event, values = window.read()
    window.close()            
        

def generate_PDF():
    global review_bank
    global DONOTDESTROYONLOAD
    global file
    global final_score

    file = file.upper()

    now = datetime.now()
    format = "%d-%m-%Y %H~%M~%S"
    time = now.strftime(format)
    
    regex = r"([\w]*)\."
    query = re.search(regex, file)
    new_file_name = query.group(1)
    full_file_name = "{}-({})".format(new_file_name,time)
    hello = "hi"
    
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", size=18)
    pdf.multi_cell(w=200,h=10,txt=full_file_name,align="C")

    pdf.set_font("Arial", "B", size=15)
    pdf.multi_cell(w=200,h=10,txt="Question Bank",align="L")

    text = ""
    
    for key in DONOTDESTROYONLOAD.keys():
        
        answer = DONOTDESTROYONLOAD[key]
        text += key + "\n" + answer + "\n\n"
        
        
    pdf.set_text_color(0,0,255)


    pdf.set_font("Arial", size=11)
    pdf.multi_cell(w=200,h=10,txt=text,align="L")
        
    pdf.set_text_color(0,0,0)
  
    pdf.set_font("Arial", "B", size=15)
    pdf.multi_cell(w=200,h=10,txt="Review",align="L")

    pdf.set_text_color(0,0,255)

    reviewtext = ""
    
    for key in review_bank.keys():
        
        out = review_bank[key]
        if out == "INCORRECT":
            reviewtext += key + "\n" + out + "   Correct Answer = ("+DONOTDESTROYONLOAD[key]+")"+"\n\n"
        else:
            reviewtext += key + "\n" + out + "\n\n"
        
        

    pdf.set_font("Arial", size=11)
    pdf.multi_cell(w=200,h=10,txt=reviewtext,align="L")  

    pdf.set_text_color(212,0,255)

    pdf.set_font("Arial", "B", size=13)
    pdf.multi_cell(w=200,h=10,txt=final_score,align="L")
    
    pdf.output(full_file_name)

    layout = [  [sg.Text("A REPORT HAS", font='Arial 35')],[sg.Text("BEEN CREATED", font='Arial 35')],
            [sg.Text('You have a PDF report waiting! It contains all the questions and answers, as well as your score and how you did.', font='50',size=(30,15), auto_size_text=True)],
            [sg.Text('The file\'s name is: {}'.format(full_file_name), font='50',size=(50,4), auto_size_text=True)],
            [sg.Button('Ok', size=(5,2))] ]
    window = sg.Window("Report", layout, size=(400,500))
    event, values = window.read()
    window.close()


populate_dict(file)
ask_away(holding_dict,q_counter)
generate_PDF()
