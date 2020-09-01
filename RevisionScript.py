import os
import sys
import random
import re
import time
from datetime import datetime
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, inch, mm, pica, toLength
from fpdf import FPDF


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

file = sys.argv[1]

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
    q_num = 1
    correct_qs = 0
    while bank != {}:
        index = random.randint(0,top_index)
        bank_of_qs = list(bank.keys())
        ask_q = bank_of_qs[index]
        ask_a = bank[ask_q]
        del bank[ask_q]
        top_index -= 1
        print("")
        print("{}----------Q{}----------{}".format(bcolors.WARNING,q_num,bcolors.ENDC))
        print("{}QUESTION {}:{} {}".format(bcolors.WARNING,q_num,bcolors.ENDC, ask_q))
        user_answer = input("")
        if user_answer.upper() == ask_a.upper():
            print("")
            print("{}~~CORRECT!~~{}".format(bcolors.BOLD,bcolors.ENDC))
            print("{}+1{} score".format(bcolors.HEADER,bcolors.ENDC))
            correct_qs += 1
            review_bank[ask_q] = "CORRECT"
        elif user_answer.upper() != ask_a.upper():
            print("")
            print("{}~~INCORRECT~~{}".format(bcolors.FAIL, bcolors.ENDC))
            print("")
            print("{}The correct answer was:{} {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.UNDERLINE,ask_a,bcolors.ENDC))
            print("")
            print("")
            print("{}Was your answer close enough? Do you want to manual override?{}".format(bcolors.OKBLUE,bcolors.ENDC))
            print("")
            override_opt = input("{}yes or no: {}".format(bcolors.OKBLUE,bcolors.ENDC))
            if override_opt.upper() == "YES":
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



populate_dict(file)
ask_away(holding_dict,q_counter)
generate_PDF()
