# بدأت تجربة (#trial = 1..7)
function nahas:story/sync
title @a times 10 70 20
execute if score #trial nh_story matches 1 run title @a subtitle {"text":"حلّوا ألغاز المعبد بهدوء وعاونوا بعضكم.","color":"yellow"}
execute if score #trial nh_story matches 1 run title @a title {"text":"التجربة 1: معبد الواحة","color":"gold","bold":true}
execute if score #trial nh_story matches 1 run tellraw @a [{"text":"⚔ التجربة ","color":"gold"},{"text":"1 - معبد الواحة","color":"gold","bold":true},{"text":": حلّوا ألغاز المعبد بهدوء وعاونوا بعضكم.","color":"white"}]
execute if score #trial nh_story matches 2 run title @a subtitle {"text":"احذروا لسعات العقارب، وتعاونوا على ملكتها.","color":"yellow"}
execute if score #trial nh_story matches 2 run title @a title {"text":"التجربة 2: وادي العقارب","color":"gold","bold":true}
execute if score #trial nh_story matches 2 run tellraw @a [{"text":"⚔ التجربة ","color":"gold"},{"text":"2 - وادي العقارب","color":"gold","bold":true},{"text":": احذروا لسعات العقارب، وتعاونوا على ملكتها.","color":"white"}]
execute if score #trial nh_story matches 3 run title @a subtitle {"text":"خذوا نفسًا عميقًا! القاعات غارقة في الماء.","color":"yellow"}
execute if score #trial nh_story matches 3 run title @a title {"text":"التجربة 3: المكتبة الغارقة","color":"gold","bold":true}
execute if score #trial nh_story matches 3 run tellraw @a [{"text":"⚔ التجربة ","color":"gold"},{"text":"3 - المكتبة الغارقة","color":"gold","bold":true},{"text":": خذوا نفسًا عميقًا! القاعات غارقة في الماء.","color":"white"}]
execute if score #trial nh_story matches 4 run title @a subtitle {"text":"اصعدوا بحذر ولا تنظروا إلى الأسفل.","color":"yellow"}
execute if score #trial nh_story matches 4 run title @a title {"text":"التجربة 4: قلعة الريح","color":"gold","bold":true}
execute if score #trial nh_story matches 4 run tellraw @a [{"text":"⚔ التجربة ","color":"gold"},{"text":"4 - قلعة الريح","color":"gold","bold":true},{"text":": اصعدوا بحذر ولا تنظروا إلى الأسفل.","color":"white"}]
execute if score #trial nh_story matches 5 run title @a subtitle {"text":"اقفزوا بين الجزر بهدوء، فالنجوم تحرسكم.","color":"yellow"}
execute if score #trial nh_story matches 5 run title @a title {"text":"التجربة 5: بحر النجوم","color":"gold","bold":true}
execute if score #trial nh_story matches 5 run tellraw @a [{"text":"⚔ التجربة ","color":"gold"},{"text":"5 - بحر النجوم","color":"gold","bold":true},{"text":": اقفزوا بين الجزر بهدوء، فالنجوم تحرسكم.","color":"white"}]
execute if score #trial nh_story matches 6 run title @a subtitle {"text":"الحمم حارّة! امشوا على الأعمدة بحذر.","color":"yellow"}
execute if score #trial nh_story matches 6 run title @a title {"text":"التجربة 6: أرض الجمر","color":"gold","bold":true}
execute if score #trial nh_story matches 6 run tellraw @a [{"text":"⚔ التجربة ","color":"gold"},{"text":"6 - أرض الجمر","color":"gold","bold":true},{"text":": الحمم حارّة! امشوا على الأعمدة بحذر.","color":"white"}]
execute if score #trial nh_story matches 7 run title @a subtitle {"text":"الحارس النحاسي ينتظركم في ساحة القصر.","color":"yellow"}
execute if score #trial nh_story matches 7 run title @a title {"text":"التجربة 7: ساحة القصر","color":"gold","bold":true}
execute if score #trial nh_story matches 7 run tellraw @a [{"text":"⚔ التجربة ","color":"gold"},{"text":"7 - ساحة القصر","color":"gold","bold":true},{"text":": الحارس النحاسي ينتظركم في ساحة القصر.","color":"white"}]
execute as @a at @s run playsound minecraft:block.bell.use master @s ~ ~ ~ 1 1
