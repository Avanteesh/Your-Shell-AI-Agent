import sys
from agent import ShellAgent
from colorama import Fore

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Command missing!")
        print("Use --help!")
    elif sys.argv[1] == "--help":
        print("Commands: ")
        print("\t--chat, opens live chat mode ('exit' command to terminate)")
        print("\t--prompt 'prompt-text'")
        print("\t--help (documentation)")
    elif sys.argv[1] == "--chat":
        user_input = input(f"{Fore.YELLOW}Human{Fore.WHITE}: ")
        while user_input != "exit":
            inputs = {"messages": [("user", user_input)]}
            try:
                result = ShellAgent.invoke(inputs)
                print(f"{Fore.GREEN}AI{Fore.WHITE}: ",result['messages'][-1].content)
            except Exception as e:
                print(e)
            user_input = input(f"{Fore.YELLOW}Human{Fore.WHITE}: ")
    elif sys.argv[1] == "--prompt":
        if len(sys.argv) < 3:
            print(f"{Fore.RED}ERROR{Fore.WHITE}: prompt missing!")
        else:
            inputs = {"messages": [("user", sys.argv[2])]}
            result = ShellAgent.invoke(inputs)
            print(f"{Fore.GREEN}AI{Fore.WHITE}: ", result['messages'][-1].content)
        


