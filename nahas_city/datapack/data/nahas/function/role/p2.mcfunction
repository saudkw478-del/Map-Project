tellraw @s {"text":"صرخة الفارس! أنت وأصدقاؤك أقوى الآن.","color":"red"}
effect give @a[distance=..14] minecraft:strength 15 1 true
effect give @a[distance=..14] minecraft:resistance 15 1 true
particle minecraft:angry_villager ~ ~1.5 ~ 1 0.5 1 0 25
playsound minecraft:entity.ravager.roar master @a[distance=..30] ~ ~ ~ 1 1.2
