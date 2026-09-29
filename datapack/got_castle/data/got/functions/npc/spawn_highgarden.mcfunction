scoreboard players set #npc_highgarden got_g 1
summon minecraft:marker 215 64 1030 {Tags:["got_warm"]}
summon minecraft:villager 207.5 64 1058.5 {Tags:["got_npc","got_h_reach","got_grp_highgarden"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 203.5 64 1062.5 {Tags:["got_npc","got_h_reach","got_grp_highgarden"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 223.5 64 1050.5 {Tags:["got_npc","got_h_reach","got_grp_highgarden"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[180.0f,0.0f]}
summon minecraft:villager 195.5 64 1068.5 {Tags:["got_npc","got_h_reach","got_grp_highgarden"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 235.5 64 1068.5 {Tags:["got_npc","got_h_reach","got_grp_highgarden"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 199.5 64 1054.5 {Tags:["got_npc","got_h_reach","got_grp_highgarden"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[270.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_highgarden,sort=random,limit=1] run tag @s add got_impostor
