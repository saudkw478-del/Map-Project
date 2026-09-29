# مرحلة جديدة في المعركة (#phase). الحوار يتحوّل من التهديد إلى التعب ليكون مناسبًا للأطفال
function nahas:story/sync
title @s times 5 40 10
title @s title {"text":" "}
title @s subtitle {"text":"الحارس يتغيّر... كونوا حذرين!","color":"yellow"}
playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 2 1
playsound minecraft:block.anvil.land master @s ~ ~ ~ 0.5 0.6
execute if score #phase nh_story matches 1 run tellraw @s [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"أنا حارس هذه المدينة منذ ألف عام. ارجعوا من حيث أتيتم!","color":"red"}]
execute if score #phase nh_story matches 2 run tellraw @s [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"نحاسي لا يتحطّم... هل تظنون أنكم تقدرون؟","color":"red"}]
execute if score #phase nh_story matches 3 run tellraw @s [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"ما هذا الضوء؟ أختامكم... تلمع!","color":"red"}]
execute if score #phase nh_story matches 4 run tellraw @s [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"أشعر بالنحاس يلين... لكنّي لن أستسلم بسهولة!","color":"red"}]
execute if score #phase nh_story matches 5 run tellraw @s [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"يكفي... أنا متعب... متعبٌ جدًا من الحراسة.","color":"red"}]
execute if score #phase nh_story matches 6.. run tellraw @s [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"يكفي... أنا متعب... متعبٌ جدًا من الحراسة.","color":"red"}]
