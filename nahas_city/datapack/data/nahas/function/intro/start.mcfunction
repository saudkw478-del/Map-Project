# بداية الافتتاحية السينمائية للّاعب الجديد (المنفّذ: اللاعب). آمن: يحفظ وضع اللعب، ولها مؤقّت أمان وزر تخطٍّ.
execute if score @s nh_intro matches 0.. run return 0
function nahas:story/init
function nahas:story/sync
function nahas:intro/store_gm
tag @s add nh_seen
scoreboard players set @s nh_intro 0
scoreboard players set @s nh_scene 1
scoreboard players set @s nh_npccd 0
gamemode spectator @s
effect give @s minecraft:blindness 10 0 true
effect give @s minecraft:darkness 20 0 true
function nahas:fx/set_night
function nahas:fx/weather_thunder
title @s clear
execute in minecraft:overworld run tp @s 300.00 100.00 2084.00 facing 300 74 2050
function nahas:fx/heartbeat
