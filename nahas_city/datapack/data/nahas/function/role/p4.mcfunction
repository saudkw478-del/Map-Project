tellraw @s {"text":"خطوة الظل! اختفيت وانتقلت.","color":"dark_purple"}
effect give @s minecraft:invisibility 8 0 true
effect give @s minecraft:speed 8 2 true
particle minecraft:large_smoke ~ ~1 ~ 0.4 0.6 0.4 0.02 30
execute positioned ^ ^ ^8 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~
particle minecraft:large_smoke ~ ~1 ~ 0.4 0.6 0.4 0.02 30
playsound minecraft:entity.enderman.teleport master @a[distance=..20] ~ ~ ~ 1 1
