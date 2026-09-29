kill @e[tag=got_origin]
summon minecraft:marker 405 64 880 {Tags:["got_origin"]}
scoreboard players set #site got_g 5
scoreboard players set #theme got_g 5
scoreboard players set #base got_g 2
scoreboard players set #total got_g 5
tellraw @a [{"text": "[BATTLE] ", "color": "red", "bold": true}, {"text": "King's Landing: The Red Keep and the Iron Throne.", "color": "white"}]
function got:battle/begin
