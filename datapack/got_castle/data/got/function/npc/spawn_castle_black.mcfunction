scoreboard players set #npc_castle_black got_g 1
summon minecraft:marker 250 64 236 {Tags:["got_warm"]}
summon minecraft:villager 242.5 64 264.5 {Tags:["got_npc","got_h_watch","got_grp_castle_black"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 238.5 64 268.5 {Tags:["got_npc","got_h_watch","got_grp_castle_black"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 258.5 64 256.5 {Tags:["got_npc","got_h_watch","got_grp_castle_black"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[180.0f,0.0f]}
summon minecraft:villager 230.5 64 274.5 {Tags:["got_npc","got_h_watch","got_grp_castle_black"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 270.5 64 274.5 {Tags:["got_npc","got_h_watch","got_grp_castle_black"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 234.5 64 260.5 {Tags:["got_npc","got_h_watch","got_grp_castle_black"],VillagerData:{type:"minecraft:taiga",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[270.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_castle_black,sort=random,limit=1] run tag @s add got_impostor
