from dataclasses import dataclass
from itertools import combinations
from copy import copy

def dbg(*msg):
  if debug:
    print(*msg)

@dataclass
class Row:
  springs: int
  groups: list[int]
  
  @classmethod
  def parse(cls, l, p2):
    springs, groups = l.split()
    if p2:
      springs = '?'.join([springs]*5)
      groups = ','.join([groups]*5)
    groups = [int(x) for x in groups.split(',')]
    return Row(springs, groups)  

def walk(s, g, curg=None):
  if s == '':
    done = len(g) == 0 and curg in [None,0]
    return done
  #dbg(s,g,curg)
  c = s[0]
  x = s[1:]
  g = copy(g)
  if c == '.':
    if curg == 0:
      curg = None
    return walk(x, g, None) if curg is None else 0
  elif c == '#':
    if curg == 0:
      return 0
    if curg is None:
      if len(g) == 0:
        return 0
      curg = g.pop(0)
    return walk(x, g, curg-1)
  else:
    return walk('.'+x, g, curg) + walk('#'+x, g, curg)
  
  
  
def parse(i, p2):
  rows = []
  for l in i.strip().split('\n'):
    rows.append(Row.parse(l, p2))
  return rows
  
def solve(i):
  rows = parse(i, False)
  dbg(rows)
  result = 0
  for r in rows:
    a = walk(r.springs, r.groups)
    dbg('RESULT', a)
    result += a
  return result

def solve2(i):
  rows = parse(i, True)
  result = 0
  for r in rows:
    a = walk(r.springs, r.groups)
    dbg('RESULT', a)
    result += a
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
tid = 12
 
test(solve, 21)
test(solve2, 525152)

debug = False

do(solve)
do(solve2)
