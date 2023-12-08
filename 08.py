import math

def dbg(*msg):
  if debug:
    print(*msg)

def parse_node(l):
  p = l.split(' ')
  return p[2][1:-1], p[3][:-1]
  
def parse(i):
  lines = i.strip().split('\n')
  dirx = [0 if c == 'L' else 1 for c in lines.pop(0)]
  lines.pop(0)
  nodes = {l.split(' ')[0]: parse_node(l) for l in lines}
  return dirx, nodes

def search(n, dirx, nodes, fn):
  t = 0
  while not fn(n):
    i = dirx[t % len(dirx)]
    t += 1
    n = nodes[n][i]
  return t


def solve(i):
  dirx, nodes = parse(i)
  dbg(nodes, dirx)
  return search('AAA', dirx, nodes, lambda x: x=='ZZZ')

def solve2(i):
  dirx, nodes = parse(i)
  starters = [x for x in nodes if x.endswith('A')]
  p = []
  for n in starters:
    t = search(n, dirx, nodes, lambda x: x.endswith('Z'))
    p.append(t)
  dbg(p)
  return math.lcm(*p)
  
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
tid = 8
 
test(solve, 2)
test(solve2, 6, f'input/{tid:02}.test2.txt')

debug = False

do(solve)
do(solve2)
