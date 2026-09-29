# أجواء: بوابة الجمر (300,900) نصف القطر 70
particle minecraft:flame ~ ~1 ~ 8 2 8 0.01 8 normal @s
execute if score #r nh_story matches 1..8 run playsound minecraft:block.lava.pop master @s ~ ~ ~ 0.4 0.8
