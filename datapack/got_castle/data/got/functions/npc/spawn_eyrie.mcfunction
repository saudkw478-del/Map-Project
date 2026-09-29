scoreboard players set #npc_eyrie got_g 1
summon minecraft:marker 500 124 690 {Tags:["got_warm"]}
summon minecraft:villager 492.5 124 718.5 {Tags:["got_npc","got_h_vale","got_grp_eyrie"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 488.5 124 722.5 {Tags:["got_npc","got_h_vale","got_grp_eyrie"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 508.5 124 710.5 {Tags:["got_npc","got_h_vale","got_grp_eyrie"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[180.0f,0.0f]}
summon minecraft:villager 480.5 124 728.5 {Tags:["got_npc","got_h_vale","got_grp_eyrie"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 520.5 124 728.5 {Tags:["got_npc","got_h_vale","got_grp_eyrie"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 484.5 124 714.5 {Tags:["got_npc","got_h_vale","got_grp_eyrie"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[270.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_eyrie,sort=random,limit=1] run tag @s add got_impostor
