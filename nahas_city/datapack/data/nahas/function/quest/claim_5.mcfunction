execute if entity @s[tag=nh_q5] run tellraw @s {"text":"استلمت هذه الجائزة من قبل.","color":"yellow"}
execute unless entity @s[tag=nh_q5] if score #seals nh_g matches 3.. run function nahas:quest/do_5
execute unless entity @s[tag=nh_q5] unless score #seals nh_g matches 3.. run tellraw @s {"text":"لم تكتمل المهمة بعد.","color":"red"}
