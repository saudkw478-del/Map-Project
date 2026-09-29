execute at @e[tag=got_origin,limit=1] run function got:build/s7_courtyard_a
execute at @e[tag=got_origin,limit=1] run forceload remove ~-60 ~-60 ~60 ~60
function got:util/rules
tellraw @a [{"text": "\u0627\u0644\u0642\u0644\u0639\u0629 \u062c\u0627\u0647\u0632\u0629! ", "color": "green", "bold": true}, {"text": "\u0627\u0644\u0623\u0633\u0644\u062d\u0629 \u0641\u064a \u0645\u062e\u0632\u0646 \u0627\u0644\u0623\u0633\u0644\u062d\u0629 (\u0627\u0644\u0641\u0646\u0627\u0621 \u0627\u0644\u063a\u0631\u0628\u064a). \u0644\u0644\u0628\u062f\u0621: /function got:game/start", "color": "white"}]
