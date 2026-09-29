scoreboard players set @s nh_npccd 120
tellraw @s {"text":"— حجر المعبد —","color":"gold","bold":true}
tellraw @s {"text":"«الختم الأول يُنال بالحكمة لا بالسيف».","color":"white"}
tellraw @s {"text":"حلّوا الألغاز بهدوء، وستنفتح الأبواب.","color":"gray","italic":true}
particle minecraft:enchant ~ ~1 ~ 0.6 0.8 0.6 0.5 40 force @s
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1
execute unless entity @s[tag=nh_lore_3] run function nahas:npc/lore_first
tag @s add nh_lore_3
