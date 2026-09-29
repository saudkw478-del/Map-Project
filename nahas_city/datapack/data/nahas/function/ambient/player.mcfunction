# المنفّذ: اللاعب (at @s)
execute store result score #r nh_story run random value 1..100
execute if dimension minecraft:overworld run function nahas:ambient/overworld
execute if dimension nahas:star_sea run function nahas:ambient/star_sea
execute if dimension nahas:ember run function nahas:ambient/ember
