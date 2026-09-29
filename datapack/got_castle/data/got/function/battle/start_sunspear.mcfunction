kill @e[tag=got_origin]
summon minecraft:marker 470 64 1235 {Tags:["got_origin"]}
scoreboard players set #site got_g 9
scoreboard players set #theme got_g 9
scoreboard players set #base got_g 2
scoreboard players set #total got_g 4
tellraw @a [{"text": "[BATTLE] ", "color": "red", "bold": true}, {"text": "Sunspear: Seat of House Martell. Unbowed, unbent, unbroken.", "color": "white"}]
function got:battle/begin
