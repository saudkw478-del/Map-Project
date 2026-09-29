scoreboard players set #npc_winter_town got_g 1
summon minecraft:marker 215 64 452 {Tags:["got_warm"]}
summon minecraft:villager 223.5 64 447.5 {Tags:["got_npc","got_h_north","got_grp_winter_town"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 233.5 64 467.5 {Tags:["got_npc","got_h_north","got_grp_winter_town"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 202.5 64 448.5 {Tags:["got_npc","got_h_north","got_grp_winter_town"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 201.5 64 463.5 {Tags:["got_npc","got_h_north","got_grp_winter_town"],VillagerData:{type:"minecraft:snow",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_winter_town,sort=random,limit=1] run tag @s add got_impostor
