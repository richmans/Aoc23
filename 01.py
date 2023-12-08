import re

def solve(i):
  s = 0
  for l in i.split('\n'):
    d = [c for c in l if c.isdigit()]
    if len(d) < 1:
      continue
    n = int(d[0] + d[-1])
    s += n
  return s
  
def solve2(i):
  num=['zerottt','one','two','three','four','five','six','seven','eight','nine']
  reg = '(?=('+'|'.join(num) + '|[1-9]))'
  sum = 0
  for l in i.split('\n'):
    nums = re.findall(reg, l)
    if len(nums) == 0:
      continue
    #print(nums)
    first = nums[0]
    last = nums[-1]
    if first in num:
      first = str(num.index(first))
    if last in num:
      last = str(num.index(last))
    sum += int(first+last)
  return sum
  
def test(fn, f, ex):
  i = open(f).read()
  o = fn(i)
  if o != ex:
    print(f"ERROR: expect {ex} got {o}")
  else:
    print("test ok")

def do(fn):
  i = open("input/01.txt").read()
  o = fn(i)
  print(fn.__name__, o)
  
test(solve, "input/01.test.txt", 142)
test(solve2,"input/01.test2.txt", 281)
do(solve)
do(solve2)
