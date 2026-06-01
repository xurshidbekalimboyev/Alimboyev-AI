import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# ==================== INGLIZ TILI MA'LUMOTLARI ====================

grammar_topics = {
    "present_simple": {
        "name": "Present Simple",
        "text": """📚 *PRESENT SIMPLE*

✅ *Ishlatilishi:*
• Odatiy, takrorlanuvchi harakatlar
• Doim to'g'ri bo'lgan faktlar
• Jadvallar va dasturlar

📝 *Formula:*
• (+) S + V(s/es) → I work / She works
• (-) S + don't/doesn't + V → I don't work / She doesn't work
• (?) Do/Does + S + V? → Do you work? / Does she work?

💡 *Signal so'zlar:*
always, usually, often, sometimes, never, every day/week/month

📖 *Misollar:*
• I go to school every day. (Men har kuni maktabga boraman)
• She doesn't like coffee. (U qahva yoqtirmaydi)
• Do they speak English? (Ular inglizcha gaplashadimi?)"""
    },
    "past_simple": {
        "name": "Past Simple",
        "text": """📚 *PAST SIMPLE*

✅ *Ishlatilishi:*
• O'tmishda tugagan harakatlar
• Aniq vaqtda bo'lgan voqealar
• Ketma-ket bo'lgan harakatlar

📝 *Formula:*
• (+) S + V2(ed) → I worked / She went
• (-) S + didn't + V → I didn't work / She didn't go
• (?) Did + S + V? → Did you work? / Did she go?

💡 *Signal so'zlar:*
yesterday, last week/month/year, ago, in 2020, then

📖 *Misollar:*
• I watched TV yesterday. (Men kecha TV ko'rdim)
• She didn't come to school. (U maktabga kelmadi)
• Did you eat breakfast? (Nonushta qildingizmi?)"""
    },
    "past_continuous": {
        "name": "Past Continuous",
        "text": """📚 *PAST CONTINUOUS*

✅ *Ishlatilishi:*
• O'tmishda davom etayotgan harakat
• Boshqa harakat bo'layotganda davom etgan harakat
• Parallel harakatlar

📝 *Formula:*
• (+) S + was/were + V-ing → I was working / They were playing
• (-) S + wasn't/weren't + V-ing → I wasn't working
• (?) Was/Were + S + V-ing? → Were you working?

💡 *Signal so'zlar:*
while, when, at that moment, at 5 o'clock yesterday

📖 *Misollar:*
• I was sleeping when she called. (U qo'ng'iroq qilganida men uxlayotgandim)
• They were playing football at 3 pm. (Soat 3da futbol o'ynashayotgan edi)
• Was he working yesterday? (U kecha ishlamayotgan edimi?)"""
    },
    "present_continuous": {
        "name": "Present Continuous",
        "text": """📚 *PRESENT CONTINUOUS*

✅ *Ishlatilishi:*
• Hozir sodir bo'layotgan harakatlar
• Vaqtincha harakatlar
• Rejalashtirilgan kelajak

📝 *Formula:*
• (+) S + am/is/are + V-ing → I am working / She is playing
• (-) S + am/is/are + not + V-ing → I'm not working
• (?) Am/Is/Are + S + V-ing? → Are you working?

💡 *Signal so'zlar:*
now, at the moment, currently, right now, today, tonight

📖 *Misollar:*
• I am studying English now. (Men hozir ingliz tili o'qiyapman)
• She is not watching TV. (U TV ko'rmayapti)
• Are they playing outside? (Ular tashqarida o'ynayaptimi?)"""
    },
    "future_simple": {
        "name": "Future Simple",
        "text": """📚 *FUTURE SIMPLE*

✅ *Ishlatilishi:*
• Kelajakdagi rejalashtirilmagan harakatlar
• Va'dalar
• Taxminlar va bashoratlar

📝 *Formula:*
• (+) S + will + V → I will work / She will go
• (-) S + won't + V → I won't work / She won't go
• (?) Will + S + V? → Will you work? / Will she go?

💡 *Signal so'zlar:*
tomorrow, next week/month/year, soon, in the future, someday

📖 *Misollar:*
• I will call you tomorrow. (Men ertaga seni chaqiraman)
• She won't come to the party. (U ziyofatga kelmaydi)
• Will they help us? (Ular bizga yordam beradimi?)"""
    },
    "present_perfect": {
        "name": "Present Perfect",
        "text": """📚 *PRESENT PERFECT*

✅ *Ishlatilishi:*
• Natijasi hozirga ta'sir qilgan o'tgan harakat
• Hayotda tajriba
• Hozirgacha davom etayotgan holat

📝 *Formula:*
• (+) S + have/has + V3 → I have worked / She has gone
• (-) S + haven't/hasn't + V3 → I haven't worked
• (?) Have/Has + S + V3? → Have you worked?

💡 *Signal so'zlar:*
already, yet, just, ever, never, recently, since, for

📖 *Misollar:*
• I have already eaten. (Men allaqachon yedim)
• She has never been to London. (U hech qachon Londonda bo'lmagan)
• Have you ever seen a lion? (Siz hech qachon sher ko'rganmisiz?)"""
    },
    "past_perfect": {
        "name": "Past Perfect",
        "text": """📚 *PAST PERFECT*

✅ *Ishlatilishi:*
• O'tmishdagi boshqa harakatdan oldin tugagan harakat
• O'tmishdagi harakatlar tartibini ko'rsatish

📝 *Formula:*
• (+) S + had + V3 → I had worked / She had gone
• (-) S + hadn't + V3 → I hadn't worked
• (?) Had + S + V3? → Had you worked?

💡 *Signal so'zlar:*
before, after, when, already, by the time, never

📖 *Misollar:*
• I had eaten before she came. (U kelishidan oldin men yegandim)
• She hadn't finished work when he called. (U qo'ng'iroq qilganida ish tugamagan edi)
• Had they left before you arrived? (Siz kelishingizdan oldin ular ketgan edimi?)"""
    },
    "future_continuous": {
        "name": "Future Continuous",
        "text": """📚 *FUTURE CONTINUOUS*

✅ *Ishlatilishi:*
• Kelajakda ma'lum vaqtda davom etadigan harakat
• Rejalashtirilgan kelajak harakatlar

📝 *Formula:*
• (+) S + will be + V-ing → I will be working / She will be playing
• (-) S + won't be + V-ing → I won't be working
• (?) Will + S + be + V-ing? → Will you be working?

💡 *Signal so'zlar:*
at this time tomorrow, next week at 5, all day tomorrow

📖 *Misollar:*
• I will be sleeping at midnight. (Yarim tunda men uxlayotgan bo'laman)
• She will be working all day tomorrow. (U ertaga kun bo'yi ishlayotgan bo'ladi)
• Will they be waiting for us? (Ular bizni kutayotgan bo'ladimi?)"""
    },
    "present_perfect_continuous": {
        "name": "Present Perfect Continuous",
        "text": """📚 *PRESENT PERFECT CONTINUOUS*

✅ *Ishlatilishi:*
• O'tmishda boshlangan va hozir davom etayotgan harakat
• Uzoq davom etgan harakatning natijasi

📝 *Formula:*
• (+) S + have/has been + V-ing → I have been working
• (-) S + haven't/hasn't been + V-ing
• (?) Have/Has + S + been + V-ing?

💡 *Signal so'zlar:*
for, since, how long, all day, lately, recently

📖 *Misollar:*
• I have been studying for 3 hours. (Men 3 soatdan beri o'qiyapman)
• She has been living here since 2020. (U 2020 yildan beri bu yerda yashayapti)
• How long have you been waiting? (Necha vaqtdan beri kutayapsiz?)"""
    },
    "past_perfect_continuous": {
        "name": "Past Perfect Continuous",
        "text": """📚 *PAST PERFECT CONTINUOUS*

✅ *Ishlatilishi:*
• O'tmishdagi boshqa harakatdan oldin davom etgan harakat

📝 *Formula:*
• (+) S + had been + V-ing → I had been working
• (-) S + hadn't been + V-ing
• (?) Had + S + been + V-ing?

💡 *Signal so'zlar:*
for, since, before, when, how long

📖 *Misollar:*
• I had been working for 5 hours when she arrived. (U kelganida men 5 soatdan beri ishlayotgandim)
• They had been playing before it rained. (Yomg'ir yog'ishidan oldin ular o'ynayotgan edi)"""
    },
    "future_perfect": {
        "name": "Future Perfect",
        "text": """📚 *FUTURE PERFECT*

✅ *Ishlatilishi:*
• Kelajakda ma'lum vaqtga qadar tugallanadigan harakat

📝 *Formula:*
• (+) S + will have + V3 → I will have finished
• (-) S + won't have + V3
• (?) Will + S + have + V3?

💡 *Signal so'zlar:*
by tomorrow, by next week, by 5 o'clock, before

📖 *Misollar:*
• I will have finished by tomorrow. (Men ertaga qadar tugatayman)
• She will have left before you arrive. (Siz kelishingizdan oldin u ketgan bo'ladi)"""
    },
    "conditionals": {
        "name": "Conditionals (Shartli gaplar)",
        "text": """📚 *CONDITIONALS — SHARTLI GAPLAR*

✅ *0-shart (Doim to'g'ri):*
If + Present Simple, Present Simple
• If you heat water to 100°C, it boils.

✅ *1-shart (Real kelajak):*
If + Present Simple, will + V
• If it rains, I will stay home.

✅ *2-shart (Xayoliy hozir):*
If + Past Simple, would + V
• If I were rich, I would travel the world.

✅ *3-shart (O'tmish xayoli):*
If + Past Perfect, would have + V3
• If I had studied, I would have passed.

📖 *Misollar:*
• If I have time, I will help you. (Vaqtim bo'lsa, yordam beraman)
• If I were you, I would study more. (Men siz bo'lganimda ko'proq o'qirdim)"""
    },
    "passive_voice": {
        "name": "Passive Voice (Noaniq nisbat)",
        "text": """📚 *PASSIVE VOICE — NOANIQ NISBAT*

✅ *Ishlatilishi:*
• Kim bajarganini bilmaymiz yoki muhim emas
• Rasmiy uslub

📝 *Formula:*
• am/is/are/was/were + V3

💡 *Asosiy zamonlar:*
• Present: The book is written. (Kitob yozilmoqda)
• Past: The book was written. (Kitob yozildi)
• Future: The book will be written. (Kitob yoziladi)
• Present Perfect: The book has been written. (Kitob yozilgan)

📖 *Misollar:*
• English is spoken all over the world. (Ingliz tili butun dunyoda gapiriladI)
• The letter was sent yesterday. (Xat kecha yuborildi)
• The house will be built next year. (Uy kelasi yil quriladi)"""
    },
    "modal_verbs": {
        "name": "Modal Verbs (Modal fe'llar)",
        "text": """📚 *MODAL VERBS — MODAL FE'LLAR*

✅ *Can* — qila olish, ruxsat
• I can swim. (Men suzа olaman)
• Can I help you? (Sizga yordam bera olamanmi?)

✅ *Could* — o'tmishda qila olish, so'roq
• I could run fast when I was young.

✅ *Must* — majburiyat
• You must wear a seatbelt. (Siz kamar takishingiz shart)

✅ *Should* — maslahat
• You should study more. (Ko'proq o'qishingiz kerak)

✅ *May/Might* — ehtimol
• It may rain today. (Bugun yomg'ir yog'ishi mumkin)

✅ *Will/Would* — kelajak, so'roq
• Would you like some tea? (Choy ichasizmi?)

✅ *Shall* — taklif
• Shall we dance? (Raqsga tushamizmi?)"""
    },
}

# ==================== O'ZBEKISTON KONSTITUTSIYASI ====================

constitution = {
    1: "O'zbekiston Respublikasi — suveren demokratik respublika. O'zbekiston Respublikasining davlat tuzumi fuqarolik tinchligini, milliy totuvlikni va xalqlar do'stligini ta'minlash asosida quriladi.",
    2: "Davlat o'z faoliyatida xalqning manfaatlarini ifoda etadi va amalga oshiradi. Davlat organlari va mansabdor shaxslar jamiyat va fuqarolar oldida mas'uldirlar.",
    3: "O'zbekiston Respublikasining davlat tili o'zbek tilidir. O'zbekiston Respublikasi o'z hududida yashovchi barcha millat va elatlarning tillari, urf-odatlari va an'analari hurmat qilinishini ta'minlaydi hamda ularning rivojlanishi uchun sharoit yaratadi.",
    4: "O'zbekiston Respublikasining davlat ramzlari — Bayroq, Gerb va Madhiya. Ularning tavsifi va rasmiy foydalanish tartibi qonun bilan belgilanadi.",
    5: "O'zbekiston Respublikasi o'z hududida yagona davlat hokimiyatini amalga oshiradi. Qoraqalpog'iston Respublikasi O'zbekiston Respublikasi tarkibiga kiradi.",
    6: "O'zbekiston Respublikasida davlat hokimiyati xalq manfaatlarini ko'zlab, faqat O'zbekiston Respublikasi Konstitutsiyasi va qonunlari asosida amalga oshiriladi.",
    7: "Xalq davlat hokimiyatining birdan-bir manbaidir. Davlat hokimiyati xalq nomidan faqat u tomonidan saylanadigan va saylangan vakillardan tashkil topadigan Oliy Majlis tomonidan amalga oshiriladi.",
    8: "O'zbekiston xalqi o'zbek, qoraqalpoq, rus, ukrain, qozoq, tojik, qirg'iz, turkman va boshqa millat va elat vakillari bilan birgalikda yashaydigan fuqarolardan iborat.",
    9: "Siyosiy hayotning turli-tumanligi, ko'ppartiyaviylik tan olinadi. Siyosiy partiyalar O'zbekiston Respublikasi Konstitutsiyasi va qonunlariga muvofiq tashkil etiladi va faoliyat yuritadi.",
    10: "Jamoat birlashmalari O'zbekiston Respublikasi Konstitutsiyasi va qonunlariga muvofiq tashkil etiladi va faoliyat yuritadi. Davlat jamoat birlashmalari faoliyatiga aralashmasligi, shuningdek, jamoat birlashmalari davlat organlari faoliyatiga aralashmasligi kerak.",
    11: "O'zbekiston Respublikasi tashqi siyosatni davlatlarning suveren tengligi, kuch ishlatmaslik yoki kuch bilan tahdid qilmaslik, chegaralar daxlsizligi, nizolarni tinch yo'l bilan hal etish, boshqa davlatlarning ichki ishlariga aralashmaslik prinsiplari asosida amalga oshiradi.",
    12: "O'zbekiston Respublikasida ijtimoiy hayot siyosiy institutlar, mafkuralar va fikrlarning xilma-xilligi asosida rivojlanadi. Hech qaysi mafkura davlat mafkurasi sifatida o'rnatilishi mumkin emas.",
    13: "O'zbekiston Respublikasida demokratiya umuminsoniy prinsiplarga asoslanadi, ularga ko'ra inson, uning hayoti, erkinligi, sha'ni, qadr-qimmati va boshqa ajralmas huquqlari oliy qadriyat hisoblanadi.",
    14: "Davlat o'z vazifalarini boshqaruv, ijroiya va sud hokimiyatining bo'linishi prinsipiga muvofiq amalga oshiradi.",
    15: "O'zbekiston Respublikasida O'zbekiston Respublikasi Konstitutsiyasi va qonunlarining ustuvorligi so'zsiz tan olinadi. Davlat, uning organlari, mansabdor shaxslar, jamoat birlashmalari, fuqarolar Konstitutsiya va qonunlarga muvofiq ish tutishlari shart.",
    16: "O'zbekiston Respublikasi Konstitutsiyasining hech bir qoidasi Konstitutsiyada mustahkamlangan fuqarolarning huquq va erkinliklarini cheklash maqsadida talqin etilishi mumkin emas.",
    17: "O'zbekiston Respublikasi o'z hududida joylashgan barcha fuqarolarga, korxonalarga, muassasalarga, tashkilotlarga, siyosiy partiyalarga, boshqa jamoat birlashmalariga nisbatan xalqaro huquqning umume'tirof etilgan normalarini va tamoyillarini hurmat qiladi.",
    18: "O'zbekiston Respublikasining barcha fuqarolari bir xil huquq va erkinliklarga ega bo'lib, jinsi, irqi, millati, tili, dini, ijtimoiy kelib chiqishi, e'tiqodi, shaxsiy va ijtimoiy mavqeidan qat'i nazar, qonun oldida tengdirlar.",
    19: "Fuqaroning huquqlari va erkinliklari, shuningdek uning burchlari Konstitutsiya va qonunlarda belgilanadi. Fuqarolarning huquq va erkinliklari o'zgalarning huquqlari, qonun va qonunosti hujjatlar bilan belgilangan majburiyatlar tomonidan cheklanishi mumkin.",
    20: "Fuqarolarning huquq va erkinliklari faqat boshqalarning huquqlari va erkinliklarini hamda demokratik jamiyat asoslarini himoya qilish maqsadida, qonunda belgilangan holatlardagina cheklanishi mumkin.",
    21: "O'zbekiston Respublikasi o'z fuqarolarini chet davlatlar hududida ham himoya qiladi va ularning homiyligini ta'minlaydi.",
    22: "O'zbekiston Respublikasi o'z fuqarosini boshqa davlatga bermaslik kafolatini beradi.",
    23: "O'zbekiston Respublikasi chet el fuqarolariga va fuqaroligi bo'lmagan shaxslarga xalqaro huquq normalariga muvofiq siyosiy boshpana berishi mumkin.",
    24: "Hayot huquqi har bir inson uchun ajralmas huquqdir. Odamni hayotdan mahrum etishga faqat sud tomonidan sud jarayoni asosida belgilangan tartibda qoʻllanilishi mumkin bo'lgan qonuniy jazo sifatida yoʻl qoʻyilishi mumkin.",
    25: "Har kim erkinlik va shaxsiy daxlsizlik huquqiga ega. Qonunda belgilangan asoslar va tartibdan tashqari hech kim hibsga olinishi yoki qamoqqa olinishi mumkin emas.",
    26: "Hech kim qonunda belgilangan tartibda va asosdan tashqari jinoiy javobgarlikka tortilishi mumkin emas. Hech kim jinoiy javobgarlikka tortilishiga sabab bo'lgan aybini isbotlash uchun o'ziga qarshi ko'rsatuv berishga majbur etilishi mumkin emas.",
    27: "Har kim o'z sha'ni va qadr-qimmatini himoya qilish huquqiga ega. Hech narsa insonning sha'ni va qadr-qimmatini kamsitish uchun asos bo'la olmaydi.",
    28: "Har kim O'zbekiston Respublikasi hududida erkin harakatlanish hamda yashash joyini tanlash huquqiga ega. Har kim O'zbekiston Respublikasidan tashqariga chiqib ketish huquqiga ega.",
    29: "Har kim fikrlash, so'z va e'tiqod erkinligi huquqiga ega. Har kim o'zi xohlagan axborotni izlash, olish va tarqatish huquqiga ega.",
    30: "Davlat organlari, jamoat birlashmalari, mansabdor shaxslar fuqarolarga ularning huquq va manfaatlarini ko'zlagan holda murojaat etish imkoniyatini ta'minlashlari shart.",
    31: "Har kim vijdon erkinligi huquqiga ega. Har kim istagan dinga e'tiqod qilish yoki hech qaysi dinga e'tiqod qilmaslik huquqiga ega.",
    32: "Fuqarolar davlat va jamiyat boshqaruvida bevosita hamda o'z vakillari orqali ishtirok etish huquqiga ega. Bunday ishtirok etish o'zini o'zi boshqarish, referendumlar o'tkazish va davlat organlarini demokratik tarzda tuzish yo'li bilan amalga oshiriladi.",
    33: "Fuqarolar qonunda belgilangan tartibda mitinglarga, yig'ilishlarga va namoyishlarga chiqish huquqiga ega.",
    34: "Fuqarolarga uyushma va kasaba uyushmalari, siyosiy partiyalar va boshqa jamoat birlashmalariga uyushish huquqi kafolat beriladi.",
    35: "Har kim mehnatkash bo'lish, erkin kasb tanlash, adolatli mehnat sharoitlarida ishlash va qonun bilan muhofaza etilish huquqiga ega.",
    36: "Har kim dam olish huquqiga ega. Mehnat munosabatlarida band bo'lgan shaxslar ish vaqtining qonunda belgilangan eng ko'p chegarasi, haftalik dam olish kunlari hamda yillik to'lanadigan ta'tillar huquqidan foydalanadilar.",
    37: "Har kim mulkdor bo'lish huquqiga ega. Mulkdor o'z mulkiga ega bo'lish, undan foydalanish va uni tasarruf etishda va bu mulkdan faqat o'zi manfaat topishida cheklanmasligi kerak.",
    38: "O'zbekiston Respublikasi fuqarolari ijtimoiy ta'minot huquqiga ega.",
    39: "Har kim malakali tibbiy xizmatdan foydalanish huquqiga ega.",
    40: "Har kim ta'lim olish huquqiga ega. Bepul umumiy ta'lim olish davlat tomonidan kafolatlanadi.",
    41: "Har kim ilmiy va texnikaviy ijod, madaniy qadriyatlardan foydalanish huquqiga ega. Davlat madaniy, ilmiy va texnikaviy rivojlanishga g'amxo'rlik qiladi.",
    42: "Har kim o'z huquqlari va erkinliklarini sud orqali himoya qilish, davlat organlari, mansabdor shaxslar, jamoat birlashmalari noqonuniy harakatlari ustidan sudga shikoyat qilish huquqiga ega.",
    43: "Davlat fuqarolarning Konstitutsiya va qonunlarda mustahkamlangan huquqlari hamda erkinliklarini ta'minlaydi.",
    44: "Fuqarolarning huquqlari buzilgan taqdirda ular qonunga muvofiq o'z huquqlarini o'zlari himoya qilish choralarini ko'rishlari mumkin.",
    45: "Fuqarolar qonunda belgilangan tartibda davlat organlariga va mansabdor shaxslarga murojaat etish huquqiga ega.",
    46: "Ayollar va erkaklar teng huquqlarga ega.",
    47: "Fuqarolar qonunda belgilangan tartibda soliq va yig'imlar to'lashlari shart.",
    48: "Fuqarolar atrof-muhitga ehtiyotkorona munosabatda bo'lishga majburdirlar.",
    49: "Davlat va jamiyat oldidagi burchlarni bajarish fuqarolar uchun majburiydir.",
    50: "Fuqarolar O'zbekiston Respublikasi Konstitutsiyasini va qonunlarini hurmat qilishlari, boshqa shaxslarning huquqlari, erkinliklari, sha'ni va qadr-qimmatini hurmat qilishlari shart.",
    51: "Konstitutsiyani va qonunlarni buzish belgilangan tartibda javobgarlikka tortishga sabab bo'ladi.",
    52: "Fuqarolar O'zbekiston Respublikasini himoya qilishga majburdirlar. Qonunda belgilangan tartibda harbiy xizmatni o'tash har bir fuqaroning burchi va majburiyatidir.",
    53: "O'zbekiston Respublikasida yer, yer osti boyliklari, suv, o'simlik va hayvonot dunyosi hamda boshqa tabiiy zahiralar umummilliy boylikdir, ulardan oqilona foydalanilishi lozim va ular davlat muhofazasidadir.",
    54: "Mulk daxlsizdir va davlat tomonidan muhofaza etiladi. Mulkdor faqat qonunda nazarda tutilgan hollarda va tartibda mulkidan mahrum etilishi mumkin.",
    55: "Yer O'zbekiston Respublikasida asosiy boylik sifatida alohida muhofaza ostiga olinadi.",
    56: "Mehnat shirkatlari, aksiyadorlik jamiyatlari, kooperativlar, xususiy korxonalar, qo'shma korxonalar, jamoat birlashmalari va boshqa tashkilotlar O'zbekiston Respublikasi qonunlarida nazarda tutilgan tartibda tashkil etiladi va faoliyat yuritadi.",
    57: "Siyosiy partiyalar va boshqa jamoat birlashmalari o'z ustavi va dasturlari asosida faoliyat yuritadilar.",
    58: "Davlat jamoat birlashmalari faoliyatining qonuniyligini nazorat qiladi.",
    59: "Oliy Majlis — O'zbekiston Respublikasining oliy vakillik organi bo'lib, qonun chiqaruvchi hokimiyatni amalga oshiradi.",
    60: "Oliy Majlis ikki palatadan — Qonunchilik palatasi (quyi palata) va Senat (yuqori palata)dan iborat.",
    61: "Qonunchilik palatasi a'zolari (deputatlar) to'rt yil muddatga saylanadi. Qonunchilik palatasi yuz o'n besh deputatdan iborat.",
    62: "Senat yuqori palata bo'lib, unga a'zolik — senatorlik to'rt yil muddatga amalga oshiriladi.",
    63: "Oliy Majlis deputatlarining daxlsizligi qonunda belgilab qo'yiladi.",
    64: "Oliy Majlisning vakolatlari qonunda belgilanadi.",
    65: "O'zbekiston Respublikasi Prezidenti davlat boshlig'i va ijroiya hokimiyatining rahbaridir.",
    66: "O'zbekiston Respublikasining Prezidenti O'zbekiston Respublikasi fuqarosi bo'lgan, o'ttiz besh yoshdan kichik bo'lmagan, davlat tilini yaxshi biladigan, bevosita saylovdan oldin kamida o'n yil O'zbekiston hududida muqim yashaган hamda fuqarolik huquqiga ega bo'lgan shaxs bo'lishi mumkin.",
    67: "Prezident umumiy, teng va to'g'ridan-to'g'ri saylov huquqi asosida yashirin ovoz berish yo'li bilan besh yil muddatga saylanadi.",
    68: "Prezidentning vakolatlari qonunda belgilanadi.",
    69: "O'zbekiston Respublikasi Prezidenti O'zbekiston Respublikasi qurolli kuchlarining Oliy Bosh qo'mondonidir.",
    70: "Prezident davlat ramzlarini tasdiqlaydi.",
    71: "Vazirlar Mahkamasi ijroiya hokimiyatini amalga oshiradi.",
    72: "Vazirlar Mahkamasi O'zbekiston Respublikasi Prezidenti rahbarligida ish olib boradi.",
    73: "Vazirlar Mahkamasi Oliy Majlis oldida hisob beradi.",
    74: "Vazirlar Mahkamasi O'zbekiston Respublikasi iqtisodiyotining, ijtimoiy va ma'naviy sohaning samarali faoliyat ko'rsatishiga, qonunlarning ijro etilishiga rahbarlik qiladi.",
    75: "O'zbekiston Respublikasi hududida mahalliy davlat hokimiyatini viloyatlar, tumanlar, shaharlar (viloyatga bo'ysunuvchi shaharlar)da Kengashlar va hokimlar amalga oshirishadi.",
    76: "Viloyat, tuman, shahar hokimlari tegishli hududda ijroiya hokimiyatini amalga oshiradi.",
    77: "Mahalliy kengashlar va hokimlar o'z vakolatlarini Konstitutsiya va qonunlar doirasida amalga oshiradilar.",
    78: "Sud hokimiyati qonun chiqaruvchi va ijroiya hokimiyatidan mustaqil holda amalga oshiriladi.",
    79: "Sudyalar mustaqildir, faqat qonunga bo'ysunadilar.",
    80: "Sudyalar daxlsizdir va ularga nisbatan jinoiy javobgarlik faqat qonunda belgilangan asoslar va tartibda qo'llanilishi mumkin.",
    81: "O'zbekiston Respublikasining sud tizimi O'zbekiston Respublikasi Konstitutsiyaviy sudi, O'zbekiston Respublikasi Oliy sudi, O'zbekiston Respublikasi Oliy xo'jalik sudidan iborat.",
    82: "O'zbekiston Respublikasi Konstitutsiyaviy sudi O'zbekiston Respublikasi Konstitutsiyasiga rioya etilishi ustidan nazoratni amalga oshiradi.",
    83: "O'zbekiston Respublikasi Oliy sudi fuqarolik, jinoyat va ma'muriy sud ishlarini ko'rib chiqishda oliy sud organi hisoblanadi.",
    84: "O'zbekiston Respublikasi Oliy xo'jalik sudi xo'jalik nizolarini ko'rib chiqishda oliy sud organi hisoblanadi.",
    85: "Prokuratura O'zbekiston Respublikasida qonunlarning aniq va bir xilda bajarilishi ustidan oliy nazoratni amalga oshiradi.",
    86: "O'zbekiston Respublikasi Bosh prokurori Oliy Majlis tomonidan tayinlanadi.",
    87: "O'zbekiston Respublikasining moliya-kredit tizimi O'zbekiston Respublikasi Markaziy banki, banklar, boshqa kredit tashkilotlari, shuningdek moliya muassasalaridan iborat.",
    88: "Soliqlar va boshqa majburiy to'lovlar faqat qonun bilan belgilanadi.",
    89: "O'zbekiston Respublikasining Davlat byudjeti Vazirlar Mahkamasi tomonidan tuziladi va Oliy Majlis tomonidan tasdiqlanadi.",
    90: "O'zbekiston Respublikasining milliy valyutasi so'mdir.",
    91: "O'zbekiston Respublikasida qo'shilma xo'jalik yuritish shakllaridan va xorijiy investitsiyalardan foydalanish qonun tomonidan kafolatlanadi.",
    92: "O'zbekiston Respublikasida mudofaa, davlat xavfsizligi va qonunchilikni muhofaza qilish uchun qurolli kuchlar va boshqa qo'shinlar tuziladi.",
    93: "O'zbekiston Respublikasining qurolli kuchlari davlatning suverenitetini, hududiy yaxlitligini va konstitutsiyaviy tuzumini himoya qilish uchun tashkil etiladi.",
    94: "O'zbekiston Respublikasi Konstitutsiyasi O'zbekiston Respublikasining Oliy qonunidir.",
    95: "O'zbekiston Respublikasi hududida O'zbekiston Respublikasi Konstitutsiyasi va qonunlarining ustuvorligi so'zsiz tan olinadi.",
    96: "Konstitutsiyaga o'zgartishlar va qo'shimchalar O'zbekiston Respublikasi Oliy Majlisi tomonidan kiritiladi.",
    97: "O'zbekiston Respublikasi Konstitutsiyasiga o'zgartish kiritish to'g'risidagi qonunlar umumiy ovozlar sonining kamida uchdan ikki qismi bilan qabul qilinadi.",
    98: "O'zbekiston Respublikasining davlat ramzlari — Bayroq, Gerb va Madhiya davlat symbols hisoblanadi.",
    99: "O'zbekiston Respublikasining poytaxti Toshkent shahridir.",
    100: "O'zbekiston Respublikasi Konstitutsiyasi referendum orqali qabul qilinadi va kuchga kiradi.",
    101: "Qoraqalpog'iston Respublikasi O'zbekiston Respublikasi tarkibiga kiradi va o'z Konstitutsiyasiga ega.",
    102: "Qoraqalpog'iston Respublikasining davlat tili o'zbek va qoraqalpoq tillaridir.",
    103: "Qoraqalpog'iston Respublikasining poytaxti No'kis shahridir.",
    104: "Qoraqalpog'iston Respublikasi o'z hududida O'zbekiston Respublikasi Konstitutsiyasi va qonunlariga muvofiq hokimiyatni amalga oshiradi.",
    105: "Viloyatlar, tumanlar va shaharlar O'zbekiston Respublikasining ma'muriy-hududiy birliklaridir.",
    106: "O'zbekiston Respublikasining ma'muriy-hududiy tuzilishi qonun bilan belgilanadi.",
    107: "Fuqarolar o'zini o'zi boshqarish organlariga saylanish va saylov organlariga ega bo'lish huquqiga ega.",
    108: "O'zini o'zi boshqarish organlari mahalla qo'mitalaridan iborat bo'lib, ular fuqarolarning turmush va maishiy muammolarini hal qilishda ishtirok etadilar.",
    109: "Davlat o'zini o'zi boshqarish organlarining faoliyatini qo'llab-quvvatlaydi.",
    110: "Referendum — fuqarolarning eng muhim davlat va jamoat hayoti masalalarini bevosita hal etish shaklidir.",
    111: "Referendumga O'zbekiston Respublikasining saylov huquqiga ega bo'lgan fuqarolari qatnashishi mumkin.",
    112: "Referendum O'zbekiston Respublikasi Prezidenti yoki Oliy Majlisning qarori bilan o'tkaziladi.",
    113: "Referendumning natijalari rasmiy e'lon qilinadi va ular O'zbekiston Respublikasi hududida majburiy kuchga ega.",
    114: "O'zbekiston Respublikasida qonun chiqarish tashabbusi huquqi Oliy Majlis deputatlariga, Vazirlar Mahkamasiga va Qoraqalpog'iston Respublikasining Joʻqorg'i Kengeshiga tegishlidir.",
    115: "Qonunlar Oliy Majlisda muhokama qilinadi va qabul qilinadi.",
    116: "Prezident qabul qilingan qonunni imzolaydi yoki uni rad etadi.",
    117: "Qonunlar rasmiy nashrda e'lon qilinganidan keyin kuchga kiradi.",
    118: "O'zbekiston Respublikasining xalqaro shartnomalariga nisbatan O'zbekiston Respublikasi qonunlari qo'llaniladi.",
    119: "O'zbekiston Respublikasi xalqaro huquqning umume'tirof etilgan norma va tamoyillarini tan oladi.",
    120: "O'zbekiston Respublikasi tinchliksevar tashqi siyosat yuritadi va qurolsizlanishga intilib, yadroviy qurollardan xoli zonani shakllantirishda ishtirok etadi.",
    121: "O'zbekiston Respublikasi xalqaro tashkilotlar bilan hamkorlik qiladi.",
    122: "O'zbekiston Respublikasi xalqaro kelishuvlar va shartnomalar tuzish huquqiga ega.",
    123: "O'zbekiston Respublikasi xalqaro huquqning subyekti sifatida xalqaro munosabatlarda ishtirok etadi.",
    124: "O'zbekiston Respublikasi Konstitutsiyasi O'zbekiston xalqiga hurmat va sadoqat asosida qabul qilingan.",
    125: "O'zbekiston Respublikasi Konstitutsiyasi 1992 yil 8 dekabrda qabul qilingan.",
    126: "Konstitutsiyaning talablari barcha fuqarolar, davlat organlari va mansabdor shaxslar uchun majburiydir.",
    127: "Davlat fuqarolarning huquqlarini himoya qilishda asosiy mas'uliyatni o'z zimmasiga oladi.",
    128: "Fuqarolar o'z huquqlarini himoya qilish uchun sudga murojaat etishlari mumkin.",
    129: "O'zbekiston Respublikasida inson huquqlari va erkinliklarini himoya qilish davlatning ustuvor vazifasidir.",
    130: "Barcha fuqarolar qonun oldida tengdir va tenglikda himoyalanish huquqiga ega.",
    131: "O'zbekiston Respublikasida ta'lim, fan va madaniyat rivojlantiriladi.",
    132: "Davlat yoshlarning har tomonlama rivojlanishi uchun sharoit yaratadi.",
    133: "Oila jamiyatning asosiy bo'g'inidir va davlat tomonidan muhofaza etiladi.",
    134: "Bola huquqlari qonun bilan kafolatlanadi va davlat tomonidan muhofaza etiladi.",
    135: "Keksalar va nogironlar davlat tomonidan alohida muhofaza ostiga olinadi.",
    136: "O'zbekiston Respublikasida ekologik xavfsizlik va atrof-muhitni muhofaza qilish davlatning ustuvor yo'nalishidir.",
    137: "Fuqarolar sog'lom muhitda yashash huquqiga ega va bu huquq qonun tomonidan himoya qilinadi.",
    138: "O'zbekiston Respublikasi Konstitutsiyasining qoidalari barcha fuqarolar uchun majburiy bo'lib, davlatning asosiy qonuni hisoblanadi.",
}

# ==================== MENYULAR ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇬🇧 Ingliz Tili", callback_data="english")],
        [InlineKeyboardButton("⚖️ Huquq (Konstitutsiya)", callback_data="law")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌟 *Xush kelibsiz!*\n\nQaysi bo'limni tanlaysiz?",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Bosh menyu
    if data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("🇬🇧 Ingliz Tili", callback_data="english")],
            [InlineKeyboardButton("⚖️ Huquq (Konstitutsiya)", callback_data="law")],
        ]
        await query.edit_message_text(
            "🌟 *Xush kelibsiz!*\n\nQaysi bo'limni tanlaysiz?",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # Ingliz tili menyusi
    elif data == "english":
        keyboard = []
        topics = list(grammar_topics.items())
        for i in range(0, len(topics), 2):
            row = []
            row.append(InlineKeyboardButton(topics[i][1]["name"], callback_data=f"gram_{topics[i][0]}"))
            if i + 1 < len(topics):
                row.append(InlineKeyboardButton(topics[i+1][1]["name"], callback_data=f"gram_{topics[i+1][0]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")])
        await query.edit_message_text(
            "🇬🇧 *Ingliz Tili — Grammatika*\n\nMavzuni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # Grammatika mavzusi
    elif data.startswith("gram_"):
        topic_key = data[5:]
        if topic_key in grammar_topics:
            topic = grammar_topics[topic_key]
            keyboard = [
                [InlineKeyboardButton("🔙 Grammatika", callback_data="english")],
                [InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")],
            ]
            await query.edit_message_text(
                topic["text"],
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )

    # Huquq menyusi — sahifalar
    elif data == "law" or data.startswith("law_page_"):
        page = 0
        if data.startswith("law_page_"):
            page = int(data.split("_")[-1])
        
        per_page = 20
        start_idx = page * per_page + 1
        end_idx = min(start_idx + per_page - 1, 138)
        
        keyboard = []
        modda_nums = list(range(start_idx, end_idx + 1))
        for i in range(0, len(modda_nums), 4):
            row = []
            for j in range(4):
                if i + j < len(modda_nums):
                    num = modda_nums[i + j]
                    row.append(InlineKeyboardButton(f"{num}-modda", callback_data=f"modda_{num}"))
            keyboard.append(row)
        
        nav_row = []
        if page > 0:
            nav_row.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"law_page_{page-1}"))
        if end_idx < 138:
            nav_row.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"law_page_{page+1}"))
        if nav_row:
            keyboard.append(nav_row)
        keyboard.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")])
        
        await query.edit_message_text(
            f"⚖️ *O'zbekiston Respublikasi Konstitutsiyasi*\n\n{start_idx}-{end_idx} moddalar:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # Modda ko'rsatish
    elif data.startswith("modda_"):
        num = int(data.split("_")[1])
        text = constitution.get(num, "Ma'lumot topilmadi.")
        page = (num - 1) // 20
        keyboard = [
            [InlineKeyboardButton("🔙 Moddalar", callback_data=f"law_page_{page}")],
            [InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")],
        ]
        await query.edit_message_text(
            f"⚖️ *{num}-MODDA*\n\n{text}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ Bot ishlamoqda...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
