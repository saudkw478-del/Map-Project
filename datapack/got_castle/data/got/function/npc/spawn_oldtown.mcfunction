scoreboard players set #npc_oldtown got_g 1
summon minecraft:marker 138 64 1155 {Tags:["got_warm"]}
summon minecraft:villager 126.5 64 1163.5 {Tags:["got_npc","got_h_reach","got_grp_oldtown"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 125.5 64 1178.5 {Tags:["got_npc","got_h_reach","got_grp_oldtown"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 151.5 64 1170.5 {Tags:["got_npc","got_h_reach","got_grp_oldtown"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 148.5 64 1154.5 {Tags:["got_npc","got_h_reach","got_grp_oldtown"],VillagerData:{type:"minecraft:savanna",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_oldtown,sort=random,limit=1] run tag @s add got_impostor
