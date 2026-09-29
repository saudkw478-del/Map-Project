scoreboard players set #camp got_g 0
function got:util/weather_clear
title @a title {"text": "\u0627\u0646\u062a\u0635\u0631\u062a \u0627\u0644\u0645\u0645\u0627\u0644\u0643!", "color": "gold", "bold": true}
title @a subtitle {"text": "\u0645\u0644\u0643 \u0627\u0644\u0644\u064a\u0644 \u0647\u064f\u0632\u0645 \u0648\u0627\u0646\u062a\u0647\u0649 \u0627\u0644\u0634\u062a\u0627\u0621", "color": "aqua"}
tellraw @a [{"text": "\u0627\u0646\u062a\u0647\u062a \u0627\u0644\u062d\u0645\u0644\u0629 \u0628\u0646\u0635\u0631 \u0639\u0638\u064a\u0645! \u0642\u0644\u0627\u0639 \u0635\u0627\u0645\u062f\u0629: ", "color": "gold", "bold": true}, {"score": {"name": "#held", "objective": "got_g"}, "color": "green"}, {"text": "  \u0642\u0644\u0627\u0639 \u0633\u0642\u0637\u062a: ", "color": "gray"}, {"score": {"name": "#fallen", "objective": "got_g"}, "color": "red"}]
xp add @a 100 levels
scoreboard players add @a got_renown 50
scoreboard players add @a got_gold 100
playsound minecraft:ui.toast.challenge_complete master @a
scoreboard objectives setdisplay sidebar
