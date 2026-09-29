scoreboard players set @s nh_gocd 45
particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
execute in minecraft:overworld run tp @s 600.5 71 1650.5
playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
tellraw @s {"text":"وصلت إلى واحة الدلال","color":"aqua"}
particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
