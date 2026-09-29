# tick واحد من الافتتاحية (يُستدعى من hook/tick لكل لاعب داخل المشهد 1)
scoreboard players add @s nh_intro 1
function nahas:intro/beats
execute if score @s nh_intro matches 0..419 run function nahas:intro/cam_orbit
execute if score @s nh_intro matches 420..519 run function nahas:intro/cam_approach
execute if score @s nh_intro matches 520..609 run function nahas:intro/cam_dolly
execute if score @s nh_intro matches 1..560 at @s run function nahas:fx/sandstorm
function nahas:intro/events
execute at @s as @e[type=minecraft:text_display,tag=nh_camtxt,distance=..25,limit=1,sort=nearest] run tp @s ^ ^0.4 ^4
