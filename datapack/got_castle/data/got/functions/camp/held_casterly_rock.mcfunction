execute if score #cs_casterly_rock got_g matches 2 run scoreboard players remove #fallen got_g 1
execute unless score #cs_casterly_rock got_g matches 3 run scoreboard players add #held got_g 1
scoreboard players reset #wt_casterly_rock got_g
scoreboard players set #cs_casterly_rock got_g 3
tellraw @a [{"text": "[\u0627\u0644\u063a\u0631\u0627\u0628] ", "color": "dark_gray", "bold": true}, {"text": "\u0635\u062e\u0631\u0629 \u0643\u0627\u0633\u062a\u0644\u064a \u0635\u0627\u0645\u062f\u0629! \u0633\u062a\u0645\u062f\u0651\u0643\u0645 \u0628\u062d\u0644\u0641\u0627\u0621 \u0641\u064a \u0627\u0644\u0645\u0639\u0631\u0643\u0629 \u0627\u0644\u0623\u062e\u064a\u0631\u0629.", "color": "green", "bold": true}]
