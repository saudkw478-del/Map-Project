execute store result score #n nh_g run clear @s minecraft:gold_nugget
scoreboard players operation @s nh_gold += #n nh_g
tellraw @s ["",{"text":"بعت قطع الذهب. ذهبك الآن: ","color":"green"},{"score":{"name":"@s","objective":"nh_gold"},"color":"yellow"}]
