execute if score #cs_storms_end got_g matches 3 run scoreboard players remove #held got_g 1
execute unless score #cs_storms_end got_g matches 2 run scoreboard players add #fallen got_g 1
scoreboard players set #cs_storms_end got_g 2
scoreboard players reset #wt_storms_end got_g
title @a title {"text": "\u0633\u0642\u0637\u062a \u0642\u0644\u0639\u0629!", "color": "dark_red", "bold": true}
title @a subtitle {"text": "\u0646\u0647\u0627\u064a\u0629 \u0627\u0644\u0639\u0627\u0635\u0641\u0629 \u0641\u064a \u064a\u062f \u0627\u0644\u0645\u0648\u062a\u0649", "color": "red"}
tellraw @a [{"text": "[\u0627\u0644\u063a\u0631\u0627\u0628] ", "color": "dark_gray", "bold": true}, {"text": "\u0633\u0642\u0637\u062a \u0646\u0647\u0627\u064a\u0629 \u0627\u0644\u0639\u0627\u0635\u0641\u0629! \u0627\u0644\u0623\u0639\u062f\u0627\u0621 \u0623\u0642\u0648\u0649 \u0627\u0644\u0622\u0646. \u064a\u0645\u0643\u0646\u0643\u0645 \u0627\u0633\u062a\u0631\u062f\u0627\u062f\u0647\u0627 \u0628\u0645\u0639\u0631\u0643\u0629 (/trigger got_battle) \u062f\u0627\u062e\u0644\u0647\u0627.", "color": "red", "bold": true}]
playsound minecraft:entity.wither.death master @a
execute if score #cs_winterfell got_g matches 2 run function got:camp/lose
