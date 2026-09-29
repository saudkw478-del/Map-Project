tag @s add got_seen
tellraw @s {"text": "Winter is coming.", "color": "aqua", "bold": true}
tellraw @s {"text": "You stand in Winterfell, seat of House Stark. The realm of Westeros lies before you:", "color": "white"}
tellraw @s {"text": "the Wall in the north, the Iron Throne in King's Landing, and the sun-scorched land of Dorne far in the south.", "color": "white"}
tellraw @s {"text": "Conquer each great castle in battle - and when the Night King comes, hold Winterfell.", "color": "yellow"}
tellraw @s {"text": "Type /trigger got_go to travel, /trigger got_battle to fight, /trigger got_kit for gear.", "color": "green"}
function got:kit/give
function got:kit/give_travel
