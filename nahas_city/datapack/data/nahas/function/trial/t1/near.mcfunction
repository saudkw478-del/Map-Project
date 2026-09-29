execute if score #t1 nh_g matches 0 run function nahas:trial/t1/begin
execute if score #t1 nh_g matches 1..3 unless entity @e[tag=nh_t1,distance=..100] run function nahas:trial/t1/next
