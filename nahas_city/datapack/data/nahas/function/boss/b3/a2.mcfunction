summon minecraft:vex ~3 ~1 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
particle minecraft:end_rod ~ ~2 ~ 5 1 5 0.05 60
execute unless score #kids nh_g matches 1 as @a[distance=..6] run damage @s 2 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..6] run damage @s 1 minecraft:magic
