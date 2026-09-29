tag @s add got_me
playsound minecraft:entity.wolf.growl master @a[distance=..40]
particle minecraft:cloud ~ ~1 ~ 1.5 0.6 1.5 0.05 60 force
effect give @a[distance=..20] minecraft:speed 15 1 true
effect give @a[distance=..20] minecraft:strength 15 0 true
title @a[distance=..20] actionbar {"text": "\u0639\u0648\u0649 \u0627\u0644\u0630\u0626\u0628!", "color": "white"}
scoreboard players set @s got_pcd 60
tag @s remove got_me
