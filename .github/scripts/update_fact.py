import json
import os
import random
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FACTS_PATH = os.path.join(REPO_ROOT, "animals.json")
HISTORY_PATH = os.path.join(REPO_ROOT, ".github", "scripts", "used_facts.json")
README_PATH = os.path.join(REPO_ROOT, "README.md")

with open(FACTS_PATH, "r", encoding="utf-8") as f:
    facts = json.load(f)

if os.path.exists(HISTORY_PATH):
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        used = set(json.load(f))
else:
    used = set()

# If we've used every fact, reset the history so it starts cycling again
unused_indices = [i for i in range(len(facts)) if i not in used]
if not unused_indices:
    used = set()
    unused_indices = list(range(len(facts)))

chosen_index = random.choice(unused_indices)
used.add(chosen_index)
chosen = facts[chosen_index]

with open(HISTORY_PATH, "w", encoding="utf-8") as f:
    json.dump(sorted(used), f)

new_block = f"{chosen['emoji']} {chosen['fact']}"

with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(
    r"<!--ANIMAL_FACT_START-->.*<!--ANIMAL_FACT_END-->",
    f"<!--ANIMAL_FACT_START-->\n{new_block}\n<!--ANIMAL_FACT_END-->",
    content,
    flags=re.DOTALL,
)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated README with: {new_block}")