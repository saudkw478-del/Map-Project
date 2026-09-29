execute if score #t7 nh_g matches 0 if score #city nh_g matches 1 run function nahas:trial/t7/announce
execute if score #t7 nh_g matches 0 if score #city nh_g matches 1 run scoreboard players set #t7 nh_g 1
execute if score #t7 nh_g matches 1 if entity @a[distance=..30] run function nahas:boss/b5/spawn
