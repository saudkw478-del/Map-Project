execute in minecraft:overworld if block 300 70 2050 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا أرض عند معسكر القافلة المهجور","color":"white"}]
execute in minecraft:overworld unless block 300 70 2050 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"أرض موجودة عند معسكر القافلة المهجور","color":"white"}]
execute in minecraft:overworld run forceload remove 300 2050
execute in minecraft:overworld if block 600 70 1650 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا أرض عند واحة الدلال","color":"white"}]
execute in minecraft:overworld unless block 600 70 1650 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"أرض موجودة عند واحة الدلال","color":"white"}]
execute in minecraft:overworld run forceload remove 600 1650
execute in minecraft:overworld if block 1000 70 1900 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا أرض عند معبد الواحة","color":"white"}]
execute in minecraft:overworld unless block 1000 70 1900 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"أرض موجودة عند معبد الواحة","color":"white"}]
execute in minecraft:overworld run forceload remove 1000 1900
execute in minecraft:overworld if block 1800 70 1850 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا أرض عند وادي العقارب","color":"white"}]
execute in minecraft:overworld unless block 1800 70 1850 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"أرض موجودة عند وادي العقارب","color":"white"}]
execute in minecraft:overworld run forceload remove 1800 1850
execute in minecraft:overworld if block 2100 70 1300 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا أرض عند المكتبة الغارقة","color":"white"}]
execute in minecraft:overworld unless block 2100 70 1300 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"أرض موجودة عند المكتبة الغارقة","color":"white"}]
execute in minecraft:overworld run forceload remove 2100 1300
execute in minecraft:overworld if block 1700 120 450 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا أرض عند قلعة الريح","color":"white"}]
execute in minecraft:overworld unless block 1700 120 450 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"أرض موجودة عند قلعة الريح","color":"white"}]
execute in minecraft:overworld run forceload remove 1700 450
execute in minecraft:overworld if block 1000 70 350 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا أرض عند بوابة النجوم","color":"white"}]
execute in minecraft:overworld unless block 1000 70 350 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"أرض موجودة عند بوابة النجوم","color":"white"}]
execute in minecraft:overworld run forceload remove 1000 350
execute in minecraft:overworld if block 300 70 900 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا أرض عند بوابة الجمر","color":"white"}]
execute in minecraft:overworld unless block 300 70 900 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"أرض موجودة عند بوابة الجمر","color":"white"}]
execute in minecraft:overworld run forceload remove 300 900
execute in minecraft:overworld if block 1200 70 1200 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا أرض عند مدينة النحاس","color":"white"}]
execute in minecraft:overworld unless block 1200 70 1200 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"أرض موجودة عند مدينة النحاس","color":"white"}]
execute in minecraft:overworld run forceload remove 1200 1200
execute in nahas:star_sea unless block 600 100 600 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"جزيرة الوصول في بحر النجوم موجودة","color":"white"}]
execute in nahas:star_sea if block 600 100 600 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا جزيرة عند (600،100،600) في بحر النجوم","color":"white"}]
execute in nahas:ember unless block 500 64 500 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[نجح] ","color":"green","bold":true},{"text":"منصة الوصول في أرض الجمر موجودة","color":"white"}]
execute in nahas:ember if block 500 64 500 minecraft:air run tellraw @a[tag=nh_tester] ["",{"text":"[فشل] ","color":"red","bold":true},{"text":"لا منصة عند (500،64،500) في أرض الجمر","color":"white"}]
execute in nahas:star_sea run forceload remove 600 600
execute in nahas:ember run forceload remove 500 500
tellraw @a[tag=nh_tester] {"text":"=== انتهى الاختبار ===","color":"gold"}
tag @a remove nh_tester
