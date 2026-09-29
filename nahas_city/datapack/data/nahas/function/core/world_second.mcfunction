function nahas:core/discover
execute if score #city nh_g matches 1 unless score #gate nh_g matches 1 in minecraft:overworld positioned 1200 70 1350 if entity @a[distance=..80] run function nahas:core/gate_open
execute in nahas:ember positioned 500 64 500 run effect give @a[distance=..3000] minecraft:fire_resistance 15 0 true
execute in nahas:ember as @a at @s if block ~ ~ ~ minecraft:lava run function nahas:portal/rescue_ember
execute in nahas:star_sea as @a[y=-200,dy=220] run function nahas:portal/rescue_star
