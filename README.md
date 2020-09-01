# PyRevisor
This is a script intended to help with exam revision. While studying, take notes in a text file. Make sure that your notes span two lines (Example in the readme). Once you have finished taking notes, run the script with the text file, and the script will quiz you on your notes in a random order. Once done, it will give you your score, as well as generate a PDF with all the questions and answers, and how you did

## How to take notes

In your text file, a 'note' should span two lines. The first line will be given to you, and you will need to finish state the second line.
For example, this is an example of a good note:
  
    All element names start with a
    Capital letter
  
## Libraries

You will need these libraries to run the script properly. 

    - os
    - sys
    - random
    - re
    - time
    - datetime
    - fpdf
    
(Downloading with pip3.8, feel free to use whichever download method suits you best)

    pip3.8 install re
    pip3.8 install fpdf
    
## How to structure your directories

You should have a new instance of the script for each subject you study
When initiaiting the script, make sure you are in the topmost directory, for example:

    - RevisionScriptTOP
    -   -> Chemistry
    -   ->  -> Notes.txt
    -   ->  -> RevisionScript.py
    -   -> Physics
    -   ->  -> Notes.txt
    -   ->  -> RevisionScript.py
    -   -> Biology
    -   ->  -> Notes.txt
    -   ->  -> RevisionScript.py
    
In this example, you will run the script from the directory 'RevisionScriptTOP'
    
