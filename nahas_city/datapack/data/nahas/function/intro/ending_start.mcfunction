# بداية النهاية الكبرى (المنفّذ: كل لاعب)
function nahas:story/init
execute unless score @s nh_intro matches 0.. run function nahas:intro/store_gm
scoreboard players set @s nh_intro 0
scoreboard players set @s nh_scene 2
gamemode spectator @s
effect give @s minecraft:blindness 3 0 true
title @s clear
execute in minecraft:overworld run tp @s 1200.00 96.00 1232.00 facing 1200 78 1200
tellraw @s [{"text":"للتخطي اكتب ","color":"gray"},{"text":"/trigger nh_start set 1","color":"yellow","clickEvent":{"action":"run_command","value":"/trigger nh_start set 1"},"click_event":{"action":"run_command","command":"/trigger nh_start set 1"}},{"text":" (أو اضغط هنا)","color":"gray"}]
