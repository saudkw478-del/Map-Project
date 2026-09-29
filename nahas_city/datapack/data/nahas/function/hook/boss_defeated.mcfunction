# النهاية الكبرى: مشهد سينمائي لكل اللاعبين
function nahas:story/init
function nahas:story/sync
tellraw @a [{"text":"الحارس النحاسي: ","color":"gold","bold":true},{"text":"شكرًا لكم... لقد حرّرتموني.","color":"yellow"}]
execute as @a run function nahas:intro/ending_start
