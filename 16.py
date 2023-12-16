from dataclasses import dataclass

TILE_TYPES = '.\/|-'
@dataclass
class Tile:
  type: int
  outports: list[bool]
  active: False
  
  def route(self, d):
    outdirs = [ (d + 2) % 4 ]
    if self.type == 2:
      outdirs = [{1:2,2:1,0:3,3:0}[d]]
    elif self.type == 1:
      outdirs = [{1:0,0:1,3:2,2:3}[d]]
    elif self.type == 3 and d % 2 == 1:
      outdirs = [0,2]
    elif self.type == 4 and d % 2 == 0:
      outdirs = [1,3]
    
    self.active = True
    for outdir in outdirs:
      if self.outports[outdir] == True:
        return [] # stop double beams
      self.outports[outdir] = True
    return outdirs

  @classmethod
  def parse(cls, c):
    typ = TILE_TYPES.index(c)
    return Tile(typ, [False]*4, False)
  
  def reset(self):
    self.outports = [False] * 4
    self.active = False
  
  def __repr__(self):
    return TILE_TYPES[self.type]
    
@dataclass
class Grid:
  t: list[list[Tile]]
  w: int
  h: int
  
  @classmethod
  def parse(cls, i):
    l = i.strip().split('\n')
    w = len(l[0])
    h = len(l)
    t = []
    for y in range(h):
      r = []
      for x in range(w):
        r.append(Tile.parse(l[y][x]))
      t.append(r)
    return Grid(t, w, h)
  
  def paint(self):
    res = ''
    for r in self.t:
      for t in r:
        res += 'X' if t.active else '.'
      res += '\n'
    return res
  
  def active(self):
    return sum([sum([1 if t.active else 0 for t in r]) for r in self.t])
  
  def reset(self):
    [[t.reset() for t in r] for r in self.t]
    
  def __str__(self):
    return '\n'.join([''.join([str(t) for t in r]) for r in self.t])
  
def dbg(*msg):
  if debug:
    print(*msg)

def beam(g, x, y, d):
  q = [(x,y,d)]
  while len(q) > 0:
    x,y,d = q.pop()
    # dbg('b',x, y,d)
    if x < 0 or y < 0 or x >= g.w or y >= g.h:
      continue
    ods = g.t[y][x].route(d)
    #dbg('ods', ods)
    for od in ods:
      nd = ( od + 2 ) % 4
      nx = x + (nd-2 if nd%2 == 1 else 0)
      ny = y - (nd-1 if nd%2 == 0 else 0)
      q.append((nx, ny, nd))

def solve(i):
  g = Grid.parse(i)
  dbg(g)
  beam(g, 0,0,3)
  dbg(g.paint())
  return g.active()

def solve2(i):
  g = Grid.parse(i)
  edges = [(0,i,3) for i in range(g.h)] + \
    [(g.w-1,i,1) for i in range(g.h)] + \
    [(i,0,0) for i in range(g.w)] + \
    [(i,g.h-1, 2) for i in range(g.w)] 
  max_active = 0
  
  for e in edges:
    g.reset()
    beam(g, *e)
    a = g.active()
    dbg('e',e, a)
    max_active = max(max_active, a)
  return max_active
  
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
tid = 16
 
test(solve, 46)
test(solve2, 51)

debug = False

do(solve)
do(solve2)
