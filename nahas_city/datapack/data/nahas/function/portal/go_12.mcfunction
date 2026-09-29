tag @s add nh_self
execute if entity @a[tag=!nh_self] run scoreboard players set @s nh_gocd 30
execute if entity @a[tag=!nh_self] run tp @s @r[tag=!nh_self]
execute unless entity @a[tag=!nh_self] run tellraw @s {"text":"لا يوجد أصدقاء آخرون الآن.","color":"yellow"}
tag @s remove nh_self
