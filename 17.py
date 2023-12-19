from dataclasses import  dataclass
from queue import PriorityQueue

def dbg(*msg):
  if debug:
    print(*msg)
    
@dataclass
class Point:
  x: int
  y: int
  
  def __hash__(self):
    return hash((self.x, self.y))

@dataclass
class Path:
  score: float
  e: Point
  c: int
  slen: int
  sdir: int
  
  def __lt__(self, o):
    return self.score < o.score

@dataclass
class Field:
  avg: float
  w: int
  h: int
  t: dict[Point, int]
  finish: Point
  
  @classmethod
  def parse(cls, i):
    t = {}
    total = 0
    lines = i.strip().split('\n')
    for y, l in enumerate(lines):
      for x, c in enumerate(l):
        t[Point(x,y)] = int(c)
        total += int(c)
    w = len(lines[0])
    h = len(lines)
    a = total / (w*h)
    f = Point(w-1, h-1)
    return cls(a,w,h,t,f)
    
  def move(self, p, d):
    nx = p.x + (d-2 if d%2 == 1 else 0)
    ny = p.y + (d-1 if d%2 == 0 else 0)
    if nx < 0 or ny < 0 or nx >= self.w or ny >= self.h:
      return None
    return Point(nx, ny)

def dirs(slen, sdir, part2):
  r = []
  #dbg(slen, sdir, part2)
  for d in range(4):
    if sdir == (d+2)%4:
      continue # no backsies
    if not part2 and d == sdir and slen == 3:
      continue
    elif part2 and d != sdir and slen < 4 and slen > 0:
      continue
    elif part2 and d == sdir and slen == 10:
      continue
    r.append(d)
  #dbg(r)
  return r
      
def solve(i, part2=False):
  f = Field.parse(i)
  q = PriorityQueue()
  dst = {}
  pd = (f.w + f.h) * f.avg # predicted cost to get to finish
  p = Path(pd, Point(0,0), 0, 0, -1)
  best = 9 * f.w * f.h
  q.put_nowait(p)
  while not q.empty():
    p = q.get_nowait()
    dbg(p)
    if p.e == f.finish:
      if not part2 or p.slen > 4:
        best = min(best, p.c)
      continue
    for d in dirs(p.slen, p.sdir, part2):
      nsdir = d
      nslen = p.slen +1 if d==p.sdir else 1
      np = f.move(p.e, d)
      if np is None:
        continue
      nc = p.c + f.t[np]
      pd = (f.w - np.x + f.h - np.y) * f.avg
      sc = nc + pd
      idx = (np.x, np.y, nslen, nsdir)
      if idx in dst and dst[idx] <= sc:
        continue
      else:
        dst[idx] = sc
      np = Path(sc, np, nc, nslen, nsdir)
      q.put_nowait(np)
      
    
  return best

def solve2(i):
  return solve(i, True)
  
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
tid = 17

test(solve, 102)
test(solve2, 94)

debug = False

do(solve)
do(solve2)
