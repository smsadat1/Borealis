import sys
from auth import login
from runner import runner

def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: borealis <command>")
        return

    cmd = args[0]

    if cmd == "auth":
        if len(args) > 1 and args[1] == "login":
            login()
        else:
            print("Usage: borealis auth login")

    elif cmd == "runner":
        runner()

    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()