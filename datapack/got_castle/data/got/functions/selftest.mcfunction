tellraw @s {"text":"--- Game of Thrones Castle self-test ---","color":"gold"}
execute if score #state got_g matches 0.. run tellraw @s {"text":"[OK] scoreboard/state ready","color":"green"}
execute unless score #state got_g matches 0.. run tellraw @s {"text":"[..] game not started yet (normal before /function got:game/start)","color":"yellow"}
execute if entity @e[tag=got_origin] run tellraw @s {"text":"[OK] castle origin marker exists (castle was built)","color":"green"}
execute unless entity @e[tag=got_origin] run tellraw @s {"text":"[..] castle not built yet: run /function got:build","color":"yellow"}
execute if entity @e[tag=got_gate] run tellraw @s {"text":"[OK] castle build finished (gate marker exists)","color":"green"}
execute at @e[tag=got_origin,limit=1] if block ~ ~ ~4 red_carpet run tellraw @s {"text":"[OK] throne room carpet found","color":"green"}
execute at @e[tag=got_origin,limit=1] if block ~ ~3 ~-19 polished_blackstone_brick_stairs run tellraw @s {"text":"[OK] Iron Throne found","color":"green"}
execute at @e[tag=got_origin,limit=1] if block ~-36 ~ ~21 chest run tellraw @s {"text":"[OK] armory chests found","color":"green"}
execute store success score #ok got_g run loot give @s loot got:kit/weapons
execute if score #ok got_g matches 1 run tellraw @s {"text":"[OK] loot tables work (you just got a Valyrian sword)","color":"green"}
execute unless score #ok got_g matches 1 run tellraw @s {"text":"[FAIL] loot tables did not load - send the log to the developer","color":"red"}
