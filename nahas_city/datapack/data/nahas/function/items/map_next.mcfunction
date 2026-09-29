function nahas:items/astro_update
execute if score #next nh_g matches 0 run tellraw @s ["",{"text":"وجهتك التالية: ","color":"yellow"},{"text":"واحة الدلال","color":"gold","bold":true},{"text":"  (س=600 ، ع=70 ، ص=1650)","color":"gray"}]
execute if score #next nh_g matches 1 run tellraw @s ["",{"text":"وجهتك التالية: ","color":"yellow"},{"text":"معبد الواحة","color":"gold","bold":true},{"text":"  (س=1000 ، ع=70 ، ص=1900)","color":"gray"}]
execute if score #next nh_g matches 2 run tellraw @s ["",{"text":"وجهتك التالية: ","color":"yellow"},{"text":"وادي العقارب","color":"gold","bold":true},{"text":"  (س=1800 ، ع=70 ، ص=1850)","color":"gray"}]
execute if score #next nh_g matches 3 run tellraw @s ["",{"text":"وجهتك التالية: ","color":"yellow"},{"text":"المكتبة الغارقة","color":"gold","bold":true},{"text":"  (س=2100 ، ع=70 ، ص=1300)","color":"gray"}]
execute if score #next nh_g matches 4 run tellraw @s ["",{"text":"وجهتك التالية: ","color":"yellow"},{"text":"قلعة الريح","color":"gold","bold":true},{"text":"  (س=1700 ، ع=120 ، ص=450)","color":"gray"}]
execute if score #next nh_g matches 5 run tellraw @s ["",{"text":"وجهتك التالية: ","color":"yellow"},{"text":"بوابة النجوم","color":"gold","bold":true},{"text":"  (س=1000 ، ع=70 ، ص=350)","color":"gray"}]
execute if score #next nh_g matches 6 run tellraw @s ["",{"text":"وجهتك التالية: ","color":"yellow"},{"text":"بوابة الجمر","color":"gold","bold":true},{"text":"  (س=300 ، ع=70 ، ص=900)","color":"gray"}]
execute if score #next nh_g matches 7 run tellraw @s ["",{"text":"وجهتك التالية: ","color":"yellow"},{"text":"مدينة النحاس","color":"gold","bold":true},{"text":"  (س=1200 ، ع=70 ، ص=1200)","color":"gray"}]
playsound minecraft:item.lodestone_compass.lock master @s ~ ~ ~ 1 1
