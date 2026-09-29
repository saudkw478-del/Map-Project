kill @e[tag=got_origin]
summon minecraft:marker 470 64 1235 {Tags:["got_origin"]}
scoreboard players set #site got_g 9
scoreboard players set #theme got_g 9
scoreboard players set #base got_g 2
scoreboard players set #total got_g 4
tellraw @a [{"text": "[\u0645\u0639\u0631\u0643\u0629] ", "color": "red", "bold": true}, {"text": "\u0633\u0646\u0633\u0628\u064a\u0631", "color": "white", "bold": true}]
function got:battle/begin
