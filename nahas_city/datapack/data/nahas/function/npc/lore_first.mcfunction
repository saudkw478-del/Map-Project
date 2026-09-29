# أول اكتشاف لحجر (المنفّذ: اللاعب)
scoreboard players add @s nh_lorefound 1
title @s actionbar {"text":"اكتشفتَ سرًّا جديدًا!","color":"green"}
execute if score @s nh_lorefound matches 8 run function nahas:npc/lore_all
