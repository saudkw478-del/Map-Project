execute if score #camp got_g matches 1 run return run tellraw @s {"text": "\u0627\u0644\u062d\u0645\u0644\u0629 \u062c\u0627\u0631\u064a\u0629! \u0623\u0648\u0642\u0641\u0648\u0647\u0627 \u0623\u0648\u0644\u064b\u0627 (/trigger got_start set 4)", "color": "red"}
scoreboard players set #mode got_g 2
scoreboard players set #total_t got_g 3300
tellraw @a [{"text": "\u0628\u062f\u0623\u062a ", "color": "green", "bold": true}, {"text": "\u062d\u0645\u0644\u0629 \u0637\u0648\u064a\u0644\u0629 (55 \u062f\u0642\u064a\u0642\u0629)", "color": "green", "bold": true}]
kill @e[tag=got_enemy]
kill @e[tag=got_wight]
kill @e[tag=got_ally]
scoreboard players set #camp got_g 1
scoreboard players set #camp_t got_g 0
scoreboard players set #min got_g 0
scoreboard players set #winter got_g 0
scoreboard players set #held got_g 0
scoreboard players set #fallen got_g 0
scoreboard players set #next_in got_g 0
scoreboard players set #next_t got_g 0
scoreboard players set #camp_battle got_g 0
scoreboard players set #final got_g 0
scoreboard players set #state got_g 0
scoreboard players set #wave got_g 0
scoreboard players reset #cs_castle_black got_g
scoreboard players reset #cs_winterfell got_g
scoreboard players reset #cs_riverrun got_g
scoreboard players reset #cs_eyrie got_g
scoreboard players reset #cs_kings_landing got_g
scoreboard players reset #cs_casterly_rock got_g
scoreboard players reset #cs_highgarden got_g
scoreboard players reset #cs_storms_end got_g
scoreboard players reset #cs_sunspear got_g
function got:util/rules
function got:util/weather_clear
title @a title {"text": "\u0627\u0644\u0644\u064a\u0644 \u0627\u0644\u0637\u0648\u064a\u0644 \u064a\u0642\u062a\u0631\u0628", "color": "aqua", "bold": true}
title @a subtitle {"text": "\u0627\u062c\u0645\u0639\u0648\u0627 \u0627\u0644\u0645\u0645\u0627\u0644\u0643... \u0627\u0644\u0634\u062a\u0627\u0621 \u0642\u0627\u062f\u0645", "color": "gray"}
playsound minecraft:ambient.cave master @a
function got:hud/update
tellraw @a {"text": "\u0627\u0628\u062f\u0623\u0648\u0627 \u0627\u0644\u0622\u0646: \u0627\u062e\u062a\u0627\u0631\u0648\u0627 \u0628\u064a\u0648\u062a\u0643\u0645 (/trigger got_house) \u0648\u062c\u0647\u0651\u0632\u0648\u0627 \u0639\u062f\u0651\u062a\u0643\u0645 \u0645\u0646 \u0645\u062a\u062c\u0631 \u0627\u0644\u062d\u0631\u0628 (/trigger got_shop).", "color": "yellow"}
