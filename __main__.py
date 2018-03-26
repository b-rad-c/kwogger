import argparse
from Kwogger.core import Menu

parser = argparse.ArgumentParser(description='Kwogger interactive utility.')
parser.add_argument('path', help='log path to tail')
args = parser.parse_args()

menu = Menu(args.path)

try:
    menu.cmdloop()
except KeyboardInterrupt:
    pass

print('Exiting Kwogger...')
