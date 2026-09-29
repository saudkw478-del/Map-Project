# أجواء: معبد الواحة (1000,1900) نصف القطر 80
particle minecraft:enchant ~ ~1.5 ~ 6 3 6 0.4 20 normal @s
execute if score #r nh_story matches 1..8 run playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 0.4 0.7
