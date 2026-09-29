scoreboard players set @s nh_npccd 10
tellraw @s {"text":"— حجر الواحة —","color":"gold","bold":true}
tellraw @s {"text":"«الماء أثمن من الذهب، والصديق أثمن من الماء».","color":"white"}
tellraw @s {"text":"قيل إنّ نبع الواحة لا ينضب ما دام أهلها كرماء.","color":"gray","italic":true}
particle minecraft:enchant ~ ~1 ~ 0.6 0.8 0.6 0.5 40 force @s
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1
execute unless entity @s[tag=nh_lore_2] run function nahas:npc/lore_first
tag @s add nh_lore_2
