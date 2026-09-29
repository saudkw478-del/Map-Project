scoreboard players remove #cool got_g 1
execute if score #cool got_g matches 1..10 run title @a actionbar [{"text": "Next wave in ", "color": "yellow"}, {"score": {"name": "#cool", "objective": "got_g"}, "color": "gold"}, {"text": " s", "color": "yellow"}]
execute if score #cool got_g matches ..0 run function got:game/next_wave
