import argparse
from Kwogger.core import Menu

parser = argparse.ArgumentParser(description='Kwogger interactive utility.')
parser.add_argument('path', help='log path to tail')
parser.add_argument('--cmd', default='follow', help='Command to be run after initializing')
args = parser.parse_args()

menu = Menu(args.path, args.cmd)

try:
    menu.cmdloop()
except KeyboardInterrupt:
    pass

print('Exiting Kwogger...')
