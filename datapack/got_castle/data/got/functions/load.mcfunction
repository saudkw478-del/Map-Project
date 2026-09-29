scoreboard objectives add got_g dummy {"text": "\u062d\u0631\u0628 \u0627\u0644\u0645\u0645\u0627\u0644\u0643", "color": "gold"}
scoreboard objectives add got_hud dummy {"text": "\u0627\u0644\u0644\u064a\u0644 \u0627\u0644\u0637\u0648\u064a\u0644", "color": "aqua", "bold": true}
scoreboard objectives add got_go trigger
scoreboard objectives add got_battle trigger
scoreboard objectives add got_kit trigger
scoreboard objectives add got_house trigger
scoreboard objectives add got_power trigger
scoreboard objectives add got_shop trigger
scoreboard objectives add got_scout trigger
scoreboard objectives add got_quest trigger
scoreboard objectives add got_start trigger
scoreboard objectives add got_accuse trigger
scoreboard objectives add got_reg dummy
scoreboard objectives add got_talkcd dummy
scoreboard objectives add got_gift dummy
scoreboard objectives add got_gold dummy
scoreboard objectives add got_renown dummy
scoreboard objectives add got_pcd dummy
scoreboard objectives add got_scd dummy
scoreboard objectives add got_scoutt dummy
scoreboard objectives add got_id dummy
scoreboard objectives add got_deaths deathCount
team add got_enemies
team modify got_enemies color red
team add got_stark {"text": "\u0622\u0644 \u0633\u062a\u0627\u0631\u0643", "color": "white"}
team modify got_stark color white
team add got_lannister {"text": "\u0622\u0644 \u0644\u0627\u0646\u0633\u062a\u0631", "color": "gold"}
team modify got_lannister color gold
team add got_targaryen {"text": "\u0622\u0644 \u062a\u0627\u0631\u062c\u0627\u0631\u064a\u0627\u0646", "color": "dark_red"}
team modify got_targaryen color dark_red
team add got_martell {"text": "\u0622\u0644 \u0645\u0627\u0631\u062a\u0644", "color": "red"}
team modify got_martell color red
team add got_tyrell {"text": "\u0622\u0644 \u062a\u0627\u064a\u0631\u064a\u0644", "color": "green"}
team modify got_tyrell color green
team add got_baratheon {"text": "\u0622\u0644 \u0628\u0627\u0631\u0627\u062b\u064a\u0648\u0646", "color": "yellow"}
team modify got_baratheon color yellow
team add got_greyjoy {"text": "\u0622\u0644 \u063a\u0631\u064a\u062c\u0648\u064a", "color": "dark_gray"}
team modify got_greyjoy color dark_gray
team add got_arryn {"text": "\u0622\u0644 \u0623\u0631\u064a\u0646", "color": "aqua"}
team modify got_arryn color aqua
team add got_tully {"text": "\u0622\u0644 \u062a\u0648\u0644\u064a", "color": "blue"}
team modify got_tully color blue
execute unless score #state got_g matches 0.. run scoreboard players set #state got_g 0
execute unless score #camp got_g matches 0.. run scoreboard players set #camp got_g 0
scoreboard players set #100 got_g 100
scoreboard players add #min got_g 0
scoreboard players add #winter got_g 0
scoreboard players add #held got_g 0
scoreboard players add #fallen got_g 0
scoreboard players add #next_in got_g 0
scoreboard players add #next_t got_g 0
scoreboard players add #wave got_g 0
scoreboard players add #enemies got_g 0
scoreboard players add #camp_battle got_g 0
scoreboard players add #final got_g 0
scoreboard players add #mode got_g 0
scoreboard players add #total_t got_g 0
scoreboard players add #camp_t got_g 0
scoreboard players add #idc got_g 0
scoreboard players add #d got_g 0
scoreboard players add #d0 got_g 0
scoreboard players add #dd got_g 0
scoreboard players add #site got_g 0
scoreboard players add #theme got_g 0
scoreboard players add #base got_g 0
scoreboard players add #total got_g 0
scoreboard players add #gear got_g 0
scoreboard players add #cool got_g 0
scoreboard players add #players got_g 0
scoreboard players set #60 got_g 60
function got:util/rules
setworldspawn 270 64 378
function got:hud/names
tellraw @a [{"text": "[\u062d\u0631\u0628 \u0627\u0644\u0645\u0645\u0627\u0644\u0643] ", "color": "gold", "bold": true}, {"text": "\u0627\u0644\u0639\u0627\u0644\u0645 \u062c\u0627\u0647\u0632. \u0627\u0643\u062a\u0628 /trigger got_quest \u0644\u0645\u0639\u0631\u0641\u0629 \u0627\u0644\u0648\u0636\u0639 \u0648 /trigger got_house \u0644\u0627\u062e\u062a\u064a\u0627\u0631 \u0628\u064a\u062a\u0643.", "color": "white"}]
