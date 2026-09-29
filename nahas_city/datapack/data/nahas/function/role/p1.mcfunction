tellraw @s {"text":"نداء الاستكشاف! الوحوش القريبة تتوهج الآن.","color":"green"}
effect give @e[distance=..60,type=!minecraft:player] minecraft:glowing 15 0 true
effect give @s minecraft:speed 10 2 true
effect give @s minecraft:jump_boost 10 1 true
particle minecraft:happy_villager ~ ~1 ~ 1 1 1 0 40
playsound minecraft:entity.evoker.prepare_summon master @a[distance=..20] ~ ~ ~ 1 1.3
function nahas:items/astro_update
