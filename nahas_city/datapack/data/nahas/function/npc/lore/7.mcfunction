scoreboard players set @s nh_npccd 120
tellraw @s {"text":"— حجر النجوم —","color":"gold","bold":true}
tellraw @s {"text":"«لكل نجمة حكاية، ولكل حكاية نهاية جميلة».","color":"white"}
tellraw @s {"text":"بحر النجوم يحفظ أسماء كل من عبر إليه.","color":"gray","italic":true}
particle minecraft:enchant ~ ~1 ~ 0.6 0.8 0.6 0.5 40 force @s
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1
execute unless entity @s[tag=nh_lore_7] run function nahas:npc/lore_first
tag @s add nh_lore_7
