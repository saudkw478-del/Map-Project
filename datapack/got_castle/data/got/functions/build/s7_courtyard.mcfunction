execute at @e[tag=got_origin,limit=1] run function got:build/s7_courtyard_a
execute at @e[tag=got_origin,limit=1] run forceload remove ~-60 ~-60 ~60 ~60
function got:util/rules
tellraw @a [{"text": "The castle is ready! ", "color": "green", "bold": true}, {"text": "Weapons & armor are in the armory (west courtyard). Start the game: /function got:game/start", "color": "white"}]
