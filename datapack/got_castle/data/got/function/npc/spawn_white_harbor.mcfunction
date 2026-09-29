scoreboard players set #npc_white_harbor got_g 1
summon minecraft:marker 395 64 470 {Tags:["got_warm"]}
summon minecraft:villager 397.5 64 474.5 {Tags:["got_npc","got_h_north","got_grp_white_harbor"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 397.5 64 487.5 {Tags:["got_npc","got_h_north","got_grp_white_harbor"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 409.5 64 486.5 {Tags:["got_npc","got_h_north","got_grp_white_harbor"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_white_harbor,sort=random,limit=1] run tag @s add got_impostor
