execute unless score #state got_g matches 0 unless score #state got_g matches 4 run return run tellraw @s {"text": "\u0645\u0639\u0631\u0643\u0629 \u062c\u0627\u0631\u064a\u0629 \u0627\u0644\u0622\u0646! (/trigger got_battle set 2 \u0644\u0625\u064a\u0642\u0627\u0641\u0647\u0627)", "color": "red"}
execute if score #camp got_g matches 1 run return run tellraw @s {"text": "\u0627\u0644\u062d\u0645\u0644\u0629 \u062c\u0627\u0631\u064a\u0629: \u0627\u0644\u0645\u0639\u0627\u0631\u0643 \u062a\u0628\u062f\u0623 \u062a\u0644\u0642\u0627\u0626\u064a\u064b\u0627 \u0639\u0646\u062f \u0647\u062c\u0648\u0645 \u0627\u0644\u063a\u0631\u0627\u0628.", "color": "red"}
execute positioned 250 64 236 if entity @s[distance=..80] run return run function got:battle/start_castle_black
execute positioned 270 64 350 if entity @s[distance=..80] run return run function got:battle/start_winterfell
execute positioned 215 64 720 if entity @s[distance=..80] run return run function got:battle/start_riverrun
execute positioned 500 124 690 if entity @s[distance=..80] run return run function got:battle/start_eyrie
execute positioned 405 64 880 if entity @s[distance=..80] run return run function got:battle/start_kings_landing
execute positioned 140 64 800 if entity @s[distance=..80] run return run function got:battle/start_casterly_rock
execute positioned 215 64 1030 if entity @s[distance=..80] run return run function got:battle/start_highgarden
execute positioned 480 64 1005 if entity @s[distance=..80] run return run function got:battle/start_storms_end
execute positioned 470 64 1235 if entity @s[distance=..80] run return run function got:battle/start_sunspear
tellraw @s {"text": "\u0642\u0641 \u062f\u0627\u062e\u0644 \u0642\u0644\u0639\u0629 \u0643\u0628\u0631\u0649 (\u062f\u0627\u062e\u0644 \u0623\u0633\u0648\u0627\u0631\u0647\u0627) \u0644\u062a\u0628\u062f\u0623 \u0645\u0639\u0631\u0643\u062a\u0647\u0627 \u0627\u0644\u062a\u062f\u0631\u064a\u0628\u064a\u0629.", "color": "yellow"}
