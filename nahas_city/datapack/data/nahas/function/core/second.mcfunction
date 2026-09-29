scoreboard players set #tk nh_g 0
scoreboard players enable @a nh_role
scoreboard players enable @a nh_go
scoreboard players enable @a nh_shop
scoreboard players enable @a nh_quest
scoreboard players enable @a nh_power
scoreboard players enable @a nh_map
scoreboard players enable @a nh_help
scoreboard players enable @a nh_ask
scoreboard players enable @a nh_start
scoreboard players add @a nh_gold 0
scoreboard players add @a nh_cd 0
scoreboard players add @a nh_cd2 0
scoreboard players add @a nh_gocd 0
scoreboard players add @a nh_pcd 0
scoreboard players add @a nh_prole 0
scoreboard players add @a nh_kills 0
scoreboard players add @a nh_lastk 0
scoreboard players add @a nh_disc 0
scoreboard players add @a nh_dead 0
scoreboard players add @a nh_askf 0
execute as @a[tag=!nh_seen] at @s run function nahas:core/first_join
execute as @a at @s run function nahas:core/player_second
execute as @a[scores={nh_dead=1..}] at @s run function nahas:core/died
function nahas:core/world_second
function nahas:trial/second
function nahas:boss/second
function nahas:ambient/second
function nahas:npc/second
