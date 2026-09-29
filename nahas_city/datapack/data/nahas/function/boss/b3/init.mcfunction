attribute @s minecraft:max_health base set 350
attribute @s minecraft:scale base set 1.5
attribute @s minecraft:attack_damage base set 6
attribute @s minecraft:knockback_resistance base set 0.7
attribute @s minecraft:follow_range base set 64
data modify entity @s Health set value 350.0f
execute if score #kids nh_g matches 1 run function nahas:boss/b3/init_kids
