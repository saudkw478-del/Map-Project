execute as @e[type=minecraft:villager,tag=got_npc,sort=nearest,limit=1,distance=..5] at @s run function got:npc/accused
scoreboard players set @s got_accuse 0
