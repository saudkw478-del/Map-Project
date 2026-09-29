tellraw @s {"text": "=== Travel (type /trigger got_go set N) ===", "color": "gold", "bold": true}
execute unless score #won_castle_black got_g matches 1 run tellraw @s {"text": "2 - Castle Black  (battle #1)", "color": "white"}
execute if score #won_castle_black got_g matches 1 run tellraw @s [{"text": "2 - Castle Black  (battle #1) ", "color": "gray"}, {"text": "[conquered]", "color": "green"}]
execute unless score #won_winterfell got_g matches 1 run tellraw @s {"text": "3 - Winterfell  (battle #9)", "color": "white"}
execute if score #won_winterfell got_g matches 1 run tellraw @s [{"text": "3 - Winterfell  (battle #9) ", "color": "gray"}, {"text": "[conquered]", "color": "green"}]
execute unless score #won_riverrun got_g matches 1 run tellraw @s {"text": "4 - Riverrun  (battle #2)", "color": "white"}
execute if score #won_riverrun got_g matches 1 run tellraw @s [{"text": "4 - Riverrun  (battle #2) ", "color": "gray"}, {"text": "[conquered]", "color": "green"}]
execute unless score #won_eyrie got_g matches 1 run tellraw @s {"text": "5 - The Eyrie  (battle #7)", "color": "white"}
execute if score #won_eyrie got_g matches 1 run tellraw @s [{"text": "5 - The Eyrie  (battle #7) ", "color": "gray"}, {"text": "[conquered]", "color": "green"}]
execute unless score #won_kings_landing got_g matches 1 run tellraw @s {"text": "6 - King's Landing  (battle #3)", "color": "white"}
execute if score #won_kings_landing got_g matches 1 run tellraw @s [{"text": "6 - King's Landing  (battle #3) ", "color": "gray"}, {"text": "[conquered]", "color": "green"}]
execute unless score #won_casterly_rock got_g matches 1 run tellraw @s {"text": "7 - Casterly Rock  (battle #4)", "color": "white"}
execute if score #won_casterly_rock got_g matches 1 run tellraw @s [{"text": "7 - Casterly Rock  (battle #4) ", "color": "gray"}, {"text": "[conquered]", "color": "green"}]
execute unless score #won_highgarden got_g matches 1 run tellraw @s {"text": "8 - Highgarden  (battle #5)", "color": "white"}
execute if score #won_highgarden got_g matches 1 run tellraw @s [{"text": "8 - Highgarden  (battle #5) ", "color": "gray"}, {"text": "[conquered]", "color": "green"}]
execute unless score #won_storms_end got_g matches 1 run tellraw @s {"text": "9 - Storm's End  (battle #6)", "color": "white"}
execute if score #won_storms_end got_g matches 1 run tellraw @s [{"text": "9 - Storm's End  (battle #6) ", "color": "gray"}, {"text": "[conquered]", "color": "green"}]
execute unless score #won_sunspear got_g matches 1 run tellraw @s {"text": "10 - Sunspear  (battle #8)", "color": "white"}
execute if score #won_sunspear got_g matches 1 run tellraw @s [{"text": "10 - Sunspear  (battle #8) ", "color": "gray"}, {"text": "[conquered]", "color": "green"}]
tellraw @s {"text": "11 - Top of the Wall", "color": "white"}
tellraw @s {"text": "12 - Beyond the Wall (Haunted Forest)", "color": "white"}
tellraw @s {"text": "13 - Moat Cailin", "color": "white"}
tellraw @s {"text": "14 - The Twins", "color": "white"}
tellraw @s {"text": "15 - Harrenhal", "color": "white"}
tellraw @s {"text": "16 - Dragonstone", "color": "white"}
tellraw @s {"text": "17 - Pyke (Iron Islands)", "color": "white"}
tellraw @s {"text": "18 - Oldtown - the Hightower", "color": "white"}
tellraw @s {"text": "19 - White Harbor", "color": "white"}
tellraw @s {"text": "Recommended order of battles: Castle Black > Riverrun > King's Landing > Casterly Rock > Highgarden > Storm's End > The Eyrie > Sunspear > Winterfell", "color": "aqua"}
