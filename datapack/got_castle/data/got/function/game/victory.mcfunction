scoreboard players set #state got_g 4
title @a title {"text": "\u0627\u0644\u0646\u0635\u0631!", "color": "gold", "bold": true}
title @a subtitle {"text": "\u0627\u0644\u0642\u0644\u0639\u0629 \u0635\u0627\u0645\u062f\u0629!", "color": "aqua"}
effect give @a minecraft:regeneration 30 2 true
xp add @a 30 levels
loot give @a loot got:reward/trophy
scoreboard players add @a got_gold 15
scoreboard players add @a[tag=got_h_lannister] got_gold 8
scoreboard players add @a got_renown 10
playsound minecraft:ui.toast.challenge_complete master @a
execute if score #camp_battle got_g matches 0 run tellraw @a {"text": "\u0627\u0646\u062a\u0635\u0631\u062a\u0645! \u0627\u0628\u062f\u0623\u0648\u0627 \u0645\u0639\u0631\u0643\u0629 \u0623\u062e\u0631\u0649 \u0628\u0640 /trigger got_battle \u0623\u0648 \u0627\u0628\u062f\u0623\u0648\u0627 \u0627\u0644\u062d\u0645\u0644\u0629 \u0628\u0640 /trigger got_start.", "color": "gray"}
execute if score #camp_battle got_g matches 1 run function got:camp/battle_won
