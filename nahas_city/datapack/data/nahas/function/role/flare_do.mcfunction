scoreboard players set @s nh_cd2 60
tellraw @s {"text":"وميض الفانوس! الأشباح تضعف.","color":"gold"}
effect give @e[distance=..15,type=#minecraft:undead] minecraft:weakness 10 1 true
effect give @e[distance=..15,type=#minecraft:undead] minecraft:glowing 10 0 true
effect give @a[distance=..12] minecraft:regeneration 5 0 true
particle minecraft:flash ~ ~1 ~ 0 0 0 0 1
particle minecraft:end_rod ~ ~1 ~ 3 1 3 0.05 60
playsound minecraft:block.beacon.activate master @a[distance=..20] ~ ~ ~ 1 1.5
