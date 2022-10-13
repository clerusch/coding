import sys
from clemlib.repcoderobj import *
word = Message("meinding")
word.show()
word.encode(3)
word.show()
word.noisify()
word.show()
word.decode()
word.show()