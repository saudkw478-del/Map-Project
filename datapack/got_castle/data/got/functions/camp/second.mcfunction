scoreboard players add #camp_t got_g 1
scoreboard players operation #min got_g = #camp_t got_g
scoreboard players operation #min got_g /= #60 got_g
scoreboard players operation #winter got_g = #camp_t got_g
scoreboard players operation #winter got_g *= #100 got_g
scoreboard players operation #winter got_g /= #total_t got_g
execute if score #winter got_g matches 101.. run scoreboard players set #winter got_g 100
execute if score #next_t got_g > #camp_t got_g run scoreboard players operation #next_in got_g = #next_t got_g
execute if score #next_t got_g > #camp_t got_g run scoreboard players operation #next_in got_g -= #camp_t got_g
execute unless score #next_t got_g > #camp_t got_g run scoreboard players set #next_in got_g 0
execute if score #mode got_g matches 1 if score #camp_t got_g matches 180 run function got:camp/warn_castle_black
execute if score #mode got_g matches 1 if score #camp_t got_g matches 300 run function got:camp/attack_castle_black
execute if score #mode got_g matches 1 if score #camp_t got_g matches 600 run function got:camp/warn_kings_landing
execute if score #mode got_g matches 1 if score #camp_t got_g matches 720 run function got:camp/attack_kings_landing
execute if score #mode got_g matches 1 if score #camp_t got_g matches 1020 run function got:camp/warn_casterly_rock
execute if score #mode got_g matches 1 if score #camp_t got_g matches 1140 run function got:camp/attack_casterly_rock
execute if score #mode got_g matches 1 if score #camp_t got_g matches 1560 run function got:camp/final_warn
execute if score #mode got_g matches 1 if score #camp_t got_g matches 1680 run function got:camp/final_start
execute if score #mode got_g matches 2 if score #camp_t got_g matches 240 run function got:camp/warn_castle_black
execute if score #mode got_g matches 2 if score #camp_t got_g matches 360 run function got:camp/attack_castle_black
execute if score #mode got_g matches 2 if score #camp_t got_g matches 660 run function got:camp/warn_riverrun
execute if score #mode got_g matches 2 if score #camp_t got_g matches 780 run function got:camp/attack_riverrun
execute if score #mode got_g matches 2 if score #camp_t got_g matches 1080 run function got:camp/warn_kings_landing
execute if score #mode got_g matches 2 if score #camp_t got_g matches 1200 run function got:camp/attack_kings_landing
execute if score #mode got_g matches 2 if score #camp_t got_g matches 1500 run function got:camp/warn_casterly_rock
execute if score #mode got_g matches 2 if score #camp_t got_g matches 1620 run function got:camp/attack_casterly_rock
execute if score #mode got_g matches 2 if score #camp_t got_g matches 1920 run function got:camp/warn_highgarden
execute if score #mode got_g matches 2 if score #camp_t got_g matches 2040 run function got:camp/attack_highgarden
execute if score #mode got_g matches 2 if score #camp_t got_g matches 2340 run function got:camp/warn_storms_end
execute if score #mode got_g matches 2 if score #camp_t got_g matches 2460 run function got:camp/attack_storms_end
execute if score #mode got_g matches 2 if score #camp_t got_g matches 2760 run function got:camp/warn_sunspear
execute if score #mode got_g matches 2 if score #camp_t got_g matches 2880 run function got:camp/attack_sunspear
execute if score #mode got_g matches 2 if score #camp_t got_g matches 3180 run function got:camp/final_warn
execute if score #mode got_g matches 2 if score #camp_t got_g matches 3300 run function got:camp/final_start
