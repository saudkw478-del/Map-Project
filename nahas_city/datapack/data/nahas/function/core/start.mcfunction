scoreboard players set @s nh_start 0
execute unless entity @s[tag=nh_seen] run function nahas:core/first_join
execute if entity @s[tag=nh_seen] run function nahas:hook/first_join
