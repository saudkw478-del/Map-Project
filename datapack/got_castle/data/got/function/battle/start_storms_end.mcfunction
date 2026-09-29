kill @e[tag=got_origin]
summon minecraft:marker 480 64 1005 {Tags:["got_origin"]}
scoreboard players set #site got_g 8
scoreboard players set #theme got_g 8
scoreboard players set #base got_g 2
scoreboard players set #total got_g 5
tellraw @a [{"text": "[\u0645\u0639\u0631\u0643\u0629] ", "color": "red", "bold": true}, {"text": "\u0646\u0647\u0627\u064a\u0629 \u0627\u0644\u0639\u0627\u0635\u0641\u0629", "color": "white", "bold": true}]
function got:battle/begin
