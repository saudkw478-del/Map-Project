summon minecraft:drowned ~10 ~1 ~0 {Tags:["nh_t3","nh_trial"],PersistenceRequired:1b,DeathLootTable:"nahas:trial/page"}
summon minecraft:drowned ~-10 ~1 ~0 {Tags:["nh_t3","nh_trial"],PersistenceRequired:1b,DeathLootTable:"nahas:trial/page"}
summon minecraft:drowned ~0 ~1 ~10 {Tags:["nh_t3","nh_trial"],PersistenceRequired:1b,DeathLootTable:"nahas:trial/page"}
execute unless score #kids nh_g matches 1 run summon minecraft:drowned ~0 ~1 ~-10 {Tags:["nh_t3","nh_trial"],PersistenceRequired:1b,DeathLootTable:"nahas:trial/page"}
particle minecraft:poof ~ ~2 ~ 8 1 8 0.05 40
playsound minecraft:entity.evoker.prepare_summon master @a[distance=..100] ~ ~ ~ 1 0.8
