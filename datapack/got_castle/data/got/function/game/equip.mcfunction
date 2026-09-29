execute if entity @s[type=minecraft:zombie] run function got:wave/gear
execute if entity @s[type=minecraft:husk] run function got:wave/gear
execute if entity @s[type=minecraft:skeleton] run function got:wave/gear
execute if entity @s[type=minecraft:stray] run function got:wave/gear
execute if entity @s[type=minecraft:vindicator] run function got:wave/gear
team join got_enemies @s
tag @s remove got_new
