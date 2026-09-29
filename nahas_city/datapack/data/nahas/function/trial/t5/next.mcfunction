scoreboard players add #t5 nh_g 1
execute if score #t5 nh_g matches 2 run function nahas:trial/t5/w2
execute if score #t5 nh_g matches 2 run tellraw @a[distance=..800] ["",{"text":"موجة أرواح جديدة!","color":"light_purple"}]
execute if score #t5 nh_g matches 3 run tellraw @a[distance=..800] ["",{"text":"ملكة النجوم تستيقظ...","color":"light_purple"}]
