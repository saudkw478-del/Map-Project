scoreboard players set #state got_g 4
title @a title {"text": "VICTORY!", "color": "gold", "bold": true}
title @a subtitle {"text": "The Night King has fallen. The realm is saved!", "color": "aqua"}
effect give @a minecraft:regeneration 30 2 true
xp add @a 30 levels
loot give @a loot got:reward/trophy
playsound minecraft:ui.toast.challenge_complete master @a
tellraw @a {"text": "You can stop with /function got:game/stop or start again with /function got:game/start", "color": "gray"}
