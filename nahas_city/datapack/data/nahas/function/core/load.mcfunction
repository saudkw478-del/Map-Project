scoreboard objectives add nh_g dummy {"text":"الحالة","color":"white"}
scoreboard objectives add nh_gold dummy {"text":"الذهب","color":"white"}
scoreboard objectives add nh_prole dummy
scoreboard objectives add nh_cd dummy
scoreboard objectives add nh_cd2 dummy
scoreboard objectives add nh_gocd dummy
scoreboard objectives add nh_pcd dummy
scoreboard objectives add nh_tmp dummy
scoreboard objectives add nh_lastk dummy
scoreboard objectives add nh_lastseal dummy
scoreboard objectives add nh_askf dummy
scoreboard objectives add nh_disc dummy
scoreboard objectives add nh_kills totalKillCount
scoreboard objectives add nh_dead deathCount
scoreboard objectives add nh_role trigger
scoreboard objectives add nh_go trigger
scoreboard objectives add nh_shop trigger
scoreboard objectives add nh_quest trigger
scoreboard objectives add nh_power trigger
scoreboard objectives add nh_map trigger
scoreboard objectives add nh_help trigger
scoreboard objectives add nh_ask trigger
scoreboard objectives add nh_start trigger
scoreboard objectives setdisplay list nh_gold
scoreboard players set #2 nh_g 2
scoreboard players set #10 nh_g 10
scoreboard players set #100 nh_g 100
function nahas:core/gamerules
execute unless score #init nh_g matches 1 run function nahas:core/first_load
scoreboard players set #loaded nh_g 1
