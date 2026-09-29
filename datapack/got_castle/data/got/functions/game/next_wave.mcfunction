scoreboard players add #wave got_g 1
scoreboard players operation Wave got_g = #wave got_g
scoreboard players set #state got_g 1
execute if score #wave got_g matches 1 run function got:wave/w1
execute if score #wave got_g matches 2 run function got:wave/w2
execute if score #wave got_g matches 3 run function got:wave/w3
execute if score #wave got_g matches 4 run function got:wave/w4
execute if score #wave got_g matches 5 run function got:wave/w5
execute if score #wave got_g matches 6 run function got:wave/w6
execute if score #wave got_g matches 7 run function got:wave/w7
