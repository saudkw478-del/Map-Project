# أجواء بحر النجوم
particle minecraft:end_rod ~ ~ ~ 12 6 12 0.01 10 normal @s
execute if score #r nh_story matches 1..6 run playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 0.4 0.5
