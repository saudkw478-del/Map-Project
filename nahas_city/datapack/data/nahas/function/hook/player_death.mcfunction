# رسائل لطيفة للأطفال عند السقوط (المنفّذ: اللاعب)
execute store result score #r nh_story run random value 1..8
execute if score #r nh_story matches 1 run tellraw @s {"text":"لا بأس يا بطل! حتى أشجع المغامرين يسقطون. انهض وحاول من جديد.","color":"green"}
execute if score #r nh_story matches 2 run tellraw @s {"text":"الفانوس ما زال يضيء لك. عُدْ أقوى هذه المرّة!","color":"green"}
execute if score #r nh_story matches 3 run tellraw @s {"text":"كلّ سقطةٍ تعلّمنا شيئًا جديدًا. ما الذي تعلّمته الآن؟","color":"green"}
execute if score #r nh_story matches 4 run tellraw @s {"text":"أصحابك ينتظرونك. لا تستسلم!","color":"green"}
execute if score #r nh_story matches 5 run tellraw @s {"text":"الأبطال في الحكايات يعودون دائمًا. وأنت منهم.","color":"green"}
execute if score #r nh_story matches 6 run tellraw @s {"text":"خذ نفسًا عميقًا... ثم ابدأ من جديد بحذر.","color":"green"}
execute if score #r nh_story matches 7 run tellraw @s {"text":"يقول الجنيّ الحكيم: من لا يسقط لا يتعلّم المشي!","color":"green"}
execute if score #r nh_story matches 8 run tellraw @s {"text":"استرح قليلًا، ثم عُدْ إلى الرحلة. المدينة تحتاجك.","color":"green"}
title @s actionbar {"text":"لا بأس... انهض وحاول من جديد","color":"green"}
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.2
