scoreboard players set #npc_casterly_rock got_g 1
summon minecraft:marker 140 64 800 {Tags:["got_warm"]}
summon minecraft:villager 132.5 64 828.5 {Tags:["got_npc","got_h_west","got_grp_casterly_rock"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 128.5 64 832.5 {Tags:["got_npc","got_h_west","got_grp_casterly_rock"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 148.5 64 820.5 {Tags:["got_npc","got_h_west","got_grp_casterly_rock"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[180.0f,0.0f]}
summon minecraft:villager 120.5 64 838.5 {Tags:["got_npc","got_h_west","got_grp_casterly_rock"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 160.5 64 838.5 {Tags:["got_npc","got_h_west","got_grp_casterly_rock"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 124.5 64 824.5 {Tags:["got_npc","got_h_west","got_grp_casterly_rock"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[270.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_casterly_rock,sort=random,limit=1] run tag @s add got_impostor
