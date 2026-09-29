summon minecraft:cave_spider ~3 ~0 ~-3 {Tags:["nh_bm"],PersistenceRequired:1b}
summon minecraft:cave_spider ~-3 ~0 ~3 {Tags:["nh_bm"],PersistenceRequired:1b}
particle minecraft:cloud ~ ~ ~ 4 0.2 4 0.1 40
execute unless score #kids nh_g matches 1 as @a[distance=..6] run damage @s 3 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..6] run damage @s 1 minecraft:magic
