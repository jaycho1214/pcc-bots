import inquirer
from data.questions import ask_basic
from lib.interface import interface

def main():
    clear = lambda: print("\033[H\033[J")
    clear()
    questions = inquirer.prompt(ask_basic())   
    bots = interface(questions)


if __name__ == "__main__":
    main()
    print("Thank you for using our program!")


