summon minecraft:husk ~6 ~0 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
summon minecraft:husk ~-6 ~0 ~0 {Tags:["nh_bm"],PersistenceRequired:1b}
execute unless score #kids nh_g matches 1 run summon minecraft:pillager ~0 ~0 ~6 {Tags:["nh_bm"],PersistenceRequired:1b}
effect give @a[distance=..9] minecraft:slowness 2 0 true
particle minecraft:explosion ~ ~1 ~ 4 0.5 4 0 5
execute unless score #kids nh_g matches 1 as @a[distance=..8] run damage @s 6 minecraft:magic
execute if score #kids nh_g matches 1 as @a[distance=..8] run damage @s 3 minecraft:magic
