scoreboard players add #wave got_g 1
scoreboard players operation Wave got_g = #wave got_g
scoreboard players operation #gear got_g = #wave got_g
scoreboard players operation #gear got_g += #base got_g
scoreboard players set #state got_g 1
execute if score #theme got_g matches 1 if score #wave got_g matches 1 run function got:wave/wildlings_1
execute if score #theme got_g matches 1 if score #wave got_g matches 2 run function got:wave/wildlings_2
execute if score #theme got_g matches 1 if score #wave got_g matches 3 run function got:wave/wildlings_3
execute if score #theme got_g matches 1 if score #wave got_g matches 4 run function got:wave/wildlings_4
execute if score #theme got_g matches 2 if score #wave got_g matches 1 run function got:wave/long_night_1
execute if score #theme got_g matches 2 if score #wave got_g matches 2 run function got:wave/long_night_2
execute if score #theme got_g matches 2 if score #wave got_g matches 3 run function got:wave/long_night_3
execute if score #theme got_g matches 2 if score #wave got_g matches 4 run function got:wave/long_night_4
execute if score #theme got_g matches 2 if score #wave got_g matches 5 run function got:wave/long_night_5
execute if score #theme got_g matches 2 if score #wave got_g matches 6 run function got:wave/long_night_6
execute if score #theme got_g matches 2 if score #wave got_g matches 7 run function got:wave/long_night_7
execute if score #theme got_g matches 3 if score #wave got_g matches 1 run function got:wave/freys_1
execute if score #theme got_g matches 3 if score #wave got_g matches 2 run function got:wave/freys_2
execute if score #theme got_g matches 3 if score #wave got_g matches 3 run function got:wave/freys_3
execute if score #theme got_g matches 3 if score #wave got_g matches 4 run function got:wave/freys_4
execute if score #theme got_g matches 4 if score #wave got_g matches 1 run function got:wave/mountain_1
execute if score #theme got_g matches 4 if score #wave got_g matches 2 run function got:wave/mountain_2
execute if score #theme got_g matches 4 if score #wave got_g matches 3 run function got:wave/mountain_3
execute if score #theme got_g matches 5 if score #wave got_g matches 1 run function got:wave/blackwater_1
execute if score #theme got_g matches 5 if score #wave got_g matches 2 run function got:wave/blackwater_2
execute if score #theme got_g matches 5 if score #wave got_g matches 3 run function got:wave/blackwater_3
execute if score #theme got_g matches 5 if score #wave got_g matches 4 run function got:wave/blackwater_4
execute if score #theme got_g matches 5 if score #wave got_g matches 5 run function got:wave/blackwater_5
execute if score #theme got_g matches 6 if score #wave got_g matches 1 run function got:wave/lannister_1
execute if score #theme got_g matches 6 if score #wave got_g matches 2 run function got:wave/lannister_2
execute if score #theme got_g matches 6 if score #wave got_g matches 3 run function got:wave/lannister_3
execute if score #theme got_g matches 6 if score #wave got_g matches 4 run function got:wave/lannister_4
execute if score #theme got_g matches 7 if score #wave got_g matches 1 run function got:wave/reach_1
execute if score #theme got_g matches 7 if score #wave got_g matches 2 run function got:wave/reach_2
execute if score #theme got_g matches 7 if score #wave got_g matches 3 run function got:wave/reach_3
execute if score #theme got_g matches 7 if score #wave got_g matches 4 run function got:wave/reach_4
execute if score #theme got_g matches 8 if score #wave got_g matches 1 run function got:wave/storm_1
execute if score #theme got_g matches 8 if score #wave got_g matches 2 run function got:wave/storm_2
execute if score #theme got_g matches 8 if score #wave got_g matches 3 run function got:wave/storm_3
execute if score #theme got_g matches 8 if score #wave got_g matches 4 run function got:wave/storm_4
execute if score #theme got_g matches 8 if score #wave got_g matches 5 run function got:wave/storm_5
execute if score #theme got_g matches 9 if score #wave got_g matches 1 run function got:wave/dorne_1
execute if score #theme got_g matches 9 if score #wave got_g matches 2 run function got:wave/dorne_2
execute if score #theme got_g matches 9 if score #wave got_g matches 3 run function got:wave/dorne_3
execute if score #theme got_g matches 9 if score #wave got_g matches 4 run function got:wave/dorne_4
