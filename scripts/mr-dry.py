!alias mr-dry embed
<drac2>
D = """
- A character may spend Hit Dice to regain hit points like a short rest.
- A character regains Hit Dice equal to half of the characterss total number of them, or one quarter if they slept in medium or heavy armor (minimum of one die).
- Class features and resources you regain after finishing a long rest are benefits of a medium rest.
- Spellcasters regain only half their maximum spell slots (rounded down) of 5th level or lower.
"""

ch=character()
sb=ch.spellbook

# get spell slot info
slots = []
for level in range(1, 6):
    used = sb.get_slots(level)  # returns used, not available
    total = sb.get_max_slots(level)
    regain = total // 2
    if regain > 0:
        slots.append((level, used, total, regain))

# get consumable info
consumables = [
    c
    for c in ch.consumables if c.min >= 0
]

# hit dice info
hit_dice = max(1, ch.levels.total_level // 2)

# Prepare the output
T = "Medium Rest"
F = "You will regain:\n"
F += f"\n\t- {hit_dice} Hit Dice\n"
F += "\n\t".join([
    f"- {regain} level {level} spell slot(s), you have {total - used}/{total} remaining."
    for level, used, total, regain in slots
])
F += "\n"
F += "\n\t".join([f"- All charges of {c.name}, you have {c.value}/{c.max} remaining." for c in consumables])

</drac2>
-title "{{T}}"
-desc "{{D}}"
-f "{{F}}"
-color <color>
-thumb <image>