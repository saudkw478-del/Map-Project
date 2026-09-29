kill @e[tag=got_origin]
summon minecraft:marker 250 64 236 {Tags:["got_origin"]}
scoreboard players set #site got_g 1
scoreboard players set #theme got_g 1
scoreboard players set #base got_g 0
scoreboard players set #total got_g 4
tellraw @a [{"text": "[\u0645\u0639\u0631\u0643\u0629] ", "color": "red", "bold": true}, {"text": "\u0627\u0644\u0642\u0644\u0639\u0629 \u0627\u0644\u0633\u0648\u062f\u0627\u0621", "color": "white", "bold": true}]
function got:battle/begin
