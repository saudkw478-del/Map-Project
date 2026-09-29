title @a title {"text": "\u0646\u0627\u0631 \u0627\u0644\u0643\u0627\u0647\u0646\u0629 \u0627\u0644\u062d\u0645\u0631\u0627\u0621", "color": "red", "bold": true}
title @a subtitle {"text": "\u0627\u0644\u0645\u0648\u062c\u0629 \u0627\u0644\u0623\u062e\u064a\u0631\u0629! \u0627\u062d\u0645\u0650 \u0627\u0644\u0642\u0644\u0639\u0629!", "color": "gray"}
playsound minecraft:block.bell.use master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/storm_5_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
