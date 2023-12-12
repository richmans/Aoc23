from dataclasses import dataclass
from itertools import combinations


@dataclass
class Universe:
  width: int
  height: int
  galaxies: list[tuple[int,int]]
  colstats: list[int]
  rowstats: list[int]

  @staticmethod
  def calc_shift(stats, exp):
    shifts = []
    cnt = 0
    for c in stats:
      shifts.append(cnt)
      if c == 0:
        cnt += exp - 1
    return shifts
    
  def expand(self, exp):
    colshift = Universe.calc_shift(self.colstats, exp)
    rowshift = Universe.calc_shift(self.rowstats, exp)
    galaxies = []
    for x,y in self.galaxies:
      x += colshift[x]
      y += rowshift[y]
      galaxies.append((x, y))
    return galaxies
    
  @classmethod
  def parse(cls, i, newv):
    lines = i.strip().split('\n')
    width = len(lines[0])
    height = len(lines)
    colstats = [0] * width
    rowstats = [0] * height
    galaxies = []
    y = 0
    for l in lines:
      x = 0
      for c in l:
        if c == '#':
          galaxies.append((x,y))
          colstats[x] += 1
          rowstats[y] += 1
        x += 1
      y += 1
    return cls(width, height, galaxies, colstats, rowstats)
    
def dbg(*msg):
  if debug:
    print(*msg)

def solve(exp, i):
  u = Universe.parse(i, False)
  expanded = u.expand(exp)
  dbg(expanded)
  result = 0
  for a,b in combinations(expanded, 2):
    result += max(a[0], b[0]) - min(a[0], b[0]) + max(a[1], b[1]) - min(a[1], b[1])
  return result
  
def test(fn, arg, ex, f=None):
  if f is None:
    f = f"input/{tid:02}.test.txt"
  i = open(f).read()
  o = fn(arg, i)
  if o != ex:
    print(f"ERROR: expect {ex} got {o}")
  else:
    print(f"test {fn.__name__} {arg} ok")

def do(fn, arg):
  i = open(f"input/{tid:02}.txt").read()
  o = fn(arg, i)
  print(fn.__name__, arg, o)
 
debug = True
tid = 11
 
test(solve, 2, 374)
test(solve, 100, 8410)

debug = False

do(solve, 2)
do(solve, 1000000)
