attribute @s minecraft:max_health base set 400
attribute @s minecraft:scale base set 3.0
attribute @s minecraft:attack_damage base set 6
attribute @s minecraft:knockback_resistance base set 0.7
attribute @s minecraft:follow_range base set 64
data modify entity @s Health set value 400.0f
execute if score #kids nh_g matches 1 run function nahas:boss/b1/init_kids
