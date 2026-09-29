execute if entity @s[tag=nh_q3] run tellraw @s {"text":"استلمت هذه الجائزة من قبل.","color":"yellow"}
execute if entity @s[scores={nh_gold=200..},tag=!nh_q3] run function nahas:quest/do_3
execute unless entity @s[tag=nh_q3] unless entity @s[scores={nh_gold=200..}] run tellraw @s {"text":"لم تكتمل المهمة بعد.","color":"red"}
