scoreboard players set #npc_kings_landing got_g 1
summon minecraft:marker 405 64 880 {Tags:["got_warm"]}
summon minecraft:villager 397.5 64 908.5 {Tags:["got_npc","got_h_crown","got_grp_kings_landing"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 393.5 64 912.5 {Tags:["got_npc","got_h_crown","got_grp_kings_landing"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 413.5 64 900.5 {Tags:["got_npc","got_h_crown","got_grp_kings_landing"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[180.0f,0.0f]}
summon minecraft:villager 385.5 64 918.5 {Tags:["got_npc","got_h_crown","got_grp_kings_landing"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 425.5 64 918.5 {Tags:["got_npc","got_h_crown","got_grp_kings_landing"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 389.5 64 904.5 {Tags:["got_npc","got_h_crown","got_grp_kings_landing"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[270.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_kings_landing,sort=random,limit=1] run tag @s add got_impostor
