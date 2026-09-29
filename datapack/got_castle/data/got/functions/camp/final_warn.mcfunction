title @a title {"text": "\u0627\u0644\u0644\u064a\u0644 \u0627\u0644\u0637\u0648\u064a\u0644 \u064a\u0628\u062f\u0623!", "color": "aqua", "bold": true}
title @a subtitle {"text": "\u0627\u0644\u0645\u0639\u0631\u0643\u0629 \u0627\u0644\u0623\u062e\u064a\u0631\u0629 \u0641\u064a \u0648\u064a\u0646\u062a\u0631\u0641\u064a\u0644 \u0628\u0639\u062f \u062f\u0642\u064a\u0642\u062a\u064a\u0646", "color": "red"}
tellraw @a [{"text": "[\u0627\u0644\u063a\u0631\u0627\u0628] ", "color": "dark_gray", "bold": true}, {"text": "\u0645\u0644\u0643 \u0627\u0644\u0644\u064a\u0644 \u0642\u0627\u062f\u0645! \u0627\u062c\u062a\u0645\u0639\u0648\u0627 \u0641\u064a \u0648\u064a\u0646\u062a\u0631\u0641\u064a\u0644 (/trigger got_go set 3)!", "color": "red", "bold": true}]
scoreboard players set #next_site got_g 2
scoreboard players operation #next_t got_g = #camp_t got_g
scoreboard players add #next_t got_g 120
