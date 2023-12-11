
def dbg(*msg):
  if debug:
    print(*msg)

pipedirs = {
  '|': (0, 2),
  '-': (3,1),
  'L': (0,1),
  'J': (0,3),
  '7': (3,2),
  'F': (1,2)  
}

dirs = {
  0: (0,-1),
  1: (1,0),
  2: (0,1),
  3: (-1,0)
}

def parse(i):
  y=0
  pipes = {}
  start = None
  for l in i.strip().split():
    x=0
    for c in l:
      if c == 'S':
        start = (x,y)
      elif c in pipedirs:
        d1, d2 = pipedirs[c]
        pipes[(x,y,d1)] = d2
        pipes[(x,y,d2)] = d1
      x += 1
    y += 1
  dims = (x,y)
  return dims, start, pipes

def find_entry(pipes, x, y):
  ds = [d for d in range(4) if traverse(x,y,d) in pipes]
  return ds
  
def solve(i):
  _, start, pipes = parse(i)
  dbg(pipes)
  tiles = find_loop(start, pipes)
  return len(tiles) // 2
  
def find_loop(start, pipes):
  x,y = start
  tiles = []
  d = find_entry(pipes, *start)[0]
  while True:
    dbg(x,y,d)
    tiles.append((x,y))
    x,y,d = traverse(x,y,d)
    if (x,y) == start:
      break
    d = pipes[(x,y,d)]
    
  return tiles

def is_inside(x,y,loop,pipes):
  cnt = 0
  for uy in range(y):
    if (x,uy) in loop and (x,uy,1) in pipes:
      cnt += 1
  return cnt % 2 == 1
  
def solve2(i):
  dims, start, pipes = parse(i)
  w,h = dims
  x,y = start
  loop = find_loop(start, pipes)
  ds = find_entry(pipes, *start)
  pipes[(x,y,ds[0])] = ds[1]
  pipes[(x,y,ds[1])] = ds[0]
  cnt = 0
  for y in range(h):
    for x in range(w):
      if (x,y) in loop:
        continue
      if is_inside(x,y,loop,pipes):
        dbg(x,y,'inside')
        cnt += 1
  return cnt
  
def traverse(x,y,d):
  nx = x + dirs[d][0]
  ny = y + dirs[d][1]
  nd = (d + 2) % 4
  dbg(x,y,d,'->',nx,ny,nd)
  return nx,ny,nd
  
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
tid = 10
 
test(solve, 8)
test(solve2, 4, f'input/10.test2.txt')
test(solve2, 10, f'input/10.test3.txt')
debug = False

do(solve)
do(solve2)
