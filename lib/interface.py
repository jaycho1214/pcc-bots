import time
import sys
import os
import threading
import inquirer
import signal

class interface:
    def __init__(self, questions):
        signal.signal(signal.SIGINT, self.isexit)
        if "Search" in questions['function']:
            from data.questions import ask_crn
            crn = [c.strip() for c in ask_crn().split()]
            self.search(questions['semester'], questions['year'], crns=crn)

        elif "Waiting" in questions['function']:
            from data.questions import ask_crn, ask_crn_with_option
            crn = [c.strip() for c in ask_crn().split()]
            crn_with_option = inquirer.prompt(ask_crn_with_option(crn))
            self.waiting(
                questions['semester'], 
                questions['year'], 
                crns=crn,
                alarm=[crn_with_option['alarm' + str(i)] for i in range(len(crn))],
                rate=crn_with_option['rate']
                )

        elif "Save" in questions['function']:
            from data.questions import ask_filename
            filename = ask_filename()
            self.save(questions['semester'], questions['year'], filename)

        elif "Register" in questions['function']:
            from data.questions import ask_crn, ask_confirmation, ask_credential, ask_time, ask_headless
            crn = [c.strip() for c in ask_crn().split()]
            self.search(questions['semester'], questions['year'], crns=crn)
            confirmation = ask_confirmation()
            if(confirmation == False):
                print("Please start over if you put wrong crn")
                sys.exit(0)
            headless = ask_headless()
            credential = inquirer.prompt(ask_credential())
            time_ = ask_time()
            self.register(questions['semester'], questions['year'], crn, "No" in headless, time_, credential['username'], credential['password'])


    def printresult(self, year, semester, crns):
        from lib.searchbot import searchbot
        bot = searchbot(year=year, term=semester)
        seats = []
        result = ""
        for crn in crns:
            bot.getTable(crn)
            class_ = bot.getClass()
            seat = bot.getSeats()
            prof = bot.getProf()
            result += f"Class: {class_}\tProfessor: {prof}\tSeats: {seat}\n"
            seats.append(seat)
        return seats, result

    def notifychange(self, last_seats, options):
        if 'Open' in options and not int(last_seats) == 0 and not int(last_seats) == -1:
            print('\a' * 3)
            return None

        elif 'Close' in options and int(last_seats) == 0:
            print('\a' * 3)
            return None

        if 'Change' in options and not int(last_seats) == -1:
            def now(seats):
                if not int(last_seats) == int(seats):
                    print('\a' * 3)
                return self.notifychange(int(seats), options)
            return now

    def search(self, semester, year, crns):
        from lib.animation import load_animation
        animation = load_animation("Fetching requested classes information", clear_at_end=False)
        animation.start()
        _, result = self.printresult(year, semester, crns) 
        animation.end = True
        time.sleep(1)
        print(result)
        return result

    def isexit(self, signum, frame):
        from lib.animation import load_animation
        x = load_animation("Quitting", clear_at_end=False)
        x.start()
        for t in threading.enumerate():
            t.end = True
        sys.exit(0)

    def waiting(self, semester, year, crns, alarm, rate):
        from lib.animation import load_animation, countdown
        from lib.searchbot import searchbot
        bot = searchbot(init=False)
        bot.setData(year=year, term=semester)
        changes = [self.notifychange(-1, alarm_) for alarm_ in alarm]
        while True:
            t_ = int(rate) * 60
            result = ""
            print("Press Ctrl-C to quit")
            animation = load_animation("Fetching requested classes information", clear_at_end=False)
            timer = countdown(t_)
            animation.start()
            seats, result = self.printresult(year, semester, crns)
            for seat, change, option in zip(seats, changes, alarm):
                if change is not None:
                    change = change(int(seat))
                else:
                    change = self.notifychange(seat, option)
            animation.end = True
            time.sleep(1)
            print(result)
            timer.start()
            while(t_):
                time.sleep(1)
                t_ -= 1
        
    def save(self, semester, year, file_name):
        from lib.animation import load_animation
        from lib.searchbot import searchbot
        self.animation = load_animation("Fetching html file", clear_at_end=False)
        self.animation.start()
        loc = searchbot(year=year, term=semester).saveHtml(file_name=file_name)    
        self.animation.end = True
        time.sleep(1)
        result = "Successfully Saved to " + loc
        print(result)
        return result

    def register(self, semester, year, crns, headless, time_, username, password):
        from lib.searchbot import searchbot
        from lib.registerbot import registerbot
        from lib.animation import countdown
        from data.questions import ask_credential
        from datetime import datetime
        bot1 = registerbot(headless=headless)
        bot1.logging_in(username, password)
        while not bot1.logged_in():
            print("Login Failed")
            print("Please Try Again")
            credential = inquirer.prompt(ask_credential()) 
            username = credential['username']
            password = credential['password']
            bot1.logging_in(username, password)
        bot1.select_term(semester + ' ' + year)

        timediff = lambda: (datetime(datetime.now().year,datetime.now().month, datetime.now().day,
        int(time_.split(':')[0]), int(time_.split(':')[1]), int(time_.split(':')[2], 0)) - \
            datetime.now()).total_seconds
        t = timediff()
        print('Everything is set!')
        print("Don\'t turn off the program and chrome, but you can hide it if you want")
        print('You can use computer, program will automatically register your classes')
        print('The clock refreshes every 20 miliseconds')
        print('Good luck!')
        while t > 0.0: 
            mins, secs = divmod(t, 60) 
            hrs, mins = divmod(mins, 60)
            timer = '{:02d}:{:02d}:{:02d}'.format(hrs, mins, secs) 
            print(timer, end="\r") 
            time.sleep(0.02)  
            t = timediff()
        time.sleep(0.5) #To prevent Early Registering!
        bot1.crn_writer(crns)
        print("Done")
        input("Press Enter to Finish it")


