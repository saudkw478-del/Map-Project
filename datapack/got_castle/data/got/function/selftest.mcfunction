tellraw @s {"text":"--- Game of Thrones self-test ---","color":"gold"}
execute if score #state got_g matches 0.. run tellraw @s {"text":"[OK] scoreboard ready (datapack loaded)","color":"green"}
execute unless score #state got_g matches 0.. run tellraw @s {"text":"[FAIL] datapack not loaded - is it enabled? (/datapack list)","color":"red"}
execute store success score #ok got_g run loot give @s loot got:kit/weapons
execute if score #ok got_g matches 1 run tellraw @s {"text":"[OK] loot tables work (you just got a Valyrian sword)","color":"green"}
execute unless score #ok got_g matches 1 run tellraw @s {"text":"[FAIL] loot tables did not load","color":"red"}
execute if biome ~ ~ ~ minecraft:snowy_taiga run tellraw @s {"text":"[OK] you are in the North biome (world map loaded)","color":"green"}
execute if block 234 64 371 minecraft:chest run tellraw @s {"text":"[OK] Winterfell armory chest found","color":"green"}
execute if block 270 67 331 minecraft:dark_oak_stairs run tellraw @s {"text":"[OK] Winterfell high seat found","color":"green"}
execute unless block 234 64 371 minecraft:chest run tellraw @s {"text":"[..] Winterfell armory not found here (fine if you are far from Winterfell or in a custom world)","color":"yellow"}
execute if entity @e[tag=got_origin] run tellraw @s {"text":"[OK] a castle battle marker exists (custom-built castle or battle started)","color":"green"}
