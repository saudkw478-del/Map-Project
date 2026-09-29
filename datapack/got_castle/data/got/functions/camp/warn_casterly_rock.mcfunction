scoreboard players set #next_site got_g 6
scoreboard players operation #next_t got_g = #camp_t got_g
scoreboard players add #next_t got_g 120
title @a title {"text": "\u063a\u0631\u0627\u0628 \u0639\u0627\u062c\u0644!", "color": "dark_gray", "bold": true}
title @a subtitle {"text": "\u0635\u062e\u0631\u0629 \u0643\u0627\u0633\u062a\u0644\u064a \u0633\u062a\u064f\u0647\u0627\u062c\u064e\u0645 \u0628\u0639\u062f \u062f\u0642\u064a\u0642\u062a\u064a\u0646", "color": "red"}
tellraw @a [{"text": "[\u0627\u0644\u063a\u0631\u0627\u0628] ", "color": "dark_gray", "bold": true}, {"text": "\u0627\u0644\u062c\u064a\u0634 \u0627\u0644\u0645\u064a\u062a \u064a\u0642\u062a\u0631\u0628 \u0645\u0646 \u0635\u062e\u0631\u0629 \u0643\u0627\u0633\u062a\u0644\u064a! \u0627\u0630\u0647\u0628\u0648\u0627 \u0625\u0644\u064a\u0647\u0627 \u0628\u0640 /trigger got_go \u0648\u0627\u062d\u0645\u0648\u0647\u0627.", "color": "red", "bold": true}]
playsound minecraft:entity.parrot.ambient master @a
