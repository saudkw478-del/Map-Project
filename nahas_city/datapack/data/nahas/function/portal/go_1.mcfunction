scoreboard players set @s nh_gocd 45
particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
execute in minecraft:overworld run tp @s 300.5 71 2050.5
playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
tellraw @s {"text":"وصلت إلى معسكر القافلة المهجور","color":"aqua"}
particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
