summon minecraft:blaze ~4 ~1 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
particle minecraft:lava ~ ~1 ~ 4 1 4 0 30
execute unless score #kids nh_g matches 1 as @a[distance=..6] run damage @s 3 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..6] run damage @s 1 minecraft:magic
