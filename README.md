# quizcards
Python GUI application to set up your own quiz cards

## Prerequisites 

You need to have wxPython installed on your machine for this program to work.

Fill your quizcards.txt with questions/answers, or create your own file in the following format:

```
[Question:] Very Stupid Question

[Answer:] Equally stupid answer

[Question:] Very Stupid Question 2

[Answer:] Equally stupid answer 2
[Question:] Very Stupid Question 3

[Answer:] Equally stupid answer 3
[Question:] Very Stupid Question 4

[Answer:] Equally stupid answer 4
```

### Installation

1. Navigate to quizcards directory

2. Run this command in your favorite command line:

```
pip install -r requirements.txt
```

### Running the program in GUI mode

1. Run the following command in your command line:

```
python quizcards.py 
```

2. Use File menu on the GUI to locate your questions file quizcards.txt etc.

### Running the program in command line mode

1. Run the following command in your command line:

```
python quizcards.py -filename quizcards.txt -nogui -randomize
```
This will load the quizcards.txt file and start your program without the GUI, questions will be picked from the file at random. You can youse your own filename. If you wish not to randomize questions, do not specify the -randomize in the command. 