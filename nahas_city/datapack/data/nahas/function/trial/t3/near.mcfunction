execute if score #t3 nh_g matches 0 run function nahas:trial/t3/begin
execute if score #t3 nh_g matches 1 store result score #pg nh_g run clear @a[distance=..100] minecraft:paper[minecraft:custom_data={nh:"page"}] 0
execute if score #t3 nh_g matches 1 if score #pg nh_g matches 3.. run function nahas:trial/t3/finish
execute if score #t3 nh_g matches 1 if score #pg nh_g matches ..2 unless entity @e[tag=nh_t3,distance=..100] run function nahas:trial/t3/w1
