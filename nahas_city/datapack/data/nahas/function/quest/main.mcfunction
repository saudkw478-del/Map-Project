function nahas:core/next
execute unless score @s nh_prole matches 1..4 run tellraw @s {"text":"خطوتك الأولى: اختر دورك بـ /trigger nh_role set 1","color":"yellow"}
tellraw @s ["",{"text":"الأختام: ","color":"gold"},{"score":{"name":"#seals","objective":"nh_g"},"color":"yellow"},{"text":" من ٧","color":"gold"}]
execute unless score #t1 nh_g matches 9 run tellraw @s ["",{"text":"- ","color":"gray"},{"text":"معبد الواحة","color":"aqua"},{"text":"  (لم يكتمل)","color":"gray"}]
execute unless score #t2 nh_g matches 9 run tellraw @s ["",{"text":"- ","color":"gray"},{"text":"وادي العقارب","color":"aqua"},{"text":"  (لم يكتمل)","color":"gray"}]
execute unless score #t3 nh_g matches 9 run tellraw @s ["",{"text":"- ","color":"gray"},{"text":"المكتبة الغارقة","color":"aqua"},{"text":"  (لم يكتمل)","color":"gray"}]
execute unless score #t4 nh_g matches 9 run tellraw @s ["",{"text":"- ","color":"gray"},{"text":"قلعة الريح","color":"aqua"},{"text":"  (لم يكتمل)","color":"gray"}]
execute unless score #t5 nh_g matches 9 run tellraw @s ["",{"text":"- ","color":"gray"},{"text":"بحر النجوم (عبر بوابة النجوم)","color":"aqua"},{"text":"  (لم يكتمل)","color":"gray"}]
execute unless score #t6 nh_g matches 9 run tellraw @s ["",{"text":"- ","color":"gray"},{"text":"أرض الجمر (عبر بوابة الجمر)","color":"aqua"},{"text":"  (لم يكتمل)","color":"gray"}]
execute if score #seals nh_g matches 6.. unless score #s7 nh_g matches 1 run tellraw @s ["",{"text":"اذهبوا إلى مدينة النحاس وواجهوا الحارس النحاسي!","color":"gold"}]
execute if score #s7 nh_g matches 1 run tellraw @s ["",{"text":"أنقذتم المدينة! أنتم أبطال القافلة.","color":"green"}]
execute if score #next nh_g matches 0 run tellraw @s {"text":"اذهب أولاً إلى واحة الدلال (س=600 ، ص=1650).","color":"yellow"}
function nahas:items/map_next
