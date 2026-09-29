# أجواء: وادي العقارب (1800,1850) نصف القطر 80
particle minecraft:dust{color:[0.8,0.3,0.15],scale:1.5} ~ ~1 ~ 8 2 8 0.1 15 normal @s
execute if score #r nh_story matches 1..6 run playsound minecraft:entity.spider.ambient master @s ~ ~ ~ 0.3 0.6
