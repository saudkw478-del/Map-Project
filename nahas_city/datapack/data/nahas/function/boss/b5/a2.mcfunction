summon minecraft:vindicator ~6 ~0 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
execute unless score #kids nh_g matches 1 run summon minecraft:vindicator ~-6 ~0 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
particle minecraft:crit ~ ~1 ~ 5 0.5 5 0.2 80
execute unless score #kids nh_g matches 1 as @a[distance=..7] run damage @s 5 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..7] run damage @s 2 minecraft:magic
