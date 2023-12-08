def dbg(*msg):
  if debug:
    print(*msg)


def solve(i):
  return 0

def solve2(i):
  return 0
  
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
tid = 2
 
test(solve, 8)
test(solve2, 2286)

debug = False

do(solve)
do(solve2)
