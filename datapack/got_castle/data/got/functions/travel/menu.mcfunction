tellraw @s {"text": "=== \u0627\u0644\u0633\u0641\u0631 (\u0627\u0643\u062a\u0628 /trigger got_go set \u0627\u0644\u0631\u0642\u0645) ===", "color": "gold", "bold": true}
execute if score #cs_castle_black got_g matches 2 run tellraw @s {"text": "2 - \u0627\u0644\u0642\u0644\u0639\u0629 \u0627\u0644\u0633\u0648\u062f\u0627\u0621  (\u0633\u0642\u0637\u062a!)", "color": "red"}
execute if score #cs_castle_black got_g matches 3 run tellraw @s [{"text": "2 - \u0627\u0644\u0642\u0644\u0639\u0629 \u0627\u0644\u0633\u0648\u062f\u0627\u0621  ", "color": "gray"}, {"text": "[\u0635\u0627\u0645\u062f\u0629]", "color": "green"}]
execute unless score #cs_castle_black got_g matches 2..3 run tellraw @s {"text": "2 - \u0627\u0644\u0642\u0644\u0639\u0629 \u0627\u0644\u0633\u0648\u062f\u0627\u0621", "color": "white"}
execute if score #cs_winterfell got_g matches 2 run tellraw @s {"text": "3 - \u0648\u064a\u0646\u062a\u0631\u0641\u064a\u0644  (\u0633\u0642\u0637\u062a!)", "color": "red"}
execute if score #cs_winterfell got_g matches 3 run tellraw @s [{"text": "3 - \u0648\u064a\u0646\u062a\u0631\u0641\u064a\u0644  ", "color": "gray"}, {"text": "[\u0635\u0627\u0645\u062f\u0629]", "color": "green"}]
execute unless score #cs_winterfell got_g matches 2..3 run tellraw @s {"text": "3 - \u0648\u064a\u0646\u062a\u0631\u0641\u064a\u0644", "color": "white"}
execute if score #cs_riverrun got_g matches 2 run tellraw @s {"text": "4 - \u0631\u064a\u0641\u0631\u0631\u0646  (\u0633\u0642\u0637\u062a!)", "color": "red"}
execute if score #cs_riverrun got_g matches 3 run tellraw @s [{"text": "4 - \u0631\u064a\u0641\u0631\u0631\u0646  ", "color": "gray"}, {"text": "[\u0635\u0627\u0645\u062f\u0629]", "color": "green"}]
execute unless score #cs_riverrun got_g matches 2..3 run tellraw @s {"text": "4 - \u0631\u064a\u0641\u0631\u0631\u0646", "color": "white"}
execute if score #cs_eyrie got_g matches 2 run tellraw @s {"text": "5 - \u0627\u0644\u0639\u0634  (\u0633\u0642\u0637\u062a!)", "color": "red"}
execute if score #cs_eyrie got_g matches 3 run tellraw @s [{"text": "5 - \u0627\u0644\u0639\u0634  ", "color": "gray"}, {"text": "[\u0635\u0627\u0645\u062f\u0629]", "color": "green"}]
execute unless score #cs_eyrie got_g matches 2..3 run tellraw @s {"text": "5 - \u0627\u0644\u0639\u0634", "color": "white"}
execute if score #cs_kings_landing got_g matches 2 run tellraw @s {"text": "6 - \u0643\u064a\u0646\u063a\u0632 \u0644\u0627\u0646\u062f\u064a\u0646\u063a  (\u0633\u0642\u0637\u062a!)", "color": "red"}
execute if score #cs_kings_landing got_g matches 3 run tellraw @s [{"text": "6 - \u0643\u064a\u0646\u063a\u0632 \u0644\u0627\u0646\u062f\u064a\u0646\u063a  ", "color": "gray"}, {"text": "[\u0635\u0627\u0645\u062f\u0629]", "color": "green"}]
execute unless score #cs_kings_landing got_g matches 2..3 run tellraw @s {"text": "6 - \u0643\u064a\u0646\u063a\u0632 \u0644\u0627\u0646\u062f\u064a\u0646\u063a", "color": "white"}
execute if score #cs_casterly_rock got_g matches 2 run tellraw @s {"text": "7 - \u0635\u062e\u0631\u0629 \u0643\u0627\u0633\u062a\u0644\u064a  (\u0633\u0642\u0637\u062a!)", "color": "red"}
execute if score #cs_casterly_rock got_g matches 3 run tellraw @s [{"text": "7 - \u0635\u062e\u0631\u0629 \u0643\u0627\u0633\u062a\u0644\u064a  ", "color": "gray"}, {"text": "[\u0635\u0627\u0645\u062f\u0629]", "color": "green"}]
execute unless score #cs_casterly_rock got_g matches 2..3 run tellraw @s {"text": "7 - \u0635\u062e\u0631\u0629 \u0643\u0627\u0633\u062a\u0644\u064a", "color": "white"}
execute if score #cs_highgarden got_g matches 2 run tellraw @s {"text": "8 - \u0647\u0627\u064a\u063a\u0627\u0631\u062f\u0646  (\u0633\u0642\u0637\u062a!)", "color": "red"}
execute if score #cs_highgarden got_g matches 3 run tellraw @s [{"text": "8 - \u0647\u0627\u064a\u063a\u0627\u0631\u062f\u0646  ", "color": "gray"}, {"text": "[\u0635\u0627\u0645\u062f\u0629]", "color": "green"}]
execute unless score #cs_highgarden got_g matches 2..3 run tellraw @s {"text": "8 - \u0647\u0627\u064a\u063a\u0627\u0631\u062f\u0646", "color": "white"}
execute if score #cs_storms_end got_g matches 2 run tellraw @s {"text": "9 - \u0646\u0647\u0627\u064a\u0629 \u0627\u0644\u0639\u0627\u0635\u0641\u0629  (\u0633\u0642\u0637\u062a!)", "color": "red"}
execute if score #cs_storms_end got_g matches 3 run tellraw @s [{"text": "9 - \u0646\u0647\u0627\u064a\u0629 \u0627\u0644\u0639\u0627\u0635\u0641\u0629  ", "color": "gray"}, {"text": "[\u0635\u0627\u0645\u062f\u0629]", "color": "green"}]
execute unless score #cs_storms_end got_g matches 2..3 run tellraw @s {"text": "9 - \u0646\u0647\u0627\u064a\u0629 \u0627\u0644\u0639\u0627\u0635\u0641\u0629", "color": "white"}
execute if score #cs_sunspear got_g matches 2 run tellraw @s {"text": "10 - \u0633\u0646\u0633\u0628\u064a\u0631  (\u0633\u0642\u0637\u062a!)", "color": "red"}
execute if score #cs_sunspear got_g matches 3 run tellraw @s [{"text": "10 - \u0633\u0646\u0633\u0628\u064a\u0631  ", "color": "gray"}, {"text": "[\u0635\u0627\u0645\u062f\u0629]", "color": "green"}]
execute unless score #cs_sunspear got_g matches 2..3 run tellraw @s {"text": "10 - \u0633\u0646\u0633\u0628\u064a\u0631", "color": "white"}
tellraw @s {"text": "11 - \u0642\u0645\u0629 \u0627\u0644\u062c\u062f\u0627\u0631", "color": "white"}
tellraw @s {"text": "12 - \u0645\u0627 \u0648\u0631\u0627\u0621 \u0627\u0644\u062c\u062f\u0627\u0631 (\u0627\u0644\u063a\u0627\u0628\u0629 \u0627\u0644\u0645\u0633\u0643\u0648\u0646\u0629)", "color": "white"}
tellraw @s {"text": "13 - \u0645\u0648\u062a \u0643\u064a\u0644\u064a\u0646", "color": "white"}
tellraw @s {"text": "14 - \u0627\u0644\u062a\u0648\u0623\u0645\u0627\u0646", "color": "white"}
tellraw @s {"text": "15 - \u0647\u0627\u0631\u064a\u0646\u0647\u0627\u0644", "color": "white"}
tellraw @s {"text": "16 - \u062f\u0631\u0627\u063a\u0648\u0646\u0633\u062a\u0648\u0646", "color": "white"}
tellraw @s {"text": "17 - \u0628\u0627\u064a\u0643 (\u062c\u0632\u0631 \u0627\u0644\u062d\u062f\u064a\u062f)", "color": "white"}
tellraw @s {"text": "18 - \u0623\u0648\u0644\u062f\u062a\u0627\u0648\u0646 - \u0628\u0631\u062c \u0647\u0627\u064a\u062a\u0627\u0648\u0631", "color": "white"}
tellraw @s {"text": "19 - \u0627\u0644\u0645\u064a\u0646\u0627\u0621 \u0627\u0644\u0623\u0628\u064a\u0636", "color": "white"}
