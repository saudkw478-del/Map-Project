# يبدأ الحوار مع أقرب شخصية (المنفّذ: اللاعب). الفاصل بين الجمل 8 ثوانٍ؛ الجمل تتغيّر حسب عدد الأختام (#seals).
scoreboard players set @s nh_npccd 8
execute as @e[type=minecraft:villager,tag=nh_npc,distance=..3.5,limit=1,sort=nearest] at @s run tp @s ~ ~ ~ facing entity @p eyes
scoreboard players add @s nh_npcline 1
scoreboard players operation @s nh_npcline %= #2 nh_story
execute if entity @e[type=minecraft:villager,tag=nh_npc_salem,distance=..3.5] run function nahas:npc/talk/salem
execute if entity @e[type=minecraft:villager,tag=nh_npc_umzaid,distance=..3.5] run function nahas:npc/talk/umzaid
execute if entity @e[type=minecraft:villager,tag=nh_npc_mansour,distance=..3.5] run function nahas:npc/talk/mansour
execute if entity @e[type=minecraft:villager,tag=nh_npc_fahd,distance=..3.5] run function nahas:npc/talk/fahd
execute if entity @e[type=minecraft:villager,tag=nh_npc_jinni,distance=..3.5] run function nahas:npc/talk/jinni
execute if entity @e[type=minecraft:villager,tag=nh_npc_layla,distance=..3.5] run function nahas:npc/talk/layla
execute if entity @e[type=minecraft:villager,tag=nh_npc_hamdan,distance=..3.5] run function nahas:npc/talk/hamdan
execute if entity @e[type=minecraft:villager,tag=nh_npc_zahra,distance=..3.5] run function nahas:npc/talk/zahra
execute if entity @e[type=minecraft:villager,tag=nh_npc_barq,distance=..3.5] run function nahas:npc/talk/barq
execute if entity @e[type=minecraft:villager,tag=nh_npc_masoud,distance=..3.5] run function nahas:npc/talk/masoud
particle minecraft:happy_villager ~ ~2 ~ 0.4 0.4 0.4 0 6 normal @s
playsound minecraft:entity.villager.celebrate master @s ~ ~ ~ 0.7 1.1
