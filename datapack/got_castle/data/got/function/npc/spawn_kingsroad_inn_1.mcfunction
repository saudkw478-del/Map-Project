scoreboard players set #npc_kingsroad_inn_1 got_g 1
summon minecraft:marker 302 64 480 {Tags:["got_warm"]}
summon minecraft:villager 304.5 64 492.5 {Tags:["got_npc","got_h_river","got_grp_kingsroad_inn_1"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 311.5 64 478.5 {Tags:["got_npc","got_h_river","got_grp_kingsroad_inn_1"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
summon minecraft:villager 296.5 64 478.5 {Tags:["got_npc","got_h_river","got_grp_kingsroad_inn_1"],VillagerData:{type:"minecraft:plains",profession:"minecraft:none",level:1},PersistenceRequired:1b,Invulnerable:1b,Rotation:[0.0f,0.0f]}
execute as @e[type=minecraft:villager,tag=got_grp_kingsroad_inn_1,sort=random,limit=1] run tag @s add got_impostor
