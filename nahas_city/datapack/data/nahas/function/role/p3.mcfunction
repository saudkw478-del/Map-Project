tellraw @s {"text":"بركة الحكيم! الشفاء للجميع.","color":"aqua"}
effect give @a[distance=..14] minecraft:instant_health 1 1 true
effect give @a[distance=..14] minecraft:regeneration 8 1 true
effect clear @a[distance=..14] minecraft:poison
effect clear @a[distance=..14] minecraft:weakness
effect clear @a[distance=..14] minecraft:slowness
effect clear @a[distance=..14] minecraft:blindness
effect clear @a[distance=..14] minecraft:nausea
effect clear @a[distance=..14] minecraft:wither
particle minecraft:heart ~ ~1.5 ~ 2 0.5 2 0 25
playsound minecraft:block.beacon.power_select master @a[distance=..20] ~ ~ ~ 1 1.5
