kill @e[tag=got_origin]
summon minecraft:marker 480 64 1005 {Tags:["got_origin"]}
scoreboard players set #site got_g 8
scoreboard players set #theme got_g 8
scoreboard players set #base got_g 2
scoreboard players set #total got_g 5
tellraw @a [{"text": "[BATTLE] ", "color": "red", "bold": true}, {"text": "Storm's End: Seat of House Baratheon. Ours is the Fury.", "color": "white"}]
function got:battle/begin
