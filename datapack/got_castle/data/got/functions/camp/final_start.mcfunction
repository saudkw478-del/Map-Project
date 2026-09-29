scoreboard players set #final got_g 1
scoreboard players set #winter got_g 100
function got:util/weather_thunder
tp @a 270 64 385
execute unless score #state got_g matches 0 unless score #state got_g matches 4 run function got:game/stop
schedule function got:camp/final_go 60t
