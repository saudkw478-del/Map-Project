scoreboard players set #t7 nh_g 9
scoreboard players set #trial nh_g 7
scoreboard players set #s7 nh_g 1
function nahas:core/seal_recount
execute as @a at @s run function nahas:core/seal_sync
