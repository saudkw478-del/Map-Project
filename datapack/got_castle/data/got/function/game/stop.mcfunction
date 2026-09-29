kill @e[tag=got_enemy]
scoreboard players set #state got_g 0
scoreboard objectives setdisplay sidebar
tellraw @a {"text": "The battle has been stopped.", "color": "gray"}
