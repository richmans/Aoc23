from functools import reduce
from dataclasses import dataclass

@dataclass
class Lens:
  label: str
  focal: int
  
  def __eq__(self, o):
    return o.label == self.label
    
def dbg(*msg):
  if debug:
    print(*msg)

def hash(s):
  r= reduce(lambda a,b: (a+ord(b))*17%256, s,0)
  return r
  
def solve(i):
  ins = i.strip().split(',')
  return sum([hash(x) for x in ins])

def solve2(i):
  b = [list() for _ in range(256)]
  for ins in i.strip().split(','):
    dbg(ins)
    if ins.endswith('-'):
      l = ins[:-1]
      lens = Lens(l,0)
      bi = hash(l)
      if lens in b[bi]:
        b[bi].remove(lens)
    else:
     l, f = ins.split('=')
     lens = Lens(l,int(f))
     bi = hash(l)
     if lens in b[bi]:
       lx = b[bi].index(lens)
       b[bi][lx].focal = int(f)
     else:
       b[bi].append(lens)
  dbg(b)
  result = 0
  for bi, bx in enumerate(b):
    for li, l in enumerate(bx):
      fp = (bi+1)*(li+1)*l.focal
      dbg(l.label, fp)
      result += fp
  return result
   
def test(fn, ex, f=None):
  if f is None:
    f = f"input/{tid:02}.test.txt"
  i = open(f).read()
  o = fn(i)
  if o != ex:
    print(f"ERROR: expect {ex} got {o}")
  else:
    print(f"test {fn.__name__} ok")

def do(fn):
  i = open(f"input/{tid:02}.txt").read()
  o = fn(i)
  print(fn.__name__, o)
 
debug = True
tid = 15
 
print(hash('HASH'))
test(solve, 1320)
test(solve2, 145)

debug = False

do(solve)
do(solve2)
