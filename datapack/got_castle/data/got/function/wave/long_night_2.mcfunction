title @a title {"text": "\u0627\u0644\u0645\u0648\u062c\u0629 2 - \u0645\u063a\u064a\u0631\u0648\u0646 \u0645\u0646 \u0648\u0631\u0627\u0621 \u0627\u0644\u062c\u062f\u0627\u0631", "color": "red", "bold": true}
title @a subtitle {"text": "\u0627\u0644\u0623\u0639\u062f\u0627\u0621 \u064a\u062a\u062c\u0645\u0639\u0648\u0646 \u0623\u0645\u0627\u0645 \u0627\u0644\u0628\u0648\u0627\u0628\u0629 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629!", "color": "gray"}
playsound minecraft:block.bell.use master @a
execute at @e[tag=got_origin,limit=1] run function got:wave/long_night_2_spawn
execute as @e[tag=got_new] at @s run function got:game/equip
