scoreboard players operation @s nh_tmp *= #2 nh_g
scoreboard players operation @s nh_gold += @s nh_tmp
title @s actionbar ["",{"text":"+","color":"gold"},{"score":{"name":"@s","objective":"nh_tmp"},"color":"gold"},{"text":" ذهب","color":"gold"}]
