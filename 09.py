def dbg(*msg):
  if debug:
    print(*msg)


def parse(i):
  return [[int(x) for x in l.split()] for l in i.strip().split('\n')]

def calc(l):
  d = [l]
  h = l
  while len([x for x in h if x != 0]) > 0:
    h = [h[x] - h[x-1] for x in range(1, len(h))]
    d.append(h)
  return d
  
def solve(i):
  p = []
  for l in parse(i):
    d = calc(l)
    n = sum([h[-1] for h in d])
    dbg(n)
    p.append(n)
  return sum(p)

def solve2(i):
  p = []
  for l in parse(i):
    d = calc(l)
    n = 0
    for h in d[::-1]:
      dbg(h)
      n = h[0] - n
    dbg(n)
    p.append(n)
    
  return sum(p)
  
def test(fn, ex):
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
tid = 9
 
test(solve, 114)
test(solve2, 2)

debug = False

do(solve)
do(solve2)
