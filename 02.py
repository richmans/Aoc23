import re

def parse(i):
  r = {}
  for l in i.split('\n'):
    if len(l) == 0:
      continue
    gname, content = l.split(': ')
    gid = int(gname[5:])
    game = [{t.split(' ')[1]: int(t.split(' ')[0]) for t in g.split(', ')} for g in content.split('; ')]
    yield gid, game

def possible(game, max):
  for d in game:
    for c, cnt in d.items():
      if c not in max or cnt > max[c]:
        return False
  return True

def solve(i):
  max = {'red': 12, 'green': 13, 'blue': 14}
  sum = 0
  for gid, g in parse(i):
    if possible(g, max):
      sum += gid
  return sum

def power(game):
  min = {'red': 0, 'green': 0, 'blue': 0}
  for d in game:
    for c, cnt in d.items():
      if c in min and cnt > min[c]:
        min[c] = cnt
  return min['red'] * min['green'] * min['blue']
  
def solve2(i):
  sum = 0
  for gid, g in parse(i):
    sum += power(g)
  return sum
  
def test(fn, f, ex):
  i = open(f).read()
  o = fn(i)
  if o != ex:
    print(f"ERROR: expect {ex} got {o}")
  else:
    print("test ok")

def do(fn):
  i = open("input/02.txt").read()
  o = fn(i)
  print(fn.__name__, o)
  
test(solve, "input/02.test.txt", 8)
test(solve2,"input/02.test.txt", 2286)
do(solve)
do(solve2)
