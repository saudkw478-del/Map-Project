scoreboard objectives add got_g dummy {"text": "Game of Thrones", "color": "gold"}
scoreboard objectives add got_go trigger
scoreboard objectives add got_battle trigger
scoreboard objectives add got_kit trigger
scoreboard objectives add got_reg dummy
scoreboard objectives add got_talkcd dummy
scoreboard objectives add got_gift dummy
team add got_enemies
team modify got_enemies color red
execute unless score #state got_g matches 0.. run scoreboard players set #state got_g 0
function got:util/rules
setworldspawn 270 64 378
tellraw @a [{"text": "[Game of Thrones] ", "color": "gold"}, {"text": "Westeros is ready. Type /trigger got_go to travel.", "color": "white"}]
