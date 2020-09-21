import threading
import sys
import time

# geeksforgeeks

clear = lambda: print("\033[H\033[J")

class countdown(threading.Thread):
    def __init__(self, t):
        threading.Thread.__init__(self)
        self.t = t
        self.end = False

    def run(self):
        t = self.t
        while t and not self.end: 
            mins, secs = divmod(t, 60) 
            hrs, min = divmod(mins, 60)
            timer = '{:02d}:{:02d}:{:02d}'.format(hrs, mins, secs) 
            print(timer, end="\r") 
            time.sleep(1) 
            t -= 1
        self.end = True

class load_animation(threading.Thread):
    def __init__(self, text, clear_at_end=True, end_text="Done"):
        threading.Thread.__init__(self)
        self.text = text
        self.clear_at_end = clear_at_end
        self.end_text = end_text
        self.end = False
    
    def run(self):
        load_str = self.text
        ls_len = len(load_str) 

        animation = "|/-\\"
        anicount = 0
        i = 0                     
        while (not self.end): 
            time.sleep(0.075)  
            load_str_list = list(load_str)  
            x = ord(load_str_list[i]) 
            y = 0                             
            if x != 32 and x != 46:              
                if x>90: 
                    y = x-32
                else: 
                    y = x + 32
                load_str_list[i]= chr(y) 
            res =''              
            for j in range(ls_len): 
                res = res + load_str_list[j] 
            sys.stdout.write("\r"+res + animation[anicount]) 
            sys.stdout.flush() 
            load_str = res 
            anicount = (anicount + 1)% 4
            i =(i + 1)% ls_len 
        sys.stdout.write("\n" + self.end_text + "\n")
        sys.stdout.flush()
        if self.clear_at_end:
            clear()
