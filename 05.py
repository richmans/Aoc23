from dataclasses import dataclass

@dataclass
class MapRule:
  dstart: int
  start: int
  stop: int

  @classmethod
  def parse(cls, r):
    l = next(r)
    if l is None or len(l) == 0: 
      return None
    dstart, start, size = [int(x) for x in l.strip().split(' ')]
    stop = start + size
    return MapRule(dstart, start, stop)
  
  def map_range(self, ran):
    mappable = range(max(self.start,ran.start), min(self.stop,ran.stop)) or None
    if mappable is None:
      return None, [ran]
    unmapped = []
    pre = range(ran.start, mappable.start)
    post = range(mappable.stop, ran.stop)
    if len(pre) > 0:
      unmapped.append(pre)
    if len(post) > 0:
      unmapped.append(post)
    mapped_start = mappable.start - self.start + self.dstart
    mapped_stop = mappable.stop - self.start + self.dstart
    mapped = range(mapped_start, mapped_stop)
    return mapped, unmapped
  
@dataclass
class Mapper:
  name: str
  rules: list[MapRule]

  @classmethod
  def parse(cls, r):
    title = next(r)
    if title is None: 
      return None
    name = title[:-5]
    rules = []
    while (rule := MapRule.parse(r)) is not None:
      rules.append(rule)
    return Mapper(name, rules)

  def map(self, i):
    for r in self.rules:      
      if i >= r.start and i < r.stop:
        return r.dstart + i - r.start
    return i
  
  # input: a range for instance (0, 30)
  # output: a list of ranges, for instance [(0, 10), (140, 150), (20, 30)]
  def map_range(self, ran):
    unmapped_ranges = [ran]
    mapped_ranges = []
    for r in self.rules:
      # for each rule:
      # try to map all unmapped ranges
      # * collect all mapped ranges
      # * save all unmapped ranges for the next rule
      # when all rules are done, all unmapped ranges are identity-mapped
      next_unmapped = []
      for x in unmapped_ranges:
        dbg('l', x)
        m, u = r.map_range(x)
        dbg('mu', m, u)
        if m:
          mapped_ranges.append(m)
        next_unmapped += u
      unmapped_ranges = next_unmapped
    return mapped_ranges + unmapped_ranges

@dataclass
class Garden:
  TOPICS = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
  
  seeds: set[int]
  maps: dict[str, Mapper]

  @classmethod
  def parse(cls, r, newstyle=False):
    seed_numbers = [int(s) for s in next(r)[7:].split(' ')]
    seeds = None
    if newstyle:
      seeds = []
      for i in range(0, len(seed_numbers), 2):
        seeds.append(range(seed_numbers[i], seed_numbers[i] + seed_numbers[i+1]))
    else:
      seeds = seed_numbers
    next(r)
    maps = {}
    while True:
      m = Mapper.parse(r)
      if m is None:
        break
      maps[m.name] = m
      
    return Garden(seeds, maps)
  
def line_reader(i):
  for l in i.strip().split('\n'):
    yield l.strip()
  while True:
    yield None

def parse(i, newstyle=False):
  r = line_reader(i)
  g = Garden.parse(r, newstyle)
  return g

def dbg(*msg):
  if debug:
    print(*msg)

def solve(i):
  garden = parse(i)
  locations = []
  for item in garden.seeds:
    dbg("SEED", item)
    for tid in range(len(Garden.TOPICS) -1):
      mname = f"{Garden.TOPICS[tid]}-to-{Garden.TOPICS[tid+1]}"
      initem = item
      item = garden.maps[mname].map(item)
      dbg(initem, mname, item)
    locations.append(item)
  return min(locations)

def solve2(i):
  garden = parse(i, True)
  dbg(garden)
  locations = []
  for item in garden.seeds:
    dbg("SEED", item)
    ranges = [item]
    for tid in range(len(Garden.TOPICS) -1):
      mname = f"{Garden.TOPICS[tid]}-to-{Garden.TOPICS[tid+1]}"
      new_ranges = []
      for r in ranges:
        new_ranges += garden.maps[mname].map_range(r)
      dbg(mname, ranges, new_ranges)
      ranges = new_ranges
    locations += ranges
  return min([l.start for l in locations])
  
def test_map():
  m = Mapper('dude', [MapRule(100, 5, 20)])
  assert(m.map(7) == 102)
  assert(m.map(2) == 2)
  assert(m.map(22) == 22)
  assert(m.map_range(range(0, 10)) == [range(100, 105), range(0, 5)])
  print("Map test ok")

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
tid = 5
 
test(solve, 35)
test(solve2, 46)
test_map()

debug = False
do(solve)
do(solve2)
