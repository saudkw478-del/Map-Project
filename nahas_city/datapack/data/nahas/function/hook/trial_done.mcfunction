# اكتملت تجربة
function nahas:story/sync
title @a times 10 60 20
title @a subtitle {"text":"أحسنتم يا أبطال!","color":"yellow"}
title @a title {"text":"اكتملت التجربة","color":"green","bold":true}
execute as @a at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.8 1.1
tellraw @a [{"text":"✔ ","color":"green"},{"text":"اكتملت التجربة! الأختام حتى الآن: ","color":"white"},{"score":{"name":"#seals","objective":"nh_story"},"color":"gold"},{"text":" من 7.","color":"white"}]
