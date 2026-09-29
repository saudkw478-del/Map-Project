scoreboard players set #s10 got_g 0
execute if score #winter got_g matches ..19 run return 0
execute as @a[tag=!got_h_stark,gamemode=!spectator,gamemode=!creative] at @s if biome ~ ~ ~ minecraft:snowy_taiga unless entity @e[type=minecraft:marker,tag=got_warm,distance=..70] unless items entity @s weapon.* minecraft:torch run function got:cold/bite
execute as @a[tag=!got_h_stark,gamemode=!spectator,gamemode=!creative] at @s if biome ~ ~ ~ minecraft:ice_spikes unless entity @e[type=minecraft:marker,tag=got_warm,distance=..70] unless items entity @s weapon.* minecraft:torch run function got:cold/bite
