scoreboard players set #t3 nh_g 9
scoreboard players set #trial nh_g 3
scoreboard players set #s3 nh_g 1
function nahas:core/seal_recount
execute as @a at @s run function nahas:core/seal_sync
execute as @a at @s run function nahas:hook/trial_done
