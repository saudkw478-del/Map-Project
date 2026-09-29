scoreboard players set #npc_lannisport got_g 1
summon minecraft:marker 96 64 850 {Tags:["got_warm"]}
summon minecraft:villager 104.5 64 845.5 {Tags:["got_npc","got_h_west","got_grp_lannisport"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 84.5 64 844.5 {Tags:["got_npc","got_h_west","got_grp_lannisport"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 90.5 64 865.5 {Tags:["got_npc","got_h_west","got_grp_lannisport"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 111.5 64 863.5 {Tags:["got_npc","got_h_west","got_grp_lannisport"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_lannisport,sort=random,limit=1] run tag @s add got_impostor
