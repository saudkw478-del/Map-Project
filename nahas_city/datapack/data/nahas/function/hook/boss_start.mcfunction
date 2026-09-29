# بدأت معركة الحارس (CORE يستدعيها لكل لاعب قريب؛ الرسائل @s، وتأخير الحوار بـ schedule عام)
function nahas:story/sync
title @s times 10 70 20
title @s subtitle {"text":"يستيقظ من نومه الطويل","color":"yellow"}
title @s title {"text":"الحارس النحاسي","color":"gold","bold":true}
playsound minecraft:block.bell.use master @s ~ ~ ~ 2 0.5
playsound minecraft:entity.lightning_bolt.thunder master @s ~ ~ ~ 2 0.6
tellraw @s [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"من الذي أيقظني من نومي الطويل؟","color":"red"}]
schedule function nahas:story/boss_line_1 80t
schedule function nahas:story/boss_line_2 200t
