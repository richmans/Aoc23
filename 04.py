from dataclasses import dataclass
import math

@dataclass
class Card:
  cid: int
  having: set[int]
  winning: set[int]

  @classmethod
  def parse(cls, l):
    cname, body = l.split(': ')
    cid = int(cname[5:])
    having_str, winning_str = body.split(' | ')
    having = {int(n.strip()) for n in having_str.split(' ') if len(n) > 0}
    winning = {int(n.strip()) for n in winning_str.split(' ') if len(n) > 0}
    card = Card(cid, having, winning)
    return card
  
  def winners(self):
    return len(self.having.intersection(self.winning))
  
  
def parse(i):
  cards = []
  for l in i.strip().split('\n'):
    cards.append(Card.parse(l))
  dbg(cards)
  return cards

def dbg(*msg):
  if debug:
    print(*msg)

def solve(i):
  cards = parse(i)
  return sum([int(2 ** (c.winners() -1)) for c in cards])
  
def solve2(i):
  cards = parse(i)
  i = 0
  amounts = {c.cid: 1 for c in cards}

  for c in cards:
    dbg(f"Card {c.cid} Appending {c.winners()} cards")
    for j in range(c.winners()):
      dbg(f"Won card {c.cid+j+1}")
      amounts[c.cid+j+1] += amounts[c.cid]
  dbg(amounts)
  return sum(amounts.values())
  
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
tid = 4
 
test(solve, 13)
test(solve2, 30)
do(solve)
do(solve2)
