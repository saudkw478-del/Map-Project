kill @e[tag=got_origin]
summon minecraft:marker 140 64 800 {Tags:["got_origin"]}
scoreboard players set #site got_g 6
scoreboard players set #theme got_g 6
scoreboard players set #base got_g 2
scoreboard players set #total got_g 4
tellraw @a [{"text": "[BATTLE] ", "color": "red", "bold": true}, {"text": "Casterly Rock: Seat of House Lannister. A Lannister always pays his debts.", "color": "white"}]
function got:battle/begin
