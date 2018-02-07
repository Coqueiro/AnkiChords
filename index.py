import sys
from tools import convert_music

for title in sys.argv[1:]:
    convert_music(title)
