execute if score #t6 nh_g matches 0 run function nahas:trial/t6/begin
execute if score #t6 nh_g matches 1 unless entity @e[tag=nh_t6,distance=..500] run function nahas:trial/t6/next
execute if score #t6 nh_g matches 2 run function nahas:boss/b4/spawn
