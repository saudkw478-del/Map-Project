# أجواء: قلعة الريح (1700,450) نصف القطر 80
particle minecraft:cloud ~ ~1 ~ 10 4 10 0.05 10 normal @s
execute if score #r nh_story matches 1..10 run playsound minecraft:item.elytra.flying master @s ~ ~ ~ 0.2 0.6
