# يحفظ وضع اللعب السابق: 0 بقاء، 1 إبداع، 2 مغامرة
scoreboard players set @s nh_introgm 0
execute if entity @s[gamemode=creative] run scoreboard players set @s nh_introgm 1
execute if entity @s[gamemode=adventure] run scoreboard players set @s nh_introgm 2
