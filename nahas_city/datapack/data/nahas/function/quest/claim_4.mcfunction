execute if entity @s[tag=nh_q4] run tellraw @s {"text":"استلمت هذه الجائزة من قبل.","color":"yellow"}
execute if entity @s[scores={nh_disc=5..},tag=!nh_q4] run function nahas:quest/do_4
execute unless entity @s[tag=nh_q4] unless entity @s[scores={nh_disc=5..}] run tellraw @s {"text":"لم تكتمل المهمة بعد.","color":"red"}
