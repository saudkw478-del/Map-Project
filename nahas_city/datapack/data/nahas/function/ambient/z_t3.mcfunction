# أجواء: المكتبة الغارقة (2100,1300) نصف القطر 80
particle minecraft:bubble ~ ~1 ~ 6 2 6 0.05 12 normal @s
execute if score #r nh_story matches 1..8 run playsound minecraft:ambient.underwater.loop.additions master @s ~ ~ ~ 0.4 1
