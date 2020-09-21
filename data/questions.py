import inquirer
from datetime import datetime

#Asks function, semester, year
def ask_basic():
    return [
        inquirer.List('function',
        message="Which function do you want to use",
        choices = [
            'Search: display remaining seats', 
            'Waiting: notify me if seats left',
            'Save: save class schedule in html file',
            'Register: automatically register classes'],
            ),
            inquirer.List('semester',
            message="Semester",
            choices=['Spring', 'Summer', 'Fall', 'Winter'],
            ),
            inquirer.Text('year',
            message="Year",
            validate=lambda _, year: int(year.strip()) >= 2015 and int(year.strip()) <= 2050,
            ),
    ]

#Asks CRN
def ask_crn():
    return inquirer.text(message="CRNs up to 10 (format: 12345 23456 34567)",
    validate=lambda _, crns: len(crns.split(',')) <= 10 and\
        all(True == y for y in [len(x.strip()) == 5 for x in crns.split()])
        )

#Asks Filename
def ask_filename():
    return inquirer.text(
    message="File name",
    default="pcc_semester.html",
    )

#Asks CRN with Alarm options
def ask_crn_with_option(crns):
    waiting_questions = []
    for idx in range(len(crns)):
        waiting_questions.append(inquirer.List('alarm' + str(idx),
        message=f"When should we notify you for crn:{crns[idx]}",
        choices = ['Open', 'Close', 'Change', 'No'],
        ))
        
    waiting_questions.append(inquirer.Text('rate',
    message="Check seats every __ minutes",
    validate=lambda _, rate: int(rate) >= 1 and int(rate) <= 60
    ))
    return waiting_questions

#Asks time
def ask_time():
    return inquirer.text(
    message="Register Time 24hr (format: 13:10:10)",
    validate=lambda _, time_: int(time_.split(':')[0]) > 0 and int(time_.split(':')[0]) < 24\
        and int(time_.split(':')[1]) >= 0 and int(time_.split(':')[1]) < 60\
            and int(time_.split(':')[2]) >= 0 and int(time_.split(':')[2]) < 60\
                and (datetime(datetime.now().year,
                datetime.now().month, datetime.now().day, int(time_.split(':')[0]), int(time_.split(':')[1]),
                int(time_.split(':')[2], 0)) - datetime.now()).seconds > 0
    )

#Asks Credentials
def ask_credential():
    return [
        inquirer.Text('username',
        message="Username"
        ),
        inquirer.Password('password',
        message="Password"
        )
    ]

def ask_headless():
    return inquirer.List('headless',
    message="Open Browser or not",
    choices=['Yes, Open browser', 'No, Work Silently']
    ),

def ask_confirmation():
    return inquirer.confirm(
    message="Correct?"
    )
