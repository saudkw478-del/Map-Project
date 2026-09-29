kill @e[tag=got_enemy]
scoreboard players set #state got_g 0
scoreboard objectives setdisplay sidebar
tellraw @a {"text": "Game stopped.", "color": "gray"}
