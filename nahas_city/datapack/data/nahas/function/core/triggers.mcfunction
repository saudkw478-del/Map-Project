execute as @a[scores={nh_role=1..}] unless score @s nh_role = @s nh_prole at @s run function nahas:role/trigger
execute as @a[scores={nh_role=0}] if score @s nh_prole matches 1.. run scoreboard players operation @s nh_role = @s nh_prole
execute as @a[scores={nh_role=..-1}] run function nahas:role/menu
execute as @a[scores={nh_go=1..}] at @s run function nahas:portal/go
scoreboard players set @a[scores={nh_go=..-1}] nh_go 0
execute as @a[scores={nh_shop=1..}] at @s run function nahas:shop/trigger
scoreboard players set @a[scores={nh_shop=..-1}] nh_shop 0
execute as @a[scores={nh_quest=1..}] at @s run function nahas:quest/trigger
scoreboard players set @a[scores={nh_quest=..-1}] nh_quest 0
execute as @a[scores={nh_power=1..}] at @s run function nahas:role/power
scoreboard players set @a[scores={nh_power=..-1}] nh_power 0
execute as @a[scores={nh_map=1..}] at @s run function nahas:items/map
scoreboard players set @a[scores={nh_map=..-1}] nh_map 0
execute as @a[scores={nh_help=1..}] at @s run function nahas:core/help
scoreboard players set @a[scores={nh_help=..-1}] nh_help 0
execute as @a[scores={nh_ask=1..}] at @s run function nahas:core/ask
scoreboard players set @a[scores={nh_ask=..-1}] nh_ask 0
execute as @a[scores={nh_start=1..}] at @s run function nahas:core/start
scoreboard players set @a[scores={nh_start=..-1}] nh_start 0
