from . import anasysfile
from . import anasysdoc
from . import heightmap
from . import irspectra
from . import anasysio

def read(fn):
    doc = anasysio.AnasysFileReader(fn)._doc
    return anasysdoc.AnasysDoc(doc)
