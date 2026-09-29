scoreboard players set #npc_gulltown got_g 1
summon minecraft:marker 560 64 668 {Tags:["got_warm"]}
summon minecraft:villager 565.5 64 680.5 {Tags:["got_npc","got_h_vale","got_grp_gulltown"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 559.5 64 667.5 {Tags:["got_npc","got_h_vale","got_grp_gulltown"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 552.5 64 681.5 {Tags:["got_npc","got_h_vale","got_grp_gulltown"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 572.5 64 667.5 {Tags:["got_npc","got_h_vale","got_grp_gulltown"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_gulltown,sort=random,limit=1] run tag @s add got_impostor
