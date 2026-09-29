execute unless entity @s[tag=nh_d_city] run tellraw @s {"text":"لم تكتشف هذا المكان بعد.","color":"red"}
execute unless score #city nh_g matches 1 run tellraw @s {"text":"بوابة المدينة مغلقة حتى تجمعوا ستة أختام.","color":"red"}
execute if score #city nh_g matches 1 run scoreboard players set @s nh_gocd 45
execute if score #city nh_g matches 1 run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
execute if score #city nh_g matches 1 run execute in minecraft:overworld run tp @s 1200.5 71 1364.5
execute if score #city nh_g matches 1 run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
execute if score #city nh_g matches 1 run tellraw @s {"text":"وصلت إلى مدينة النحاس","color":"aqua"}
execute if score #city nh_g matches 1 run particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30
