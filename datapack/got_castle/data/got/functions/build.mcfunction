kill @e[tag=got_origin]
kill @e[tag=got_gate]
kill @e[tag=got_center]
execute align xyz run summon minecraft:marker ~ ~ ~ {Tags:["got_origin"]}
tellraw @a {"text": "\u062c\u0627\u0631\u064d \u0628\u0646\u0627\u0621 \u0627\u0644\u0642\u0644\u0639\u0629... \u0627\u0628\u0642\u064e \u0642\u0631\u0628 \u0627\u0644\u0645\u0646\u062a\u0635\u0641 \u0646\u062d\u0648 20 \u062b\u0627\u0646\u064a\u0629.", "color": "yellow"}
execute at @e[tag=got_origin,limit=1] run forceload add ~-60 ~-60 ~60 ~60
schedule function got:build/s1_ground 40t
