  
#!/bin/sh



#  Created by Pete Hewage
#  Copyright (c) 2020 Pete Hewage, All Rights Reserved.
echo Starting...
echo -Pete Hewage 2020

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

brew install curl wget
brew install python-setuptools python-dev build-essential python-pip
python --version


echo ...
echo 
echo Installing fpdf
pip install fpdf
echo Installing regex
pip install regex
echo Installing datetime
pip install datetime
echo finished!



echo starting script...
python3 RevisionScript.py

