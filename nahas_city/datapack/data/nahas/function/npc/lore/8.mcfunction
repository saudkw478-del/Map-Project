scoreboard players set @s nh_npccd 10
tellraw @s {"text":"— حجر الجمر —","color":"gold","bold":true}
tellraw @s {"text":"«النار تحرق من يعاديها وتدفّئ من يحترمها».","color":"white"}
tellraw @s {"text":"الجمر يخفي أعمق أسرار المدينة.","color":"gray","italic":true}
particle minecraft:enchant ~ ~1 ~ 0.6 0.8 0.6 0.5 40 force @s
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1
execute unless entity @s[tag=nh_lore_8] run function nahas:npc/lore_first
tag @s add nh_lore_8
