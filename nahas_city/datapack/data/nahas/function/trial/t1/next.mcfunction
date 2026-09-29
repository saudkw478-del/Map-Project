scoreboard players add #t1 nh_g 1
execute if score #t1 nh_g matches 2..3 run tellraw @a[distance=..100] ["",{"text":"موجة جديدة من الحراس!","color":"red"}]
execute if score #t1 nh_g matches 2 run function nahas:trial/t1/w2
execute if score #t1 nh_g matches 3 run function nahas:trial/t1/w3
execute if score #t1 nh_g matches 4 run function nahas:trial/complete_1
