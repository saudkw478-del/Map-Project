kill @e[tag=got_origin]
summon minecraft:marker 270 64 350 {Tags:["got_origin"]}
scoreboard players set #site got_g 2
scoreboard players set #theme got_g 2
scoreboard players set #base got_g 2
scoreboard players set #total got_g 7
tellraw @a [{"text": "[\u0645\u0639\u0631\u0643\u0629] ", "color": "red", "bold": true}, {"text": "\u0648\u064a\u0646\u062a\u0631\u0641\u064a\u0644", "color": "white", "bold": true}]
function got:battle/begin
