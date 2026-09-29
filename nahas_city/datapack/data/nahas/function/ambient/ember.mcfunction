# أجواء أرض الجمر
particle minecraft:white_ash ~ ~2 ~ 12 5 12 0.05 20 normal @s
execute if score #r nh_story matches 1..6 run playsound minecraft:block.lava.pop master @s ~ ~ ~ 0.4 0.8
