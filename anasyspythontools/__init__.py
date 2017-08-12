from . import anasysfile
from . import anasysdoc
from . import heightmap
from . import irspectra
from . import anasysio

def read(fn):
    doc = anasysio.AnasysFileReader(fn).doc
    return anasysdoc.AnasysDoc(doc)
