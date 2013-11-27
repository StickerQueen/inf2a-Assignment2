from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?


# Tags for words playing a special role in the grammar:

tagged_function_words = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in tagged_function_words]

# English nouns with identical plural forms (list courtesy of Wikipedia):

identical_plurals = ['bison','buffalo','deer','fish','moose','pike','plankton',
     'salmon','sheep','swine','trout']


def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    if s in identical_plurals:
      return s
    if s[-3:] == 'men':
      s = s[:-3]+'man'
    else:
      s = verb_stem(s)
    return s
 
def tag_word (wd,lx):
    """returns a list of all possible tags for wd relative to lx"""

def tag_words (wds,lx):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (wds[0],lx)
        tag_rest = tag_words (wds[1:],lx)
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

