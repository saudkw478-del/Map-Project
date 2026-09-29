tag @s add nh_seen
scoreboard players set @s nh_gold 20
scoreboard players set @s nh_prole 0
scoreboard players set @s nh_lastk 0
loot give @s loot nahas:kit/start
advancement grant @s only nahas:root
advancement grant @s only nahas:lantern
spawnpoint @s 300 71 2050
scoreboard players set #started nh_g 1
title @s times 10 70 20
title @s subtitle {"text":"ليلة الفانوس","color":"yellow"}
title @s title {"text":"مدينة النحاس","color":"gold"}
tellraw @s {"text":"أهلاً بك أيها المسافر! معك فانوس الجني. اكتب /trigger nh_help set 1 لتعرف الأوامر.","color":"yellow"}
function nahas:role/menu
function nahas:hook/first_join
