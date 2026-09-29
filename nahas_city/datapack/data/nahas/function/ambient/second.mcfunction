# أجواء كل ثانية (يُستدعى من CORE). لا يعمل على من هو داخل مشهد سينمائي.
function nahas:story/init
function nahas:fx/time_query
scoreboard players set #night nh_story 0
execute if score #t nh_story matches 13000..23000 run scoreboard players set #night nh_story 1
execute as @a[scores={nh_intro=..-1}] at @s run function nahas:ambient/player
