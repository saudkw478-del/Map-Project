execute if entity @s[tag=nh_q2] run tellraw @s {"text":"استلمت هذه الجائزة من قبل.","color":"yellow"}
execute if entity @s[scores={nh_kills=50..},tag=!nh_q2] run function nahas:quest/do_2
execute unless entity @s[tag=nh_q2] unless entity @s[scores={nh_kills=50..}] run tellraw @s {"text":"لم تكتمل المهمة بعد.","color":"red"}
