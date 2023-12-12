from dataclasses import dataclass
from itertools import combinations

def dbg(*msg):
  if debug:
    print(*msg)

@dataclass
class Row:
  springs: int
  groups: list[int]
  wildcards: list[int]
  
  @classmethod
  def parse(cls, l, p2):
    s, groups = l.split()
    if p2:
      s = '?'.join([s]*5)
      groups = ','.join([groups]*5)
    springs = sum([1<<i for i, b in enumerate(s) if b == '#'])
    wildcards = [i for i,b in enumerate(s) if b == '?']
    groups = [int(x) for x in groups.split(',')]
    return Row(springs, groups, wildcards)  

def calc(s):
  result = []
  inside = False
  while s > 0:
    x = s & 1
    s = s >> 1
    if not inside and x == 1:
      result.append(1)
    elif inside and x == 1:
      result[-1] += x
    inside = x == 1
  return result
    
def parse(i, p2):
  rows = []
  for l in i.strip().split('\n'):
    rows.append(Row.parse(l, p2))
  return rows

def num_solutions(r):
  # python 3.10+
  present = int.bit_count(r.springs)
  needed = sum(r.groups)
  ones = needed - present
  base = r.springs
  result = 0
  for i in combinations(r.wildcards, ones):
    c = base | sum([1<<z for z in i])
    result += 1 if calc(c) == r.groups else 0
  return result
  
def solve(i):
  rows = parse(i, False)
  dbg(rows)
  return sum([num_solutions(r) for r in rows])

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
tid = 12
 
test(solve, 21)
test(solve2, 525152)

debug = False

do(solve)
do(solve2)
