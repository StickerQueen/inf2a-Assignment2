class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
      self.cat_dict = {'P':[], 'N':[], 'A':[], 'I':[], 'T':[]}

    def add(self, stem, cat):
      """adds the given stem to the dictionary entry
        for a category"""
      if cat in self.cat_dict.keys():
        if not stem in self.cat_dict[cat]:  self.cat_dict[cat].append(stem)
      else:
        return 'Error: not a valid tag'
    
    def getAll(self, cat):
      """returns all stems with a given category"""
      return self.cat_dict[cat]

class FactBase:
    """stores unary and binary relational facts"""
    def __init__(self):
      self.binaries = {}
      self.unaries = {}

    def addUnary(self, pred, e1):
      """adds a unary predicate to a list and stores the subject"""
      if not pred in self.unaries.keys():
        self.unaries[pred] = []
      self.unaries[pred].append(e1)

    def queryUnary(self, pred, e1):
      """returns whether or not a fact has been stored"""
      if not pred in self.unaries.keys():
        return False
      if e1 in self.unaries[pred]:
        return True
      return False
   
    def addBinary(self, pred, e1, e2):
      """adds a binary predicate to a list and stores the subjects"""
      if not pred in self.binaries.keys():
        self.binaries[pred] = []
      self.binaries[pred].append((e1,e2))

    def queryBinary(self, pred, e1, e2):
      """returns whether or not a fact has been stored"""
      if not pred in self.binaries.keys():
        return False
      if (e1,e2) in self.binaries[pred]:
        return True

import re

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    if re.match('.*s', s):
      if re.match('(unt|.)ies', s):
        s = s[:-1]
      elif re.match('.*ies', s):
        s = s[:-3]+'y'
      elif re.match('.*es', s):
        if re.match('.*([ox]|ch|sh|ss|zz)es', s):
          s = s[:-2]
        elif re.match('.*[zs]es',s):
          s = s[:-1]
        elif re.match('.*[^i]es',s):
          s = s[:-1]
      else:
        s = s[:-1]
      if s == 'has':
        s = 'have'
    return s

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement (wlist,lx,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
