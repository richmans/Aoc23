from dataclasses import dataclass

def dbg(*msg):
  if debug:
    print(*msg)

def get_inside(x, insides):
  for i in insides:
    if x >= i[0] and x <= i[1]:
      return i
  return None

def consolidate(insides):
  insides = sorted(insides)
  i = 0
  r = []
  while i < len(insides):
    x = insides[i]
    i += 1
    while i < len(insides) and x[1] == insides[i][0] -1:
      i += 1
      x[1] = insides[i][1]
    r.append(x)
  return r

class Grid:
  def __init__(self):
    # in the beginning, there was darkness
    self.h = {}
    self.tops = set()
    self.cur = Point(0,0)
    self.top = Point(0,0)
    self.bottom = Point(0,0)
    
  def draw(self, ins):
    p = self.cur
    np = p.dig(ins)
    if p.y == np.y:
      start = min(p.x, np.x)
      stop = max(p.x, np.x)
      if p.y not in self.h:
        self.h[p.y] = []
      self.h[p.y].append((start, stop))
    if p.x == np.x:
      top = Point(p.x, min(p.y, np.y))
      self.tops[top] = True
    self.top = self.top.min(np)
    self.bottom = self.bottom.max(np)
    self.cur = np
  
  def measure(self):
    cnt = 0
    last = 0
    insides = []
    levels = sorted(self.h.keys())
    for y in levels:
      drop = y - last
      cnt += sum([(b-a+1)* drop for a,b in insides])
      for l in self.h[y]:
        i = get_inside(l, insides):
        if i != None
          bef = (i[0], l[0])
          aft = (l[1], i[1])
          insides.remove(i)
          insides.append(bef)
          insides.append(aft)
        else:
          cnt += l[1] - l[0] -1
          insides.append(l)
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
  dbg(g.h)
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
