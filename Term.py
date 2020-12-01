import tty, sys, termios
from Vec import Vec

class Term:
    def clear(self):
        print(f"\033[2J", end="", flush=False)

    def move_cursor(self, coords):
        print(f"\033[{coords[1]+1};{coords[0]+1}H", end="", flush=False)

    def write_here(self, coords: Vec, string):
        old = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        for i, line in enumerate(string.splitlines()):
            if line != "":
                self.move_cursor(coords + (0,i))
                print(line,end="", flush=False)
        termios.tcsetattr(sys.stdin, termios.TCSANOW, old)

    def draw_rectangle(self, pos: Vec, size: Vec, label=""):
        old = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        self.move_cursor(pos)
        if (size == (0,0)):
            pass
        elif (size.x == 1 and size.y == 1):
            print("X", end="")
        elif (size.y == 1):
            print("<" + "=" * (size.x - 2) + ">",end="", flush=False)
        elif (size.x == 1):
            print("^" ,end="", flush=False)
            print(f"\033[1B", end="", flush=False)
            print(f"\033[1D", end="", flush=False)
            for i in range(size.y-2):
                print("|" ,end="", flush=False)
                print(f"\033[1B", end="", flush=False)
                print(f"\033[1D", end="", flush=False)
            print("V" ,end="", flush=False)
        else:
            print("/" + "-" * (size.x - 2) + "\\" ,end="", flush=False)
            print(f"\033[1B", end="", flush=False)
            print(f"\033[{size.x}D", end="", flush=False)
            for i in range(size.y - 2):
                if i == 0:
                    print("|", end="")
                    print(label, end="")
                    print(" " * (size.x - 2 - len(label)) + "|" ,end="", flush=False)
                else:
                    print("|" + " " * (size.x - 2) + "|" ,end="", flush=False)
                print(f"\033[1B", end="", flush=False)
                print(f"\033[{size.x}D", end="", flush=False)
            print("\\" + "-" * (size.x - 2) + "/" ,end="", flush=False)
        termios.tcsetattr(sys.stdin, termios.TCSANOW, old)
