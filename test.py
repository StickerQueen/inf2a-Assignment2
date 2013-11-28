from agreement import *

lx = Lexicon()
lx.add('John','P')
lx.add('dog', 'N')
lx.add('like','T')
lx.add('fox','N')
lx.add('blue','A')
lx.add('say','T')

be = Tree('BE',['BEs'])

breakIt = Tree('S',[Tree('Nom',[Tree('AN',[Tree('N',['Ns'])])]), Tree('QP',[Tree('VP',[Tree('T',['Tp'])])])])
work = all_parses(['Who','does','John','like','?'],lx)[0]
work2 = Tree('VP', [Tree('VP',[Tree('T',['Tp'])]),Tree('AND',['AND']),Tree('VP',[Tree('T',['Tp'])])])
work3 = Tree('NP',[Tree('AN',[Tree('N',['Ns'])])])
breakIt2 = all_parses(['Who','does','dogs','like','?'],lx)[0][1]
tr0 = all_valid_parses(['Who','likes','foxes','?'],lx)[0]
tr = restore_words(tr0, ['Who','likes','foxes','?'])
tr.draw()
