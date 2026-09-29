scoreboard players set #npc_winterfell got_g 1
summon minecraft:marker 270 64 350 {Tags:["got_warm"]}
summon minecraft:villager 262.5 64 378.5 {Tags:["got_npc","got_h_north","got_grp_winterfell"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 258.5 64 382.5 {Tags:["got_npc","got_h_north","got_grp_winterfell"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 278.5 64 370.5 {Tags:["got_npc","got_h_north","got_grp_winterfell"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[180.0f,0.0f]}
summon minecraft:villager 250.5 64 388.5 {Tags:["got_npc","got_h_north","got_grp_winterfell"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 290.5 64 388.5 {Tags:["got_npc","got_h_north","got_grp_winterfell"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 254.5 64 374.5 {Tags:["got_npc","got_h_north","got_grp_winterfell"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[270.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_winterfell,sort=random,limit=1] run tag @s add got_impostor
