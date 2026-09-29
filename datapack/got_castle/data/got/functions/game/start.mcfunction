execute unless entity @e[tag=got_origin] run return run tellraw @s {"text": "\u0627\u0628\u0646\u0650 \u0627\u0644\u0642\u0644\u0639\u0629 \u0623\u0648\u0644\u064b\u0627: /function got:build", "color": "red"}
scoreboard players set #site got_g 2
scoreboard players set #theme got_g 2
scoreboard players set #base got_g 2
scoreboard players set #total got_g 7
function got:battle/begin
