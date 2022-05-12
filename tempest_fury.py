from random import randint
import re

def lexer(expression):
    regex = re.compile("|".join("(?P<{}>{})".format(token_type, regex) for token_type, regex in (
        ("dice",r'\d+(?=d)'),
        ("sides", r'(?<=d)\d+'),
        ("add", r'(?<=\+)\d+'),
        ("mult", r'(?<=\*)\d+'),
        ("dc", r'(?<=\-)\d+'),
        ("res", r'(?<=/)\d+'),
        )))
    li = [ ( match.group(0), match.lastgroup ) for match in regex.finditer(expression) ]
    di = {"add":0,"mult":1,"dc":0,"res":1}
    for item in li:
      di[str(item[1])] = int(item[0])
    return di

def calculate(verbose = 0):
  targets = []
  for i in range(int(input("how many targets are there? >  "))):
    value = input(f"Resistance number for target #{i+1}? >  ").split("a")
    value.append(0)
    targets.append({"resistance" : int(value[0])})
    targets[i]["ascension"] = int(value[1])
  num_bolts = int(input("How many bolts per target? >  "))
  di = lexer(input("Damage per bolt (represented as number of dice d sides ex: 3d6)? >  "))
  for i,target in enumerate(targets):
    failed = 0
    for _ in range(num_bolts):
      rolled = randint(1,20)
      if rolled == 20:
        if verbose:
          print(f"Target {i+1}: Rolled a 20! Resisted!!")
        continue
      if rolled == 1:
        failed += 1
        if verbose:
          print(f"Target {i+1}: Rolled a 1... Failed!")
        continue
      rolled += randint(1,(2+2*target["ascension"])) if target["ascension"] > 0 else 0
      if rolled < target["resistance"]:
        if verbose:
          print(f"Target {i+1}: Failed, Rolled {rolled} needed {target['resistance']}")
        failed += 1
      elif verbose:
        print(f"Target {i+1}: Resisted, Rolled {rolled} needed {target['resistance']}")
    target["failed"] = failed
  for i,target in enumerate(targets):
    damage = 0
    for roll in range(target["failed"]):
      rolled_damage = 0
      for _ in range(di['dice']):
        rolled_damage += randint(1,di["sides"])
      total_damage = (rolled_damage+ di["add"])*di["mult"] // di["res"] - di["dc"]
      damage += total_damage
      if verbose > 1:
        print(f"Damage Roll #{roll+1} deals {total_damage} damage")
    print(f"Target {i+1} failed {target['failed']} resistances and takes {damage} damage!")


if __name__ == "__main__":
  calculate()