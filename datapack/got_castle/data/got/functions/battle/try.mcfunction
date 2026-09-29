execute unless score #state got_g matches 0 unless score #state got_g matches 4 run return run tellraw @s {"text": "A battle is already in progress! (/trigger got_battle set 2 stops it)", "color": "red"}
execute positioned 250 64 236 if entity @s[distance=..80] run return run function got:battle/start_castle_black
execute positioned 270 64 350 if entity @s[distance=..80] run return run function got:battle/start_winterfell
execute positioned 235 64 770 if entity @s[distance=..80] run return run function got:battle/start_riverrun
execute positioned 500 124 690 if entity @s[distance=..80] run return run function got:battle/start_eyrie
execute positioned 405 64 880 if entity @s[distance=..80] run return run function got:battle/start_kings_landing
execute positioned 140 64 800 if entity @s[distance=..80] run return run function got:battle/start_casterly_rock
execute positioned 215 64 1030 if entity @s[distance=..80] run return run function got:battle/start_highgarden
execute positioned 480 64 1005 if entity @s[distance=..80] run return run function got:battle/start_storms_end
execute positioned 470 64 1235 if entity @s[distance=..80] run return run function got:battle/start_sunspear
tellraw @s {"text": "Stand inside a great castle (within its walls) to start its battle.", "color": "yellow"}
