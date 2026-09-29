# نهاية أي مشهد سينمائي: يعيد وضع اللعب المحفوظ ويمسح المؤثّرات. يمكن للمشرف تشغيله يدويًا:
# /function nahas:intro/end (as @s) أو: /execute as <لاعب> run function nahas:intro/end
scoreboard players set @s nh_start 0
title @s clear
title @s reset
execute if score @s nh_scene matches 1 run function nahas:intro/end_1
execute if score @s nh_scene matches 2 run function nahas:intro/end_2
function nahas:fx/text_clear
effect clear @s minecraft:blindness
effect clear @s minecraft:darkness
effect clear @s minecraft:night_vision
execute unless score @s nh_introgm matches 0..2 run scoreboard players set @s nh_introgm 0
execute if score @s nh_introgm matches 0 run gamemode survival @s
execute if score @s nh_introgm matches 1 run gamemode creative @s
execute if score @s nh_introgm matches 2 run gamemode adventure @s
scoreboard players set @s nh_scene 0
scoreboard players set @s nh_intro -1
