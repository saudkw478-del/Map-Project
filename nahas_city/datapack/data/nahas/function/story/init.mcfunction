# تهيئة لوحات النتائج الخاصة بالقصة (آمنة للتكرار). تُستدعى من ambient/second و hook/first_join.
# #textmode: 0 = صيغة 1.21.4 (نص JSON)، 1 = صيغة 1.21.5+/26.x (مركّب NBT).
scoreboard objectives add nh_story dummy
scoreboard objectives add nh_intro dummy
scoreboard objectives add nh_scene dummy
scoreboard objectives add nh_introgm dummy
scoreboard objectives add nh_npccd dummy
scoreboard objectives add nh_npcline dummy
scoreboard objectives add nh_ttl dummy
scoreboard objectives add nh_askq dummy
scoreboard objectives add nh_askcd dummy
scoreboard objectives add nh_lorefound dummy
scoreboard objectives add nh_start trigger
scoreboard players set #2 nh_story 2
execute unless score #textmode nh_story matches 0.. run scoreboard players set #textmode nh_story 0
execute unless score #cityseq nh_story matches -1.. run scoreboard players set #cityseq nh_story -1
execute unless score #t nh_story matches 0.. run scoreboard players set #t nh_story 6000
# لاعبون بلا مؤقّت مشهد: -1 = خارج أي مشهد
execute as @a unless score @s nh_intro matches -1.. run scoreboard players set @s nh_intro -1
