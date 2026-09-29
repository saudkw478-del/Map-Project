summon minecraft:vex ~3 ~1 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
summon minecraft:vex ~-3 ~1 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
particle minecraft:end_rod ~ ~2 ~ 6 1 6 0.05 80
effect give @a[distance=..10] minecraft:slowness 2 0 true
execute unless score #kids nh_g matches 1 as @a[distance=..8] run damage @s 3 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..8] run damage @s 1 minecraft:magic
