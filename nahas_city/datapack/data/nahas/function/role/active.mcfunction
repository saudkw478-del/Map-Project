execute unless score @s nh_prole matches 1..4 run tellraw @s {"text":"اختر دورك أولاً: /trigger nh_role set 1","color":"red"}
execute if score @s nh_prole matches 1..4 if score @s nh_cd matches 1.. run tellraw @s ["",{"text":"قوتك تحتاج إلى راحة: ","color":"red"},{"score":{"name":"@s","objective":"nh_cd"},"color":"yellow"},{"text":" ثانية","color":"red"}]
execute if score @s nh_prole matches 1..4 if score @s nh_cd matches ..0 run function nahas:role/fire
