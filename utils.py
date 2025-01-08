#utils
import re

def findWholeWord(w):
    return re.compile(r'(?:\W|^){0}(?:\W|$)'.format(re.escape(w)), flags=re.IGNORECASE).search
