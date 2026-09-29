scoreboard players set #npc_storms_end got_g 1
summon minecraft:marker 480 64 1005 {Tags:["got_warm"]}
summon minecraft:villager 472.5 64 1033.5 {Tags:["got_npc","got_h_storm","got_grp_storms_end"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 468.5 64 1037.5 {Tags:["got_npc","got_h_storm","got_grp_storms_end"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 488.5 64 1025.5 {Tags:["got_npc","got_h_storm","got_grp_storms_end"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[180.0f,0.0f]}
summon minecraft:villager 460.5 64 1043.5 {Tags:["got_npc","got_h_storm","got_grp_storms_end"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 500.5 64 1043.5 {Tags:["got_npc","got_h_storm","got_grp_storms_end"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 464.5 64 1029.5 {Tags:["got_npc","got_h_storm","got_grp_storms_end"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[270.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_storms_end,sort=random,limit=1] run tag @s add got_impostor
