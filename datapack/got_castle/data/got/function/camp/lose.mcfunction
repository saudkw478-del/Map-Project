scoreboard players set #camp got_g 0
scoreboard players set #camp_battle got_g 0
kill @e[tag=got_enemy]
scoreboard players set #state got_g 0
function got:util/weather_thunder
title @a title {"text": "\u0627\u0646\u062a\u0635\u0631 \u0627\u0644\u0634\u062a\u0627\u0621", "color": "dark_red", "bold": true}
title @a subtitle {"text": "\u0633\u0642\u0637\u062a \u0648\u064a\u0646\u062a\u0631\u0641\u064a\u0644... \u0644\u0643\u0646 \u064a\u0645\u0643\u0646\u0643\u0645 \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629 \u0645\u0646 \u062c\u062f\u064a\u062f", "color": "gray"}
playsound minecraft:entity.wither.death master @a
scoreboard objectives setdisplay sidebar
