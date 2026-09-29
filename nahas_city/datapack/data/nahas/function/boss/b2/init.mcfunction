attribute @s minecraft:max_health base set 300
attribute @s minecraft:scale base set 2.0
attribute @s minecraft:attack_damage base set 5
attribute @s minecraft:knockback_resistance base set 0.7
attribute @s minecraft:follow_range base set 64
data modify entity @s Health set value 300.0f
execute if score #kids nh_g matches 1 run function nahas:boss/b2/init_kids
