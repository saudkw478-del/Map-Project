# tick واحد من النهاية الكبرى
scoreboard players add @s nh_intro 1
execute if score @s nh_intro matches 0..759 run function nahas:intro/ending_cam
execute if score @s nh_intro matches 1..700 at @s run particle minecraft:end_rod ~ ~-5 ~ 25 8 25 0.05 15 force @s
function nahas:intro/ending_events
execute at @s as @e[type=minecraft:text_display,tag=nh_camtxt,distance=..25,limit=1,sort=nearest] run tp @s ^ ^0.4 ^4
