kill @e[tag=got_origin]
summon minecraft:marker 215 64 1030 {Tags:["got_origin"]}
scoreboard players set #site got_g 7
scoreboard players set #theme got_g 7
scoreboard players set #base got_g 1
scoreboard players set #total got_g 4
tellraw @a [{"text": "[BATTLE] ", "color": "red", "bold": true}, {"text": "Highgarden: Seat of House Tyrell, the garden of the realm.", "color": "white"}]
function got:battle/begin
