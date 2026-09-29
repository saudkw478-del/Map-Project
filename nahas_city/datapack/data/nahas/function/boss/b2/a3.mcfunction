summon minecraft:vex ~2 ~1 ~2 {Tags:["nh_bm"],PersistenceRequired:1b}
summon minecraft:vex ~-2 ~1 ~-2 {Tags:["nh_bm"],PersistenceRequired:1b}
effect give @a[distance=..16] minecraft:levitation 2 0 true
effect give @a[distance=..16] minecraft:slow_falling 8 0 true
execute unless score #kids nh_g matches 1 as @a[distance=..8] run damage @s 3 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..8] run damage @s 1 minecraft:magic
