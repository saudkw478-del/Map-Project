# تخطّي: /trigger nh_start set 1 (CORE يعالج nh_start ويستدعي hook/first_join، وهذه تتحوّل إلى تخطٍّ أثناء المشهد)
scoreboard players set @s nh_start 0
tellraw @s {"text":"تم تخطّي المقدّمة.","color":"gray"}
function nahas:intro/end
