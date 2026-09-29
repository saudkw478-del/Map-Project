execute if score #t5 nh_g matches 0 run function nahas:trial/t5/begin
execute if score #t5 nh_g matches 1..2 unless entity @e[tag=nh_t5,distance=..800] run function nahas:trial/t5/next
execute if score #t5 nh_g matches 3 positioned 560 97 921 if entity @a[distance=..40] run function nahas:boss/b3/spawn
