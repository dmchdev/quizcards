import re
import argparse
import random
import wx

class Frame(wx.Frame):
    def __init__(self, parent=None, id=-1, size=(650, 700), pos=wx.DefaultPosition,
                 title='Test Cards', style=wx.MAXIMIZE_BOX | wx.RESIZE_BORDER
                 | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX):
        wx.Frame.__init__(self, parent, id, title, pos, size=size)
        self.question_list=[]
        self.InitUi()

    def InitUi(self):
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        open_file_item = filemenu.Append(wx.ID_OPEN, 'Open Test File')
        filemenu.AppendSeparator()
        exit_item = filemenu.Append(wx.ID_EXIT, 'Exit', 'Exit Application')
        menubar.Append(filemenu, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, exit_item)
        self.Bind(wx.EVT_MENU, self.OnFileOpen, open_file_item)
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.question_label = wx.StaticText(panel, label="QUESTION: ", style=wx.ALIGN_LEFT)
        vbox.Add(self.question_label,0,  wx.ALL|wx.EXPAND|wx.ALIGN_LEFT, 5)
        self.question_text = wx.TextCtrl(panel,size = (600,50), style=wx.TE_MULTILINE)
        vbox.Add(self.question_text,0,  wx.ALL|wx.EXPAND|wx.ALIGN_LEFT, 10)
        self.show_answer_btn = wx.Button(panel, label="Show Answer")
        self.show_answer_btn.Bind(wx.EVT_BUTTON, self.OnClickedShowAnswer)
        vbox.Add(self.show_answer_btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.answer_label = wx.StaticText(panel, label="ANSWER: ", style=wx.ALIGN_LEFT)
        vbox.Add(self.answer_label,0,  wx.ALL|wx.EXPAND|wx.ALIGN_LEFT, 5)
        self.answer_text = wx.TextCtrl(panel,size = (600,400), style=wx.TE_MULTILINE)
        vbox.Add(self.answer_text,0,  wx.ALL|wx.EXPAND|wx.ALIGN_LEFT, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL) 
        hbox.AddStretchSpacer(1) 
        self.next_question_btn = wx.Button(panel, label="Next Question")
        self.next_question_btn.Bind(wx.EVT_BUTTON, self.OnClickedNextQuestion)
        hbox.Add(self.next_question_btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.random_question_btn = wx.Button(panel, label="Random Question")
        self.random_question_btn.Bind(wx.EVT_BUTTON, self.OnClickedRandomQuestion)
        hbox.Add(self.random_question_btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.restart_questions_btn = wx.Button(panel, label="Restart Questions")
        self.restart_questions_btn.Bind(wx.EVT_BUTTON, self.OnClickedRestartQuestions)
        hbox.Add(self.restart_questions_btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        hbox.AddStretchSpacer(1) 
        vbox.Add(hbox,1,wx.ALL|wx.EXPAND)
        panel.SetSizer(vbox)
    
    def OnClickedRestartQuestions(self, event):
        if self.question_list:
            self.question_iterator = iter(self.question_list)
        else:
            self._show_message("Nothing to restart. Load a file first", "File Load Error")

    def OnClickedNextQuestion(self, event):
        try:
            if not self.question_list:
                self._show_message()
            else:   
                self.current_question = _get_question(next(self.question_iterator))
                self.question_text.SetValue(self.current_question[0])
                self.answer_text.SetValue(" ")
        except StopIteration:
            self._show_message("NO MORE QUESTIONS TO ASK. ALL DONE", "END OF TEST")


    def OnClickedRandomQuestion(self, event):
        try:
            self.current_question = _get_question(random.choice(self.question_list))
            self.question_text.SetValue(self.current_question[0])
            self.answer_text.SetValue(" ")
        except:
            self._show_message()

    def OnClickedShowAnswer(self, event):
        try:
            self.current_question
            self.answer_text.SetValue(self.current_question[1])
        except:
            self._show_message()
            
    def _show_message(self,
                      message="Must Load File Before Clicking This Button",
                      title="File Load Error"):
        with wx.MessageDialog(
            self, message, title,style=wx.OK,
            pos=wx.DefaultPosition) as errorDialog:
                errorDialog.ShowModal()

    def OnFileOpen(self, e):
        with wx.FileDialog(self, "Open Test file", wildcard="Text Files (*.txt)|*.txt",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind    

            # Proceed loading the file chosen by the user
            filename = fileDialog.GetPath()
            try:
                file_content = _get_filecontent(filename)
                self.doLoadFile(file_content)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)
    
    def doLoadFile(self, file_content):
        if "[Answer:]" not in file_content or "[Question:]" not in file_content:
            bad_format_error_message = """This file is not properly formatted.
               Please make sure you prefix your questions with '[Question:] and
               answers with '[Answer:]'"""
            with wx.MessageDialog(
                self,
                bad_format_error_message,
                "Error in file format",
                style=wx.OK, pos=wx.DefaultPosition) as errorDialog:
                errorDialog.ShowModal()
        else:
            self.question_list = _prepare_questions(file_content)
            self.question_iterator = iter(self.question_list)
            self.current_question = _get_question(next(self.question_iterator))
            self.question_text.SetValue(self.current_question[0])
    
    def OnQuit(self, e):
        self.Close()

class TextArea(wx.TextCtrl):
    def __init__(self, parent=wx.Frame, id=wx.ID_ANY, value='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TE_MULTILINE, validator=wx.DefaultValidator,
                 name="ANSWER:"):
        wx.TextCtrl.__init__(self, parent, id, value, pos, size, style, validator, name)

class QuizCardsApp(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def _get_question(question_item):
    question = question_item.split('[ANSWER:]')[0]
    answer = question_item.split('[ANSWER:]')[1]
    return question, answer

def _ask_question(question_item):
    question, answer = _get_question(question_item)
    print('\n'+'='*50 + '\n')
    print("QUESTION:\n" + question + '\n')
    proceed_answer = input("Ready to see the answer?(Y/N): ")
    if proceed_answer.upper() in ["Y", "YES"]:
        print("\nANSWER:") 
        print(answer + '\n')
    else:
        pass 

def _get_filecontent(filename):
    with open(filename, 'r') as quizfile:
        filecontent = quizfile.read()
    return filecontent

def _prepare_questions(filecontent):
    end_pattern = re.compile(r"\[[Ee][Nn][Dd]\]")
    question_pattern = re.compile(r"(\[[Qq][Uu][Ee][Ss][Tt][Ii][Oo][Nn]:\])|(\[[Qq][Uu][Ee][Ss][Tt][Ii][Oo][Nn]\]:)")
    answer_pattern = re.compile(r"(\[[Aa][Nn][Ss][Ww][Ee][Rr]:\])|(\[[Aa][Nn][Ss][Ww][Ee][Rr]\]:)")
    filecontent = filecontent.encode('ascii', 'ignore').decode('ascii')
    filecontent = re.sub(end_pattern, "[END]", filecontent)
    working_tests = filecontent.split('[END]')[0]
    working_tests = re.sub(question_pattern, '[QUESTION:]', working_tests)
    working_tests = re.sub(answer_pattern, '[ANSWER:]', working_tests)
    question_list = working_tests.split('[QUESTION:]')[1:]
    return question_list


def _run_program_cl(args):
    filecontent = _get_filecontent(args.FILENAME)
    question_list = _prepare_questions(filecontent)
    question_iterator = iter(question_list)
    while True:
        if args.RANDOMIZE:
            _ask_question(random.choice(question_list))
        else:
            try:    
                _ask_question(next(question_iterator))
            except StopIteration as e:
                print("\nNO MORE QUESTIONS TO ASK. ALL DONE")
                break
        next_question = input("Next question?(Y/N): ")
        if next_question.upper() not in ["Y", "YES"]:
            print("Exiting program")
            break
    
def _parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-filename', '--FILENAME', type=str, nargs='?', default='TestingQuestionsAndAnswers.txt')
    parser.add_argument('-randomize', '--RANDOMIZE', action='store_true', default=False )
    parser.add_argument('-nogui', '--NOGUI', action='store_true', default=False)
    args = parser.parse_args()
    return args

def main(): 
    args = _parse_cli_args()
    if args.NOGUI:
        _run_program_cl(args)
    else:
        thisapp = QuizCardsApp()
        thisapp.MainLoop()

if __name__ == '__main__':
    main()