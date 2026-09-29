execute if score #t2 nh_g matches 0 run function nahas:trial/t2/announce
execute if score #t2 nh_g matches 0 run scoreboard players set #t2 nh_g 1
execute if score #t2 nh_g matches 1 if entity @a[distance=..28] run function nahas:boss/b1/spawn
