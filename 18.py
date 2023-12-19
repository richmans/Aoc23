from dataclasses import dataclass

def dbg(*msg):
  if debug:
    print(*msg)

class Grid:
  def __init__(self):
    # in the beginning, there was darkness
    self.t = {Point(0,0): (0,0,0)}
    self.cur = Point(0,0)
    self.top = Point(0,0)
    self.bottom = Point(0,0)
    
    
  def draw(self, ins):
    p = self.cur
    for _ in range(ins.l):
      p = p.move(ins.d)
      self.t[p] = ins.c
    self.top = self.top.min(p)
    self.bottom = self.bottom.max(p)
    self.cur = p
  
  def measure(self):
    cnt = 0
    for y in range(self.top.y, self.bottom.y + 1):
      inside = False
      up = down = False
      for x in range(self.top.x, self.bottom.x + 1):
        p = Point(x,y)
        dug = p in self.t
        if not dug:
          up = down = False
        else:
          up |= Point(x,y-1) in self.t
          down |= Point(x,y+1) in self.t
        if up and down:
          inside = not inside
          up = down = False
        dbg(p, inside)
        if inside or dug:
          cnt += 1
    return cnt
      
@dataclass
class Point:
  x: int
  y: int
  
  def min(self, o):
    return Point(min(self.x, o.x), min(self.y, o.y))
  
  def max(self, o):
    return Point(max(self.x, o.x), max(self.y, o.y))
  
  def __hash__(self):
    return hash((self.x, self.y))
  
  def move(self, d):
    x = self.x + d[0]
    y = self.y + d[1]
    return Point(x,y)
    
  def dig(self, i):
    x = self.x + i.d[0] * i.l
    y = self.y + i.d[1] * i.l
    return Point(x,y)
    
@dataclass
class Instruction:
  d: tuple[int,int]
  l: int
  c: tuple[int, int, int]

def parse(i):
  result = []
  dirs = {'U': (0, -1), 'R': (1,0), 'D': (0,1), 'L': (-1, 0)}
  for l in i.strip().split('\n'):
    d, l, c = l.split()
    d = dirs[d]
    l = int(l)
    c = (int(c[2:4], 16), int(c[4:6], 16), int(c[6:8], 16))
    result.append(Instruction(d, l, c))
  return result

def solve(i):
  i = parse(i)
  dbg(i)
  g = Grid()
  for ins in i:
    g.draw(ins)
  
  return g.measure()

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
tid = 18
 
test(solve, 62)
test(solve2, 2286)

debug = False

do(solve)
#do(solve2)
