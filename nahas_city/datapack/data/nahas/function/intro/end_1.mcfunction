function nahas:fx/lantern_off
execute in minecraft:overworld run tp @s 300.00 71.00 2053.00 facing 300 73 2050
tellraw @s [{"text":"استيقظتم في معسكر القافلة المهجور. ","color":"yellow"},{"text":"ابحثوا عن صندوق الفانوس، ثم اتّجهوا إلى واحة الدلال.","color":"white"}]
tellraw @s [{"text":"اكتب ","color":"gray"},{"text":"/trigger nh_help","color":"green"},{"text":" للمساعدة.","color":"gray"}]
spawnpoint @s 300 71 2053
