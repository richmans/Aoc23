from dataclasses import dataclass
from copy import copy 
import sys

log = open('output/their.txt','r')
class LineReader:
  def __init__(self, s):
    self.lines = s.split('\n')
    self.num = len(self.lines)
    self.idx = 0
  
  def eof(self):
    return self.idx >= self.num
  
  def get(self):
    if self.idx >= self.num:
      return None
    self.idx += 1
    return self.lines[self.idx - 1]
    
def f2i(l):
  return [ sum([1<<i if c == '#' else 0 for i,c in enumerate(x)]) for x in l]
  
@dataclass
class Field:
  rows: list[str]
  cols: list[str]
  r: list[int]
  c: list[int]
  
  @classmethod
  def parse(cls, r, p2):
    l = r.get()
    rows = []
    cols = []
    while l != '':
      rows.append(l)
      l = r.get()
    for i in range(len(rows[0])):
      cols.append(''.join([rows[j][i] for j in range(len(rows))]))
    return Field(rows, cols, f2i(rows), f2i(cols))

@dataclass
class Mirror:
  offset: int
  smudges: int
  
  def __hash__(self):
    return hash(self.offset)
  
def find(l, allowed_smudges=0):
  dbg('== find')
  ms = set()
  for i in range(1, len(l)):
    c = l[i]
    for m in copy(ms):
      o = m.offset
      x = o - (i-o) + 1
      if x < 0:
        if m.smudges == allowed_smudges:
          return o + 1
        else:
          ms.remove(m)
          continue
      # python3.10+
      smudges = int.bit_count(c ^ l[x])
      # dbg('adding smudges', smudges)
      m.smudges += smudges 
      if m.smudges > allowed_smudges:
        dbg('drop', m, i, x)
        ms.remove(m)

    smudges = int.bit_count(c ^ l[i-1])
    if smudges <= allowed_smudges:
      dbg('add',i-1, smudges)
      ms.add(Mirror(i-1, smudges))
  cands = [m for m in ms if m.smudges == allowed_smudges]
  
  if len(cands) == 0:
    return 0
  if len(cands) > 1:
    print('multiple cands!')
  return cands[0].offset +1
  
def dbg(*msg):
  if debug:
    print(*msg)

def parse(i, p2):
  r = LineReader(i)
  pats = []
  while not r.eof():
    pats.append(Field.parse(r, p2))
  return pats

def check_result(p, vert, num):
  x = log.readline().strip()
  parts = x.split()
  evert = parts[0] == 'c'
  enum = int(parts[1])
  if evert != vert or enum != num:
    print(f'mismatch ex: {evert} {enum}, found {vert} {num }', p)
    print('\n'.join(p.rows))
  
def solve(i, smudges=0):
  pats = parse(i, False)
  dbg(pats)
  result = 0
  for p in pats:
    m = find(p.c, smudges)
    if m > 0:
      dbg('vertical mirror at', m)
      #check_result(p, True, m)
    else:
      mr = find(p.r, smudges) 
      #  dbg('horizontal mirror at', mr)
      #check_result(p, False,mr)
      if mr == 0:
        print('err: no mirror')
        print('\n'.join(p.rows))
      m = mr * 100
    result += m
  return result

def solve2(i):
  return solve(i, 1)
  
def test(fn, ex, f=None):
  if f is None:
    f = f"input/{tid:02}.test.txt"
  i = open(f).read()
  o = fn(i)
  if o != ex:
    print(f"ERROR: expect {ex} got {o}")
    sys.exit(1)
  else:
    print(f"test {fn.__name__} ok")

def do(fn):
  i = open(f"input/{tid:02}.txt").read()
  o = fn(i)
  print(fn.__name__, o)
 
debug = True
tid = 13
 
test(solve, 405)
test(solve, 100, 'input/13.test2.txt')
test(solve2, 1400, 'input/13.test3.txt')
test(solve2, 400)

debug = False

do(solve)
do(solve2)

