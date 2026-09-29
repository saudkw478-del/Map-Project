# أجواء الليل العامة (المنفّذ: اللاعب في العالم العادي): رعد بعيد وهمس
execute store result score #r nh_story run random value 1..100
execute if score #r nh_story matches 1..4 run function nahas:fx/thunder_far
execute if score #r nh_story matches 5..8 run function nahas:fx/whisper
execute if score #r nh_story matches 9..10 run function nahas:ambient/whisper_line_roll
