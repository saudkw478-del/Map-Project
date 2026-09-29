execute store result score #n nh_g run clear @s minecraft:gold_ingot
scoreboard players operation #n nh_g *= #10 nh_g
scoreboard players operation @s nh_gold += #n nh_g
tellraw @s ["",{"text":"بعت سبائك الذهب. ذهبك الآن: ","color":"green"},{"score":{"name":"@s","objective":"nh_gold"},"color":"yellow"}]
