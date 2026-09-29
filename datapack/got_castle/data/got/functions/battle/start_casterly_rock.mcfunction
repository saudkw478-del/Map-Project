kill @e[tag=got_origin]
summon minecraft:marker 140 64 800 {Tags:["got_origin"]}
scoreboard players set #site got_g 6
scoreboard players set #theme got_g 6
scoreboard players set #base got_g 2
scoreboard players set #total got_g 4
tellraw @a [{"text": "[\u0645\u0639\u0631\u0643\u0629] ", "color": "red", "bold": true}, {"text": "\u0635\u062e\u0631\u0629 \u0643\u0627\u0633\u062a\u0644\u064a", "color": "white", "bold": true}]
function got:battle/begin
