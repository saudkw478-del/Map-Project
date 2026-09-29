bossbar set nahas:boss1 players @a[distance=..100]
execute store result score #hp nh_g run data get entity @s Health
execute store result bossbar nahas:boss1 value run data get entity @s Health
scoreboard players operation #pct nh_g = #hp nh_g
scoreboard players operation #pct nh_g *= #100 nh_g
scoreboard players operation #pct nh_g /= #bmax1 nh_g
scoreboard players set #np nh_g 1
execute if score #pct nh_g matches ..66 run scoreboard players set #np nh_g 2
execute if score #pct nh_g matches ..33 run scoreboard players set #np nh_g 3
execute unless score #np nh_g = #b1_ph nh_g run function nahas:boss/b1/phase
scoreboard players add #b1_t nh_g 1
execute if score #b1_t nh_g matches 5.. run function nahas:boss/b1/act
