from test import*
from data import*

def machin(texte):
    print(globals())
    print('\n\n')
    print(locals())
    print(value)
    global txt
    txt=text(texte)
    txt.display()
print(globals())
print('\n\n')
print(locals())
print(value)
machin('test')
print('\n\n')
txt.display()
