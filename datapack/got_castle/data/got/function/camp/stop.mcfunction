scoreboard players set #camp got_g 0
scoreboard players set #camp_battle got_g 0
kill @e[tag=got_enemy]
kill @e[tag=got_wight]
scoreboard players set #state got_g 0
scoreboard objectives setdisplay sidebar
tellraw @a {"text": "\u0623\u064f\u0648\u0642\u0641\u062a \u0627\u0644\u062d\u0645\u0644\u0629.", "color": "gray"}
