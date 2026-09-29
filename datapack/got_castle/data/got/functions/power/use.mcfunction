execute if score @s got_pcd matches 1.. run return run title @s actionbar {"text": "\u0627\u0644\u0642\u062f\u0631\u0629 \u062a\u062d\u062a\u0627\u062c \u0648\u0642\u062a\u064b\u0627 \u0644\u0644\u062a\u0639\u0627\u0641\u064a...", "color": "red"}
execute unless entity @s[tag=got_house_any] run return run tellraw @s {"text": "\u0627\u062e\u062a\u0631 \u0628\u064a\u062a\u064b\u0627 \u0623\u0648\u0644\u064b\u0627: /trigger got_house", "color": "red"}
execute if entity @s[tag=got_h_stark] run function got:power/stark
execute if entity @s[tag=got_h_lannister] run function got:power/lannister
execute if entity @s[tag=got_h_targaryen] run function got:power/targaryen
execute if entity @s[tag=got_h_martell] run function got:power/martell
execute if entity @s[tag=got_h_tyrell] run function got:power/tyrell
execute if entity @s[tag=got_h_baratheon] run function got:power/baratheon
execute if entity @s[tag=got_h_greyjoy] run function got:power/greyjoy
execute if entity @s[tag=got_h_arryn] run function got:power/arryn
execute if entity @s[tag=got_h_tully] run function got:power/tully
