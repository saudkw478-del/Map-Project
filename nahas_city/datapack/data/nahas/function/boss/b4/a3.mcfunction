summon minecraft:blaze ~4 ~1 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
summon minecraft:blaze ~-4 ~1 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
particle minecraft:lava ~ ~1 ~ 5 1 5 0 50
execute unless score #kids nh_g matches 1 as @a[distance=..8] run damage @s 4 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..8] run damage @s 2 minecraft:magic
