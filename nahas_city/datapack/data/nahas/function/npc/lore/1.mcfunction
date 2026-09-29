scoreboard players set @s nh_npccd 10
tellraw @s {"text":"— حجر القافلة —","color":"gold","bold":true}
tellraw @s {"text":"نُقش على الحجر: «مرّت من هنا قافلةٌ بلا دليل، فوجدت فانوسًا يعرف الطريق».","color":"white"}
tellraw @s {"text":"وتحتها كلمة صغيرة: ابقوا معًا.","color":"gray","italic":true}
particle minecraft:enchant ~ ~1 ~ 0.6 0.8 0.6 0.5 40 force @s
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1
execute unless entity @s[tag=nh_lore_1] run function nahas:npc/lore_first
tag @s add nh_lore_1
