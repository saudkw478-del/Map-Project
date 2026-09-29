kill @e[tag=got_origin]
summon minecraft:marker 270 64 350 {Tags:["got_origin"]}
scoreboard players set #site got_g 2
scoreboard players set #theme got_g 2
scoreboard players set #base got_g 2
scoreboard players set #total got_g 7
tellraw @a [{"text": "[BATTLE] ", "color": "red", "bold": true}, {"text": "Winterfell: Seat of House Stark. Stand against the Long Night.", "color": "white"}]
function got:battle/begin
