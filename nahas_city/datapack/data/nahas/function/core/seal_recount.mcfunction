scoreboard players set #seals nh_g 0
execute if score #s1 nh_g matches 1 run scoreboard players add #seals nh_g 1
execute if score #s2 nh_g matches 1 run scoreboard players add #seals nh_g 1
execute if score #s3 nh_g matches 1 run scoreboard players add #seals nh_g 1
execute if score #s4 nh_g matches 1 run scoreboard players add #seals nh_g 1
execute if score #s5 nh_g matches 1 run scoreboard players add #seals nh_g 1
execute if score #s6 nh_g matches 1 run scoreboard players add #seals nh_g 1
execute if score #s7 nh_g matches 1 run scoreboard players add #seals nh_g 1
execute if score #seals nh_g matches 3.. run advancement grant @a only nahas:seals_3
execute if score #seals nh_g matches 6.. unless score #city nh_g matches 1 run function nahas:core/city_open
