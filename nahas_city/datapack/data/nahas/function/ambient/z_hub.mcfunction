# أجواء: واحة الدلال (600,1650) نصف القطر 80
particle minecraft:glow ~ ~2 ~ 8 3 8 0.02 6 normal @s
execute if score #r nh_story matches 1..6 run playsound minecraft:entity.villager.ambient master @s ~ ~ ~ 0.4 1
