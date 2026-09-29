scoreboard players set #npc_kl_city got_g 1
summon minecraft:marker 360 64 868 {Tags:["got_warm"]}
summon minecraft:villager 423.5 64 812.5 {Tags:["got_npc","got_h_crown","got_grp_kl_city"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 366.5 64 870.5 {Tags:["got_npc","got_h_crown","got_grp_kl_city"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 354.5 64 864.5 {Tags:["got_npc","got_h_crown","got_grp_kl_city"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 363.5 64 860.5 {Tags:["got_npc","got_h_crown","got_grp_kl_city"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
summon minecraft:villager 357.5 64 874.5 {Tags:["got_npc","got_h_crown","got_grp_kl_city"],VillagerData:{type:"minecraft:jungle",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[90.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_kl_city,sort=random,limit=1] run tag @s add got_impostor
