kill @e[tag=got_origin]
summon minecraft:marker 235 64 770 {Tags:["got_origin"]}
scoreboard players set #site got_g 3
scoreboard players set #theme got_g 3
scoreboard players set #base got_g 1
scoreboard players set #total got_g 4
tellraw @a [{"text": "[BATTLE] ", "color": "red", "bold": true}, {"text": "Riverrun: Seat of House Tully at the fork of the rivers.", "color": "white"}]
function got:battle/begin
