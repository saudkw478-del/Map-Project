scoreboard players set #camp_battle got_g 0
kill @e[tag=got_wight,distance=..120]
execute if score #site got_g matches 1 run function got:camp/held_castle_black
execute if score #site got_g matches 2 run function got:camp/held_winterfell
execute if score #site got_g matches 3 run function got:camp/held_riverrun
execute if score #site got_g matches 4 run function got:camp/held_eyrie
execute if score #site got_g matches 5 run function got:camp/held_kings_landing
execute if score #site got_g matches 6 run function got:camp/held_casterly_rock
execute if score #site got_g matches 7 run function got:camp/held_highgarden
execute if score #site got_g matches 8 run function got:camp/held_storms_end
execute if score #site got_g matches 9 run function got:camp/held_sunspear
execute if score #final got_g matches 1 run function got:camp/win
