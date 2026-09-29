scoreboard players remove #cool got_g 1
execute if score #cool got_g matches 1..10 run title @a actionbar [{"text": "\u0627\u0644\u0645\u0648\u062c\u0629 \u0627\u0644\u0642\u0627\u062f\u0645\u0629 \u0628\u0639\u062f ", "color": "yellow"}, {"score": {"name": "#cool", "objective": "got_g"}, "color": "gold"}, {"text": " \u062b\u0627\u0646\u064a\u0629", "color": "yellow"}]
execute if score #cool got_g matches ..0 run function got:game/next_wave
