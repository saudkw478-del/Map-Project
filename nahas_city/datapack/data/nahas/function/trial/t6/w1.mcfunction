summon minecraft:blaze ~8 ~1 ~2 {Tags:["nh_t6","nh_trial"],PersistenceRequired:1b}
summon minecraft:blaze ~-8 ~1 ~2 {Tags:["nh_t6","nh_trial"],PersistenceRequired:1b}
execute unless score #kids nh_g matches 1 run summon minecraft:blaze ~0 ~1 ~-9 {Tags:["nh_t6","nh_trial"],PersistenceRequired:1b}
particle minecraft:poof ~ ~2 ~ 8 1 8 0.05 40
playsound minecraft:entity.evoker.prepare_summon master @a[distance=..100] ~ ~ ~ 1 0.8
