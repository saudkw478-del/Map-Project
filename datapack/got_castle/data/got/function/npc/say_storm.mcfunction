execute store result score #r got_g run random value 1..5
execute if score #r got_g matches 1 run tellraw @a[distance=..10] [{"text": "<Stormlander> ", "color": "yellow"}, {"text": "Ours is the Fury! Storm's End has never fallen to a siege.", "color": "white"}]
execute if score #r got_g matches 2 run tellraw @a[distance=..10] [{"text": "<Stormlander> ", "color": "yellow"}, {"text": "The walls here are older than the kingdom. Stone cannot be scared.", "color": "white"}]
execute if score #r got_g matches 3 run tellraw @a[distance=..10] [{"text": "<Stormlander> ", "color": "yellow"}, {"text": "They say a shadow once crept through the wall. Guard the gate anyway.", "color": "white"}]
execute if score #r got_g matches 4 run tellraw @a[distance=..10] [{"text": "<Stormlander> ", "color": "yellow"}, {"text": "Stannis is a grim man, but a fair one. Do you fight well?", "color": "white"}]
execute if score #r got_g matches 5 run tellraw @a[distance=..10] [{"text": "<Stormlander> ", "color": "yellow"}, {"text": "The armory has heavy armor. Take it - you will need it against the wave.", "color": "white"}]
playsound minecraft:entity.villager.ambient master @a[distance=..10]
