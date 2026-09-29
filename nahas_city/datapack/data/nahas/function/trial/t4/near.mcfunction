execute if score #t4 nh_g matches 0 run function nahas:trial/t4/announce
execute if score #t4 nh_g matches 0 run scoreboard players set #t4 nh_g 1
execute if score #t4 nh_g matches 1 positioned 1700 152 436 if entity @a[distance=..22] run function nahas:boss/b2/spawn
