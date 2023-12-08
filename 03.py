from dataclasses import dataclass

@dataclass
class Number:
  num: int
  size: int
  x: int
  y: int

  def edges(self):
    return [(self.x-1, self.y), (self.x+self.size, self.y)] + \
      [(x,self.y-1) for x in range(self.x-1, self.x+self.size+1)] + \
      [(x,self.y+1) for x in range(self.x-1, self.x+self.size+1)] 

@dataclass
class Symbol:
  sym: str
  x: int
  y: int

def parse(i):
  digits = '1234567890'
  numbers = []
  symbols = {}
  x = 0
  y = 0
  for l in i.strip().split('\n'):
    x=0
    num = None
    for c in l:
      if c in digits:
        if num is not None:
          num.size += 1
          num.num = num.num * 10 + int(c)  
        else:
          num = Number(int(c), 1, x, y)
          numbers.append(num)
      else:
          num = None
          if c != '.':
            symbols[(x,y)] = Symbol(c, x, y)
      x += 1
    y += 1
  return numbers, symbols

def dbg(*msg):
  if debug:
    print(*msg)

def solve(i):
  numbers, symbols = parse(i)
  sum = 0
  dbg(symbols)
  for num in numbers:
    dbg(f"== {num} ==")
    for e in num.edges():
      dbg("Edge:", e)
      if e in symbols:
        dbg("HIT")
        sum += num.num
  return sum

def solve2(i):
  sum = 0
  numbers, symbols = parse(i)
  gears = [s for s in symbols.values() if s.sym == '*']
  for g in gears:
    touching = [n for n in numbers if (g.x, g.y) in n.edges()]
    if len(touching) == 2:
      sum += touching[0].num * touching[1].num
  return sum
  
def test(fn, ex):
  f = f"input/{tid:02}.test.txt"
  i = open(f).read()
  o = fn(i)
  if o != ex:
    print(f"ERROR: expect {ex} got {o}")
  else:
    print("test ok")

def do(fn):
  i = open(f"input/{tid:02}.txt").read()
  o = fn(i)
  print(fn.__name__, o)

debug = False 
tid = 3
 
test(solve, 4361)
test(solve2, 467835)
do(solve)
do(solve2)
