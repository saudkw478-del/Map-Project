# النهاية الكبرى: مشهد سينمائي لكل اللاعبين
function nahas:story/init
function nahas:story/sync
tellraw @s [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"شكرًا لكم... لقد حرّرتموني.","color":"yellow"}]
# يبدأ المشهد لكل اللاعبين مرة واحدة فقط (سواء استدعاها CORE لكل لاعب أو للاعب واحد)
execute as @a unless score @s nh_scene matches 2 run function nahas:intro/ending_start
