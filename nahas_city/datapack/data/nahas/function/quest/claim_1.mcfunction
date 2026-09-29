execute if entity @s[tag=nh_q1] run tellraw @s {"text":"استلمت هذه الجائزة من قبل.","color":"yellow"}
execute if entity @s[scores={nh_kills=10..},tag=!nh_q1] run function nahas:quest/do_1
execute unless entity @s[tag=nh_q1] unless entity @s[scores={nh_kills=10..}] run tellraw @s {"text":"لم تكتمل المهمة بعد.","color":"red"}
