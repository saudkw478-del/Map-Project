# أول دخول: يبدأ المشهد السينمائي (المنفّذ: اللاعب)
function nahas:story/init
function nahas:story/sync
# CORE يستدعي هذه الدالة أيضًا عند /trigger nh_start (إعادة القصة): إن كان اللاعب داخل مشهد فهذا يعني تخطّيه
execute if score @s nh_intro matches 0.. run return run function nahas:intro/skip
spawnpoint @s 300 71 2053
function nahas:intro/start
