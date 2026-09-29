kill @e[tag=got_origin]
summon minecraft:marker 500 124 690 {Tags:["got_origin"]}
scoreboard players set #site got_g 4
scoreboard players set #theme got_g 4
scoreboard players set #base got_g 1
scoreboard players set #total got_g 3
tellraw @a [{"text": "[BATTLE] ", "color": "red", "bold": true}, {"text": "The Eyrie: The impregnable fortress of House Arryn.", "color": "white"}]
function got:battle/begin
