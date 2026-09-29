# ختم جديد (المنفّذ: اللاعب الذي ناله؛ nh_lastseal = رقم الختم)
function nahas:story/sync
title @a times 10 80 30
title @a subtitle [{"selector":"@s","color":"yellow"},{"text":" نال الختم رقم ","color":"yellow"},{"score":{"name":"@s","objective":"nh_lastseal"},"color":"gold"}]
title @a title {"text":"ختم من النحاس!","color":"gold","bold":true}
execute at @s run function nahas:fx/seal_burst
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 1 1
execute if score @s nh_lastseal matches 1 run tellraw @a [{"text":"✦ ","color":"gold"},{"text":"ختم الواحة: ","color":"gold","bold":true},{"text":"في معبد الواحة ذكّرنا الحكماءُ أنّ الصبر مفتاح كل باب.","color":"yellow"}]
execute if score @s nh_lastseal matches 2 run tellraw @a [{"text":"✦ ","color":"gold"},{"text":"ختم العقرب: ","color":"gold","bold":true},{"text":"ملكة العقارب تنحني لمن جمع الشجاعة مع الحيلة.","color":"yellow"}]
execute if score @s nh_lastseal matches 3 run tellraw @a [{"text":"✦ ","color":"gold"},{"text":"ختم الحكمة: ","color":"gold","bold":true},{"text":"المكتبة الغارقة سلّمت سرّها لمن شارك العلم مع أصحابه.","color":"yellow"}]
execute if score @s nh_lastseal matches 4 run tellraw @a [{"text":"✦ ","color":"gold"},{"text":"ختم الريح: ","color":"gold","bold":true},{"text":"الريح حملتكم إلى القمّة، فقلعتها استسلمت لخفّتكم.","color":"yellow"}]
execute if score @s nh_lastseal matches 5 run tellraw @a [{"text":"✦ ","color":"gold"},{"text":"ختم النجوم: ","color":"gold","bold":true},{"text":"النجوم رقصت فرحًا وأضاءت طريقًا جديدًا.","color":"yellow"}]
execute if score @s nh_lastseal matches 6 run tellraw @a [{"text":"✦ ","color":"gold"},{"text":"ختم الجمر: ","color":"gold","bold":true},{"text":"الجمر انطفأ غضبه، وبقي دفؤه يرافقكم.","color":"yellow"}]
execute if score @s nh_lastseal matches 7 run tellraw @a [{"text":"✦ ","color":"gold"},{"text":"ختم النحاس: ","color":"gold","bold":true},{"text":"اكتملت الأختام! انكسر سحر النحاس الأخير.","color":"yellow"}]
execute if score #seals nh_story matches 0 run tellraw @a [{"text":"الأختام: ","color":"gray"},{"text":"☆☆☆☆☆☆☆","color":"gold"},{"text":" (0/7)","color":"gray"}]
execute if score #seals nh_story matches 1 run tellraw @a [{"text":"الأختام: ","color":"gray"},{"text":"★☆☆☆☆☆☆","color":"gold"},{"text":" (1/7)","color":"gray"}]
execute if score #seals nh_story matches 2 run tellraw @a [{"text":"الأختام: ","color":"gray"},{"text":"★★☆☆☆☆☆","color":"gold"},{"text":" (2/7)","color":"gray"}]
execute if score #seals nh_story matches 3 run tellraw @a [{"text":"الأختام: ","color":"gray"},{"text":"★★★☆☆☆☆","color":"gold"},{"text":" (3/7)","color":"gray"}]
execute if score #seals nh_story matches 4 run tellraw @a [{"text":"الأختام: ","color":"gray"},{"text":"★★★★☆☆☆","color":"gold"},{"text":" (4/7)","color":"gray"}]
execute if score #seals nh_story matches 5 run tellraw @a [{"text":"الأختام: ","color":"gray"},{"text":"★★★★★☆☆","color":"gold"},{"text":" (5/7)","color":"gray"}]
execute if score #seals nh_story matches 6 run tellraw @a [{"text":"الأختام: ","color":"gray"},{"text":"★★★★★★☆","color":"gold"},{"text":" (6/7)","color":"gray"}]
execute if score #seals nh_story matches 7 run tellraw @a [{"text":"الأختام: ","color":"gray"},{"text":"★★★★★★★","color":"gold"},{"text":" (7/7)","color":"gray"}]
