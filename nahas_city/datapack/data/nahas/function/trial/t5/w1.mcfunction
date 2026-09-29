summon minecraft:vex ~6 ~1 ~3 {Tags:["nh_t5","nh_trial"],PersistenceRequired:1b}
summon minecraft:vex ~-6 ~1 ~3 {Tags:["nh_t5","nh_trial"],PersistenceRequired:1b}
execute unless score #kids nh_g matches 1 run summon minecraft:vex ~0 ~1 ~-8 {Tags:["nh_t5","nh_trial"],PersistenceRequired:1b}
particle minecraft:poof ~ ~2 ~ 8 1 8 0.05 40
playsound minecraft:entity.evoker.prepare_summon master @a[distance=..100] ~ ~ ~ 1 0.8
