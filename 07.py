from dataclasses import dataclass
from collections import Counter
def dbg(*msg):
  if debug:
    print(*msg)

@dataclass
class Hand:
  cards: list[int]
  bid: int
  score: int
  
  @classmethod
  def parse(cls, i, newv):
    parts = i.split()
    cards = list(parts[0])
    bid = int(parts[1])
    score = cls.calc(cards, newv)
    h = Hand(cards, bid, score)
    
    return h
  
  @staticmethod
  def kind(cards, newv):
    # count occurrences, sort groupsizes, take highest 2
    counts = Counter(cards)
    bonus = 0
    if newv:
      bonus = counts['J']
      counts['J'] = 0
      
    d = list(sorted(counts.values())[:-3:-1])
    d[0] += bonus
    if len(d) == 1:
      d.append(0)
    lookup = [
      [1,1],
      [2,1],
      [2,2],
      [3,1],
      [3,2],
      [4,1],
      [5,0]
    ]
    return lookup.index(d)
  
  def __lt__(self, o):
    return self.score < o.score
  
  @staticmethod
  def calc(cards, newv=False):
    l = 'J23456789TQKA' if newv else '23456789TJQKA'
    r = Hand.kind(cards, newv)
    for c in cards:
      r = r * 13 + l.index(c)
    return r

def parse(i, newv):
  hands = []
  for l in i.strip().split('\n'):
    hands.append(Hand.parse(l, newv))
  dbg(hands)
  return hands
  
def solve(i, newv=False):
  hands = parse(i, newv)
  result = 0
  for i, h in enumerate(sorted(hands)):
    result += (i+1) * h.bid
  return result

def solve2(i):
  return solve(i, True)
  
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
tid = 7
 
test(solve, 6440)
test(solve2, 5905)

debug = False

do(solve)
do(solve2)
