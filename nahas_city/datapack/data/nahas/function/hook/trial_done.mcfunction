# اكتملت تجربة
function nahas:story/sync
title @s times 10 60 20
title @s subtitle {"text":"أحسنتم يا أبطال!","color":"yellow"}
title @s title {"text":"اكتملت التجربة","color":"green","bold":true}
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.8 1.1
tellraw @s [{"text":"✔ ","color":"green"},{"text":"اكتملت التجربة! الأختام حتى الآن: ","color":"white"},{"score":{"name":"#seals","objective":"nh_story"},"color":"gold"},{"text":" من 7.","color":"white"}]
