import webbrowser
import os
import datetime

def handle_command(command):
    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"
    elif "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"
    elif "open github" in command:
        webbrowser.open("https://github.com")
        return "Opening GitHub"
    elif "open vs code" in command:
        code_path = "C:\\Users\\keyur\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(code_path)
    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(chrome_path)
    elif "word" in command:
        word_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
        os.startfile(word_path)
    elif "excel" in command:
        excel_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
        os.startfile(excel_path)
    elif "powerpoint" in command:
        powerpoint_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
        os.startfile(powerpoint_path)
    elif "notepad" in command:
        notepad_path = "C:\\Windows\\system32\\notepad.exe"
        os.startfile(notepad_path)
    elif "cmd" in command:
        cmd_path = "C:\\Windows\\system32\\cmd.exe"
        os.startfile(cmd_path) 
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}"
    elif "terminate" in command:
        print("Terminating")
        exit()
        return "Terminating"
    
    return None
