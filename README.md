# Game of Thrones – Westeros (ماب ماينكرافت كامل)

خريطة Westeros كاملة لماينكرافت **Java Edition** (الإصدار 1.21 وما بعده)، بنفس تقسيم القصة، تلعبها مع ربعك وعيالك:
معارك بموجات أعداء وبوس في كل قلعة، أسلحة ودروع، سفر بين المواقع، وعناوين تظهر لك عند دخول كل إقليم.

![الخريطة](docs/westeros_map.png)

## صور من منظور اللاعب

> هذي **رسومات (renders) من مجسّم سوّيته أنا يقرأ العالم اللي ولّدته**، بألوان وأنسجة تقريبية وبدون لقطات حقيقية من ماينكرافت،
> فالشكل الحقيقي داخل اللعبة بيكون أنعم (إضاءة وأنسجة ماينكرافت الأصلية). الغرض منها إنك تشوف التصميم والأماكن.

| | |
|---|---|
| ![](docs/screenshots/01_winterfell_spawn.jpg) نقطة البداية: فناء Winterfell | ![](docs/screenshots/04_throne_room.jpg) قاعة العرش في King's Landing |
| ![](docs/screenshots/05_wall_from_castle_black.jpg) الجدار من سطح Castle Black | ![](docs/screenshots/06_atop_the_wall.jpg) فوق الجدار |
| ![](docs/screenshots/03_night_battle.jpg) معركة عند الغروب من فوق السور | ![](docs/screenshots/10_iron_throne.jpg) العرش الحديدي |
| ![](docs/screenshots/11_godswood_weirwood.jpg) شجرة الـ Weirwood في الـ Godswood | ![](docs/screenshots/16_highgarden.jpg) Highgarden |
| ![](docs/screenshots/17_sunspear.jpg) Sunspear | ![](docs/screenshots/18_casterly_rock.jpg) Casterly Rock |
| ![](docs/screenshots/08_kings_landing.jpg) King's Landing من طريق الملك | ![](docs/screenshots/09_eyrie.jpg) The Eyrie فوق جبلها |
| ![](docs/screenshots/villagers_lineup.jpg) القرويين بلبس Westeros | ![](docs/screenshots/villager_north.jpg) الشمال (Stark) وحرس الليل |

## القرويين (لبس Westeros + سلوك ذكي مبرمج)

- **اللبس:** حزمة موارد (`GoT_Villagers_ResourcePack.zip`) تبدّل شكل القرويين: فراء رمادي للشمال (Stark)، أسود وذهبي لحرس الليل وStormlands، أزرق للأنهار (Tully)، قرمزي وذهبي لـ Lannister وأراضي التاج، برتقالي لـ Dorne، أخضر للـ Reach (Tyrell)، أسمال زيتونية لأهل العنق.
  تُحمَّل تلقائيًا مع العالم في اللعب الفردي، وإذا ما ظهرت فعّلها من *Options ← Resource Packs* (المثبّت ينسخها لمجلد الحزم).
- **الوجود:** القلاع فيها 6 قرويين لكل قلعة، وفي القرى والموانئ (White Harbor, Lannisport, Oldtown …) قرويين قرب الأبواب. يظهرون تلقائيًا لما تقترب منهم، ولا يموتون (لأنهم للزينة والقصة).
- **الكلام:** اضغط بزر الفأرة الأيمن على أي قروي يرد عليك بجملة من قصة بيته (لكل بيت 5 جمل فيها تلميحات للعب)، وأحيانًا يعطيك مؤونة (مرة كل دقيقتين تقريبًا).
- **بخصوص الذكاء الاصطناعي:** ما أقدر أحط ذكاء اصطناعي حقيقي (مثل Claude) داخل ماينكرافت العادي، لأنه ما يقدر يتصل بالإنترنت ولا ينفّذ نماذج لغوية.
  اللي سويته سلوك مبرمج: حركة القرويين الطبيعية بذكاء ماينكرافت الأصلي، وردودهم حسب بيتهم، وهدايا عشوائية. الذكاء الاصطناعي الحقيقي ممكن مستقبلًا لكن يحتاج سيرفر Paper مع إضافة (plugin) ومفتاح API ومصاريف استخدام.

> ملاحظة صريحة: بيئة التطوير اللي بنيت فيها هذا المشروع ما تقدر تشغّل ماينكرافت ولا تدخل CurseForge،
> فما جرّبت العالم داخل اللعبة بنفسي. اللي تحققت منه: العالم انقرأ من جديد بقارئ مستقل،
> وكل أوامر الـ datapack اجتازت فاحص الصياغة `mecha`، وكل أسماء البلوكات والعناصر والكيانات موجودة في
> ماينكرافت من 1.20.1 إلى 26.1. إذا طلع أي خطأ أو رسالة غريبة، انسخها وأرسلها لي وأصلحها.

## الخطوة الوحيدة اللي عليك (Windows)

1. نزّل الملف `dist/GoT_Westeros_Install.zip` من هذا المستودع، فكّ الضغط، وانقر مرتين على **`Install_Windows.bat`**.
2. افتح ماينكرافت Java (1.21+) ← **Singleplayer** ← **Game of Thrones – Westeros** ← العب.

(Mac / Linux: شغّل `install_mac_linux.sh` بدل الـ bat.)

إذا طلعت رسالة *"This world was saved in an older version"* اضغط **Play / Load** — طبيعي، لأن العالم مكتوب بصيغة 1.20.1 واللعبة تحدّثه تلقائيًا.
وإذا طلعت رسالة عن الـ datapack ("made for a different version") اضغط **Yes / Continue**.

## تفتحها لربعك

| الطريقة | الخطوات |
|---|---|
| **نفس الشبكة (الأسهل)** | ادخل العالم ← `Esc` ← **Open to LAN** ← فعّل **Allow Cheats: ON** ← **Start LAN World**. ربعك على نفس الواي فاي يشوفونه في **Multiplayer**. |
| **Aternos (سيرفر مجاني)** | سوّ سيرفر Java ← ارفع `dist/GoT_Westeros_Server_World.zip` (فك الضغط وارفع مجلد `world` بمحتوياته في مجلد العالم). الـ datapack جاهز داخله. |
| **سيرفرك الخاص (Docker)** | ضع مجلد العالم باسم `world` جنب `server/docker-compose.yml` ثم `docker compose up -d`. |

## طريقة اللعب

كل الأوامر تشتغل من الدردشة، وحتى للاعبين اللي ما هم أدمن:

| الأمر | وظيفته |
|---|---|
| `/trigger got_go` | قائمة السفر، ثم `/trigger got_go set 6` مثلًا للانتقال إلى King's Landing |
| `/trigger got_battle` | يبدأ معركة القلعة اللي واقف داخلها |
| `/trigger got_battle set 2` | يوقف المعركة |
| `/trigger got_kit` | يعطيك أسلحتك ودروعك من جديد (`set 2` = جناحين وحصان للتنقل) |
| `/function got:help` | ملخص الأوامر (للأدمن) |

أول ما تدخل العالم تجد نفسك في **Winterfell** ومعك عدّة كاملة: سيف Valyrian، قوس Dragonglass، Scorpion Crossbow، درع، ودرع Kingsguard. وفي كل قلعة **مخزن أسلحة** (الفناء الغربي) فيه صناديق بأسلحة ودروع أقوى: Longclaw وIce وNeedle، أدرع Lannister وNight's Watch وTargaryen، رمح Kraken وغيرها.

### المعارك (الترتيب المقترح للقصة)

كل معركة موجات أعداء تتصاعد ثم بوس نهائي، وتعطيك مكافآت بين الموجات. عدد الأعداء يزيد مع عدد اللاعبين.

1. **Castle Black** – الـ Wildlings يهاجمون الجدار
2. **Riverrun** – خيانة الـ Freys
3. **King's Landing** – معركة Blackwater، النار الخضراء (Creepers)
4. **Casterly Rock** – الأسد لا ينسى
5. **Highgarden** – ورود Tyrell المسمومة
6. **Storm's End** – العاصفة و Stannis
7. **The Eyrie** – قلعة فوق الجبل (3 موجات، ابدأ المعركة وأنت على الهضبة)
8. **Sunspear** – أفاعي الرمل
9. **Winterfell** – **الليل الطويل**: 7 موجات، والنهاية **Night King** (Wither)

> نصيحة: خلّ اللاعبين على الأسوار وفوق البوابة بالأقواس، والباقي بالسيوف في الفناء.

### أرقام السفر

`/trigger got_go set N`

| N | المكان | N | المكان |
|---|---|---|---|
| 2 | Castle Black | 11 | قمة الجدار |
| 3 | Winterfell | 12 | ما وراء الجدار |
| 4 | Riverrun | 13 | Moat Cailin |
| 5 | The Eyrie | 14 | The Twins |
| 6 | King's Landing | 15 | Harrenhal |
| 7 | Casterly Rock | 16 | Dragonstone |
| 8 | Highgarden | 17 | Pyke (جزر الحديد) |
| 9 | Storm's End | 18 | Oldtown – برج Hightower |
| 10 | Sunspear | 19 | White Harbor |

## الأقاليم

عند دخول كل إقليم يظهر عنوانه وشعاره: **ما وراء الجدار، الشمال، العنق، جزر الحديد، الأنهار، الوادي، الغرب، أراضي التاج، الأمطار، الريتش، دورن**.
لكل إقليم تضاريسه: ثلج وغابات صنوبر في الشمال، مستنقعات العنق، جبال Eyrie وMountains of the Moon، أنهار Trident وMander، غابة Kingswood، زهور الريتش، صحراء وجبال دورن الحمراء.
والجدار الجليدي طوله 256 بلوك وارتفاعه 78، عليه سلالم وبوابة نفق عند Castle Black.

## فحص سريع إن كل شي شغّال

داخل اللعبة (وأنت قرب Winterfell) اكتب: `/function got:selftest` — يطبع لك `[OK]` أو `[FAIL]` لكل جزء (الـ datapack، الـ loot، الخريطة، مخزن الأسلحة).

## للمطوّرين

```
tools/world/   مولّد العالم (تضاريس، أقاليم، أنهار، طرق، أشجار، معالم) + كاتب ملفات Anvil و level.dat
tools/castle.py  قالب القلعة (يقبل ألوان كل بيت)   tools/game.py  المعارك/الموجات/الأسلحة/السفر
tools/generate.py  يولّد الـ datapack   tools/package.py  يبني كل شي ويطلّع الـ zip في dist/
tools/render/     مجسّم الصور من منظور اللاعب (يقرأ العالم مباشرة)   tools/villagers/  رسم لبس القرويين + حزمة الموارد
tools/validate_names.py  يتحقق من أسماء البلوكات/العناصر مقابل سجلات ماينكرافت
datapack/got_castle/  الـ datapack المولّد    world/GoT_Westeros/  العالم المولّد
```

لإعادة البناء: `python3 tools/package.py` (يحتاج `numpy`, `scipy`, `Pillow`).
الـ datapack يشتغل أيضًا لحاله في أي عالم: `/function got:build` يبني قلعة واحدة مكانك، ثم `/function got:game/start`.
