tag @s add nh_tester
tellraw @s {"text":"=== اختبار مدينة النحاس ===","color":"gold"}
execute if score #loaded nh_g matches 1 run tellraw @s ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"الحزمة محمّلة (nahas:core/load)","color":"white"}]
execute unless score #loaded nh_g matches 1 run tellraw @s ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"الحزمة غير محمّلة، جرّب /reload","color":"white"}]
execute store result score #n nh_g run scoreboard objectives list
execute if score #n nh_g matches 10.. run tellraw @s ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"لوحات النقاط موجودة","color":"white"}]
execute unless score #n nh_g matches 10.. run tellraw @s ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لوحات النقاط ناقصة","color":"white"}]
execute store result score #n nh_g run loot spawn ~ ~ ~ loot nahas:items/seal_1
execute if score #n nh_g matches 1.. run tellraw @s ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"جداول الغنائم تعمل (ختم النحاس)","color":"white"}]
execute unless score #n nh_g matches 1.. run tellraw @s ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"جدول الغنائم لا يعمل","color":"white"}]
kill @e[type=minecraft:item,distance=..3,nbt={Item:{id:"minecraft:copper_ingot"}}]
execute store result score #n nh_g run loot spawn ~ ~ ~ loot nahas:kit/start
execute if score #n nh_g matches 1.. run tellraw @s ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"حقيبة البداية تعمل","color":"white"}]
execute unless score #n nh_g matches 1.. run tellraw @s ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"حقيبة البداية لا تعمل","color":"white"}]
kill @e[type=minecraft:item,distance=..3]
execute store success score #d1 nh_g in nahas:star_sea run forceload add 600 600
execute store success score #d2 nh_g in nahas:ember run forceload add 500 500
execute if score #d1 nh_g matches 1 run tellraw @s ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"البُعد nahas:star_sea موجود","color":"white"}]
execute unless score #d1 nh_g matches 1 run tellraw @s ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"البُعد nahas:star_sea غير موجود","color":"white"}]
execute if score #d2 nh_g matches 1 run tellraw @s ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"البُعد nahas:ember موجود","color":"white"}]
execute unless score #d2 nh_g matches 1 run tellraw @s ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"البُعد nahas:ember غير موجود","color":"white"}]
execute store success score #h1 nh_g run function nahas:hook/tick
execute store success score #h2 nh_g run function nahas:ambient/second
execute store success score #h3 nh_g run function nahas:npc/second
execute unless score #h1 nh_g matches 0 unless score #h2 nh_g matches 0 unless score #h3 nh_g matches 0 run tellraw @s ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"دوال القصة (hook/ambient/npc) موجودة","color":"white"}]
execute if score #h1 nh_g matches 0 run tellraw @s ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"hook/tick غير موجودة","color":"white"}]
execute if score #h2 nh_g matches 0 run tellraw @s ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"ambient/second غير موجودة","color":"white"}]
execute if score #h3 nh_g matches 0 run tellraw @s ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"npc/second غير موجودة","color":"white"}]
tellraw @s {"text":"جارٍ فحص عالم الخريطة (٣ ثوانٍ)...","color":"gray"}
execute in minecraft:overworld run forceload add 300 2050
execute in minecraft:overworld run forceload add 600 1650
execute in minecraft:overworld run forceload add 1000 1900
execute in minecraft:overworld run forceload add 1800 1850
execute in minecraft:overworld run forceload add 2100 1300
execute in minecraft:overworld run forceload add 1700 450
execute in minecraft:overworld run forceload add 1000 350
execute in minecraft:overworld run forceload add 300 900
execute in minecraft:overworld run forceload add 1200 1200
schedule function nahas:selftest2 60t
