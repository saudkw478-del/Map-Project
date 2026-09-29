particle minecraft:crit ~ ~1 ~ 4 0.5 4 0.2 60
execute unless score #kids nh_g matches 1 as @a[distance=..6] run damage @s 4 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..6] run damage @s 2 minecraft:magic
