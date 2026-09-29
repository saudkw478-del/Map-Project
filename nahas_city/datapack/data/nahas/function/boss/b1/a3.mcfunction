summon minecraft:cave_spider ~4 ~0 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
summon minecraft:cave_spider ~-4 ~0 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
effect give @a[distance=..8] minecraft:slowness 3 0 true
particle minecraft:smoke ~ ~1 ~ 3 0.5 3 0.05 40
execute unless score #kids nh_g matches 1 as @a[distance=..7] run damage @s 4 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..7] run damage @s 2 minecraft:magic
