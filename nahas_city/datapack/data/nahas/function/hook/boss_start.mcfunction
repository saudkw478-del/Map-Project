# بدأت معركة الحارس
function nahas:story/sync
title @a times 10 70 20
title @a subtitle {"text":"يستيقظ من نومه الطويل","color":"yellow"}
title @a title {"text":"الحارس النحاسي","color":"gold","bold":true}
execute as @a at @s run playsound minecraft:block.bell.use master @s ~ ~ ~ 2 0.5
execute as @a at @s run playsound minecraft:entity.lightning_bolt.thunder master @s ~ ~ ~ 2 0.6
tellraw @a [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"من الذي أيقظني من نومي الطويل؟","color":"red"}]
schedule function nahas:story/boss_line_1 80t
schedule function nahas:story/boss_line_2 200t
