scoreboard players set #npc_riverrun got_g 1
summon minecraft:marker 215 64 720 {Tags:["got_warm"]}
summon minecraft:villager 207.5 64 748.5 {Tags:["got_npc","got_h_river","got_grp_riverrun"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 203.5 64 752.5 {Tags:["got_npc","got_h_river","got_grp_riverrun"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 223.5 64 740.5 {Tags:["got_npc","got_h_river","got_grp_riverrun"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[180.0f,0.0f]}
summon minecraft:villager 195.5 64 758.5 {Tags:["got_npc","got_h_river","got_grp_riverrun"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 235.5 64 758.5 {Tags:["got_npc","got_h_river","got_grp_riverrun"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 199.5 64 744.5 {Tags:["got_npc","got_h_river","got_grp_riverrun"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[270.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_riverrun,sort=random,limit=1] run tag @s add got_impostor
