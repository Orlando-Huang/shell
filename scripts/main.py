import os
import sys
import glob
import shlex
import shutil
import socket
import subprocess

HOME = os.path.expanduser('~')
returnError = lambda text: print(f"\033[91m{text}\033[0m")
print("""
██████╗░░█████╗░░██╗░░░░░░░██╗███████╗██████╗░██████╗░░█████╗░░██████╗██╗░░██╗
██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██║░░██║
██████╔╝██║░░██║░╚██╗████╗██╔╝█████╗░░██████╔╝██████╦╝███████║╚█████╗░███████║
██╔═══╝░██║░░██║░░████╔═████║░██╔══╝░░██╔══██╗██╔══██╗██╔══██║░╚═══██╗██╔══██║
██║░░░░░╚█████╔╝░░╚██╔╝░╚██╔╝░███████╗██║░░██║██████╦╝██║░░██║██████╔╝██║░░██║
╚═╝░░░░░░╚════╝░░░░╚═╝░░░╚═╝░░╚══════╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝
""".strip())
os.chdir(HOME)

while True:
    try:
        print('\n'+os.getcwd())
        tokens = shlex.split(input(">>> "))
        if not tokens: continue
        command, *args = tokens
        match command:
            case "echo":
                print(' '.join(args))
            case "cls" | "clear":
                match len(args):
                    case 0: os.system('cls' if os.name == 'nt' else 'clear')
                    case _: returnError("Too many arguments! Expected None.")
            case "pwd":
                match len(args):
                    case 0: print(os.getcwd()))
                    case _: returnError("Too many arguments! Expected None.")
            case "hostname":
                match len(args):
                    case 0: print(socket.gethostname())
                    case _: returnError("Too many arguments! Expected None.") 
            case "hostip":
                match len(args):
                    case 0: print(socket.gethostbyname(socket.gethostname()))
                    case _: returnError("Too many arguments! Expected None.")
            case "exit":
                match len(args):
                    case 0: sys.exit()
                    case 1: sys.exit(args[0])
                    case _: returnError("Too many arguments! Expected 1 or less.") 
            case "cd":
                match len(args):
                    case 0: os.chdir(HOME)
                    case 1: os.chdir(args[0])
                    case _: returnError("Too many arguments! Expected 1 or less.")
            case "ls":
                match len(args):
                    case 0: path = os.getcwd()
                    case 1:
                        if os.path.exists(args[0]):
                            path = args[0]
                        else:
                            returnError(f"ERROR: Path not found: '{args[0]}")
                            continue
                    case _: returnError("Too many arguments! Expected 1 or less.")
                if not path.endswith(os.sep): path += os.sep
                items = glob.glob(f'{path}*')
                items.sort(key = lambda item: not os.path.isdir(item))
                print('\n'.join([f"{item[len(path):]}/" if os.path.isdir(item) else item[len(path):] for item in items]))
            case "cp" | "copy":
                match len(args):
                    case 0:
                        src = input("Source: ")
                        dst = input("Destination: ")
                    case 1:
                        src = args[0]
                        dst = input("Destination: ")
                    case 2: src, dst = args
                    case _: returnError("Too many arguments! Expected 2 or less.")
                shutil.copy(src, dst) if os.path.isfile(src) else shutil.copytree(src, dst)
            case "mv" | "move":
                match len(args):
                    case 0:
                        src = input("Source: ")
                        dst = input("Destination: ")
                    case 1:
                        src = args[0]
                        dst = input("Destination: ")
                    case 2:
                        src, dst = args
                    case _:
                        returnError("Too many arguments! Expected 2 or less.")
                shutil.move(src, dst)
            case _:
                if shutil.which(command):
                    os.system(f"{command} {' '.join(args)}")
                else:
                    returnError(f"ERROR: {command} is not recognised as a command or executable!")
    except (KeyboardInterrupt, EOFError):
        print("Use 'exit' to exit")
        continue
    except Exception as e:
        returnError(f"ERROR: {e}")
