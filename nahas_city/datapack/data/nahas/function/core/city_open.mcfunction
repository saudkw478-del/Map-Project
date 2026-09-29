scoreboard players set #city nh_g 1
title @a times 10 80 30
title @a subtitle {"text":"اذهبوا إلى البوابة الجنوبية","color":"yellow"}
title @a title {"text":"انفتحت بوابة المدينة!","color":"gold"}
tellraw @a ["",{"text":"ستة أختام اجتمعت! بوابة مدينة النحاس الجنوبية انفتحت. اذهبوا إلى القصر وواجهوا الحارس.","color":"gold"}]
execute as @a run loot give @s loot nahas:items/key
advancement grant @a only nahas:city_open
forceload add 1200 1350
schedule function nahas:core/gate_force 60t
execute as @a at @s run function nahas:hook/city_open
