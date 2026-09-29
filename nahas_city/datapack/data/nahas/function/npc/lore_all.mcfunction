# مكافأة جمع كل الأسرار (تعتمد على جدول nahas:gift/traveler من CORE)
tellraw @a [{"selector":"@s","color":"yellow"},{"text":" جمع كل أسرار الحجارة الثمانية! الجني الحكيم يمنحه هديّة.","color":"gold"}]
loot give @s loot nahas:gift/traveler
execute at @s run function nahas:fx/seal_burst
