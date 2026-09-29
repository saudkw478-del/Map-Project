kill @e[tag=got_origin]
summon minecraft:marker 405 64 880 {Tags:["got_origin"]}
scoreboard players set #site got_g 5
scoreboard players set #theme got_g 5
scoreboard players set #base got_g 2
scoreboard players set #total got_g 5
tellraw @a [{"text": "[\u0645\u0639\u0631\u0643\u0629] ", "color": "red", "bold": true}, {"text": "\u0643\u064a\u0646\u063a\u0632 \u0644\u0627\u0646\u062f\u064a\u0646\u063a", "color": "white", "bold": true}]
function got:battle/begin
