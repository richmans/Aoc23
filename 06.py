def dbg(*msg):
  if debug:
    print(*msg)

def parse(i):
  lines = i.split('\n')
  times = [int(i) for i in lines[0].split()[1:]]
  records = [int(i) for i in lines[1].split()[1:]]
  dbg(times, records)
  return times, records
  
def calc(t, record):
  wins = 0
  for c in range(t):
    dist = c * (t-c)
    wins += 1 if dist > record else 0
  return wins
  
def solve(i):
  times, records = parse(i)
  result = 1
  for n in range(len(times)):
    result *= calc(times[n], records[n])
  return result

def solve2(i):
  times, records = parse(i)
  tim = int(''.join([str(n) for n in times]))
  rec = int(''.join([str(n) for n in records]))
  dbg(tim, rec)
  return calc(tim, rec)
  
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
tid = 6
 
test(solve, 288)
test(solve2, 71503)

debug = False

do(solve)
do(solve2)
