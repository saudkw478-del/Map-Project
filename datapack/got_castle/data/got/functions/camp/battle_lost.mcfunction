kill @e[tag=got_enemy]
scoreboard players set #state got_g 0
scoreboard players set #camp_battle got_g 0
title @a title {"text": "\u0641\u0634\u0644\u062a\u0645 \u0641\u064a \u0627\u0644\u062f\u0641\u0627\u0639!", "color": "dark_red", "bold": true}
title @a subtitle {"text": "\u0627\u0644\u0623\u0639\u062f\u0627\u0621 \u0627\u062c\u062a\u0627\u062d\u0648\u0627 \u0627\u0644\u0642\u0644\u0639\u0629", "color": "red"}
execute if score #site got_g matches 1 run function got:camp/fell_castle_black
execute if score #site got_g matches 2 run function got:camp/fell_winterfell
execute if score #site got_g matches 3 run function got:camp/fell_riverrun
execute if score #site got_g matches 4 run function got:camp/fell_eyrie
execute if score #site got_g matches 5 run function got:camp/fell_kings_landing
execute if score #site got_g matches 6 run function got:camp/fell_casterly_rock
execute if score #site got_g matches 7 run function got:camp/fell_highgarden
execute if score #site got_g matches 8 run function got:camp/fell_storms_end
execute if score #site got_g matches 9 run function got:camp/fell_sunspear
