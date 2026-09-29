scoreboard players set @s nh_npccd 10
tellraw @s {"text":"— حجر الريح —","color":"gold","bold":true}
tellraw @s {"text":"«من يصعد بلا خوف تحمله الريح».","color":"white"}
tellraw @s {"text":"لا تنظروا إلى الأسفل، انظروا إلى القفزة التالية.","color":"gray","italic":true}
particle minecraft:enchant ~ ~1 ~ 0.6 0.8 0.6 0.5 40 force @s
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1
execute unless entity @s[tag=nh_lore_6] run function nahas:npc/lore_first
tag @s add nh_lore_6
