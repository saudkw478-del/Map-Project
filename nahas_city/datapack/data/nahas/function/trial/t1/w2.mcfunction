summon minecraft:husk ~12 ~1 ~6 {Tags:["nh_t1","nh_trial"],PersistenceRequired:1b}
summon minecraft:pillager ~-12 ~1 ~6 {Tags:["nh_t1","nh_trial"],PersistenceRequired:1b}
summon minecraft:husk ~6 ~1 ~-12 {Tags:["nh_t1","nh_trial"],PersistenceRequired:1b}
execute unless score #kids nh_g matches 1 run summon minecraft:pillager ~-6 ~1 ~-12 {Tags:["nh_t1","nh_trial"],PersistenceRequired:1b}
particle minecraft:poof ~ ~2 ~ 8 1 8 0.05 40
playsound minecraft:entity.evoker.prepare_summon master @a[distance=..100] ~ ~ ~ 1 0.8
