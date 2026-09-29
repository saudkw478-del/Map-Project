execute unless entity @e[tag=got_origin] run return run tellraw @s {"text": "Build the castle first: /function got:build", "color": "red"}
scoreboard players set #site got_g 2
scoreboard players set #theme got_g 2
scoreboard players set #base got_g 2
scoreboard players set #total got_g 7
function got:battle/begin
