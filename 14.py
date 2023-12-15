from dataclasses import dataclass
from copy import copy

def dbg(*msg):
  if debug:
    print(*msg)

stone_ids = {'.':0, '#': 1, 'O':2}
stone_syms = {v:k for k,v in stone_ids.items()}

@dataclass
class Stone:
  type: int
  x: int
  y: int
  
@dataclass
class Row:
  stones: list[Stone]
  length: int
  
  def paint(self):
    sid = 0
    result = ''
    for i in range(self.length):
      if sid < len(self.stones) and self.stones[sid].x == i:
        result += stone_syms[self.stones[sid].type]
        sid += 1
      else:
        result += '.'
    return result
  
  def fall(self):
    g = -1
    for s in self.stones:
      if s.type == 1:
        g = s.x
      else:
        g += 1
        s.x = g
    
  def weight(self):
    result = sum([self.length -s.x for s in self.stones if s.type == 2])
    return result
        
@dataclass
class Plate:
  rows: list[Row]
  height: int
  width: int
  
  def paint(self):
    result = ''
    for r in self.rows:
      result += r.paint() + '\n'
    return result
  
  def rotate(self, ccw=True):
    height = self.width
    width = self.height
    dbg
    rows = [Row([], width) for _ in range(height)]
    for r in self.rows:
      for s in r.stones:
        ns = copy(s)
        if ccw:
          ns.x = s.y 
          ns.y = height - s.x -1
          rows[ns.y].stones.append( ns)
        else:
          ns.x = width - s.y -1
          ns.y = s.x
          rows[ns.y].stones.insert(0, ns)
    return Plate(rows, height, width)
  
  def weight(self):
    result = sum([r.weight() for r in self.rows])
    return result
    
  @classmethod
  def parse(cls, i, v2):
    rows = []
    lines = i.strip().split('\n')
    rlen = len(lines[0])
    for y, l in enumerate(lines): 
      stones = []
      for x,c in enumerate(l):
        if c == '.':
          continue
        stones.append(Stone(stone_ids[c],x,y))
      rows.append(Row(stones, rlen))
    return Plate(rows, len(lines), rlen)
  
  def fall(self):
    for r in self.rows:
      r.fall()
      
def solve(i):
  p = Plate.parse(i, False)
  dbg(p.paint())
  p = p.rotate(True)
  dbg(p.paint())
  p.fall()
  wt = p.weight()
  p = p.rotate(False)
  dbg(p.paint())
  return wt

def solve2(i):
  return 0
  
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
tid = 14
 
test(solve, 136)
test(solve2, 2286)

debug = False

do(solve)
do(solve2)
