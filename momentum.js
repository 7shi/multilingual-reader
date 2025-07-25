// Initialize datasets array if undefined
if (typeof datasets === 'undefined') {
    var datasets = [];
}

// Add momentum dataset to datasets array
datasets.push([
{
"fr": "Marie: Bienvenue dans « Bonds Quantiques », l'émission qui donne un sens à l'univers, un mystère à la fois. Je suis Marie.",
"en": "Mary: Welcome to \"Quantum Leaps,\" the show that makes sense of the universe, one puzzle at a time. I'm Mary.",
"ja": "Mary: 『量子の跳躍』へようこそ。この番組では、1つずつ謎を解きながら、宇宙の意味を明らかにします。私はメアリーです。"
},
{
"fr": "Jean: Et je suis Jean. C'est un plaisir d'être ici.",
"en": "John: And I'm John. It's a pleasure to be here.",
"ja": "John: 私はジョンです。ここに来れて光栄です。"
},
{
"fr": "Marie: Jean, aujourd'hui nous avons une question d'auditeur qui est juste... fantastique.",
"en": "Mary: John, today we've got a listener question that's just... fantastic.",
"ja": "Mary: ジョン、今日は本当に素晴らしいリスナーからの質問があります。"
},
{
"fr": "Jean: Oh?",
"en": "John: Oh?",
"ja": "John: あっ？"
},
{
"fr": "Marie: Ça touche au cœur de ce qui rend la mécanique quantique si… si étrange.",
"en": "Mary: It gets right to the core of what makes quantum mechanics so… well, so weird.",
"ja": "Mary: それは、量子力学がなぜこんなにも…不思議なのかという本質に迫っています。"
},
{
"fr": "Jean: J'adore ceux-ci. Qu'est-ce que c'est ?",
"en": "John: I love those. What is it?",
"ja": "John: それらが大好きです。何ですか？"
},
{
"fr": "Marie: Ils demandent, euh, « en mécanique quantique, on obtient le moment cinétique à partir de quelque chose appelé un « opérateur » ».",
"en": "Mary: They ask, uh, \"In quantum mechanics, you get momentum from something called an 'operator.'\"",
"ja": "Mary: 彼らは、ええと、「量子力学では、「演算子」と呼ばれるものから運動量を得る」と尋ねています。"
},
{
"fr": "Jean: D'accord",
"en": "John: Okay.",
"ja": "John: わかりました"
},
{
"fr": "Marie: Mais dans ma tête, le momentum vient de regarder quelque chose se déplacer — d’un changement de position. Comment peut-il être une chose que l’on mesure toute seule ?",
"en": "Mary: \"But in my head, momentum comes from watching something move—from a change in position. How can it be a thing you measure all by itself?\"",
"ja": "Mary: しかし、私の頭の中では、運動量は何かが動いているのを見て、位置の変化から来るものです。どうして、それが単独で測定できるものなのでしょうか？"
},
{
"fr": "Jean: C’est une question véritablement brillante.",
"en": "John: That is a truly brilliant question.",
"ja": "John: それは本当に素晴らしい質問です。"
},
{
"fr": "Marie: Vraiment?",
"en": "Mary: Right?",
"ja": "Mary: 本当？"
},
{
"fr": "Jean: Cela rend parfaitement compte du passage que nous devons faire de notre intuition quotidienne, classique à la réalité quantique.",
"en": "John: It perfectly captures the jump we have to make from our everyday, classical intuition to the quantum reality.",
"ja": "John: それは、私たちの日常的で古典的な直感から量子の現実への跳躍を正確に捉えています。"
},
{
"fr": "Marie: Exactement. Pour une balle de baseball, je la suis de la colline du lanceur jusqu'à la plaque.",
"en": "Mary: Exactly. For a baseball, I track it from the pitcher's mound to the plate.",
"ja": "Mary: まさにそう。野球のボールに関しては、投手のマウンドからホームプレートまでその動きを追跡します。"
},
{
"fr": "Jean: D'accord.",
"en": "John: Sure.",
"ja": "John: その通りです。"
},
{
"fr": "Marie: Je vois son changement de position. Simple.",
"en": "Mary: I see its position change. Simple.",
"ja": "Mary: その位置の変化が見える。単純だ。"
},
{
"fr": "Jean: Et c'est là qu'on doit, vous savez, reprogrammer nos cerveaux. Pour un électron, le manuel des règles est complètement différent.",
"en": "John: And that’s where we have to, you know, rewire our brains. For an electron, the rulebook is entirely different.",
"ja": "John: そして、それこそが私たちが脳を再プログラミングしなければならないところです。電子の場合、ルールはまったく異なります。"
},
{
"fr": "Marie: D'accord.",
"en": "Mary: Okay.",
"ja": "Mary: わかりました。"
},
{
"fr": "Jean: L'essentiel, c'est que l'électron n'est pas seulement une petite balle ; c'est aussi une onde... une onde.",
"en": "John: The key is that an electron isn't just a tiny ball; it's also a wave... a wave.",
"ja": "John: 重要なのは、電子が単なる小さなボールではなく、波でもあるということです…波です。"
},
{
"fr": "Marie: La dualité onde-particule. C’est vrai.",
"en": "Mary: The wave-particle duality. Right.",
"ja": "Mary: 波動-粒子二重性。その通り。"
},
{
"fr": "Jean: Et son moment n'est pas une vitesse que nous calculons, mais une... une propriété fondamentale de cette onde.",
"en": "John: And its momentum isn't a speed we calculate, but a... a fundamental property of that wave.",
"ja": "John: その運動量は我々が計算する速度ではなく、…その波の基本的な性質です。"
},
{
"fr": "Marie: Hmm.",
"en": "Mary: Hmm.",
"ja": "Mary: ふむ。"
},
{
"fr": "Jean: Imaginez des rides sur un étang. Le moment d'une particule quantique est comme la « ondulation » de son onde dans l'espace — la distance entre les crêtes.",
"en": "John: Imagine ripples on a pond. The momentum of a quantum particle is like the 'waviness' of its wave in space—how close together the crests are.",
"ja": "John: 池の水面にできる波紋を想像してみてください。量子粒子の運動量は、空間におけるその波の「波打ち具合」、つまり波の山と山の間隔のように考えられます。"
},
{
"fr": "Marie: Alors, une onde très serrée et très ondulée signifie un moment élevé ?",
"en": "Mary: So, a very tightly packed, wiggly wave means high momentum?",
"ja": "Mary: では、非常に密に詰まっており、波打ち具合が激しい波ということは、運動量が高いということですか？"
},
{
"fr": "Jean: Vous avez raison. Et l'« opérateur de moment » n'est rien d'autre qu'un outil mathématique qui pose une question à l'onde : « Combien es-tu ondulée ? »",
"en": "John: You've got it. And the 'momentum operator' is simply the mathematical tool that asks the wave a question: 'How wavy are you?'",
"ja": "John: その通りです。そして「運動量演算子」は、波に質問する数学的なツールで、その質問は「どのくらい波打ち具合が強いですか？」です。"
},
{
"fr": "Marie: Exactement.",
"en": "Mary: Right.",
"ja": "Mary: そうです。"
},
{
"fr": "Jean: Il mesure le taux de changement de la forme de l'onde. Nous ne suivons pas un point en mouvement ; nous analysons la forme intrinsèque de l'onde elle-même.",
"en": "John: It measures the rate of change of the wave's shape. We're not tracking a moving dot; we're analyzing the inherent form of the wave itself.",
"ja": "John: それは波の形状の変化率を測定しています。動く点を追跡しているのではなく、波そのものの本来の形を分析しているのです。"
},
{
"fr": "Marie: Ah, je vois ! Donc, cela ne dépend pas d'un changement de position, car c'est une caractéristique de l'onde à un seul moment. Mais attendez… si la position et le moment ne sont que deux aspects différents de la même onde…",
"en": "Mary: Ah, I see! So it doesn't depend on a change in position, because it's a feature of the wave at a single moment. But wait… if position and momentum are just two different aspects of the same wave...",
"ja": "Mary: ああ、わかりました！だから、それは位置の変化に依存するわけではないのです。なぜなら、それはある一瞬の波の特性だからです。しかし、位置と運動量が同じ波の2つの異なる側面であるなら…"
},
{
"fr": "Jean: Oui...",
"en": "John: Yes...",
"ja": "John: はい..."
},
{
"fr": "Marie: ...ils doivent être connectés de quelque manière. Cela... cela me semble nous mener quelque part de très célèbre.",
"en": "Mary: ...they have to be connected somehow. This... this feels like it's leading us somewhere very famous.",
"ja": "Mary: ...それらはどこかで結びついているはずだ。これは…これは、どこか非常に有名なところに導いていっているような気がする。"
},
{
"fr": "Jean: C'est le chemin direct vers le principe d'incertitude de Heisenberg.",
"en": "John: It's the direct path to Heisenberg's Uncertainty Principle.",
"ja": "John: それはハイゼンベルクの不確定性原理に至る直接の道です。"
},
{
"fr": "Marie: Ah.",
"en": "Mary: Ah.",
"ja": "Mary: ああ。"
},
{
"fr": "Jean: Pensez-y. Pour avoir un momentum parfaitement défini, vous avez besoin d'une onde parfaite et uniforme — comme une note musicale pure — qui s'étend sans fin.",
"en": "John: Think it through. To have a perfectly defined momentum, you need a perfect, uniform wave—like a pure musical note—that stretches on and on.",
"ja": "John: よく考えてみましょう。完璧に定義された運動量を持たせるには、無限に続く純粋な音のような、完全で均一な波が必要です。"
},
{
"fr": "Marie: D'accord, une onde parfaitement régulière.",
"en": "Mary: Okay, a perfectly regular wave.",
"ja": "Mary: わかりました。完全に均一な波です。"
},
{
"fr": "Jean: Mais si votre onde s'étend partout, à travers l'ensemble de l'univers…",
"en": "John: But if your wave extends everywhere, across the entire universe…",
"ja": "John: しかし、もしあなたの波が至る所に広がり、宇宙全体にわたっていれば…"
},
{
"fr": "Marie: Oui?",
"en": "Mary: Yeah?",
"ja": "Mary: ええ？"
},
{
"fr": "Jean: ...où se trouve la particule ?",
"en": "John: ...where is the particle?",
"ja": "John: …では、粒子はどこにあるの？"
},
{
"fr": "Marie: Vous n'avez aucune idée. Sa position est complètement incertaine. Et… laissez-moi deviner… si vous voulez connaître sa position parfaitement…",
"en": "Mary: You have no idea. Its position is completely uncertain. And… let me guess… if you want to know its position perfectly...",
"ja": "Mary: 全く分からない。その位置は完全に不確実です。そして…想像してみると…その位置を完全に把握したいとしたら…"
},
{
"fr": "Jean: Allez-y.",
"en": "John: Go on.",
"ja": "John: どうぞ。"
},
{
"fr": "Marie: l'onde doit être un pic unique et net.",
"en": "Mary: ...the wave has to be a single, sharp spike.",
"ja": "Mary: 波は一つの鋭いピークである必要があります。"
},
{
"fr": "Jean: Exactement. Mais une pointe n'a pas de longueur d'onde définie. C'est juste… une pointe.",
"en": "John: Exactly. But a spike has no defined wavelength. It's just… a spike.",
"ja": "John: その通りです。しかし、このような鋭いピークには明確な波長はありません。それはただ… 鋭いピークです。"
},
{
"fr": "Marie: Exactement.",
"en": "Mary: Right.",
"ja": "Mary: そう。"
},
{
"fr": "Jean: Donc, sa « ondulation », son moment, deviennent complètement inconnus. Et ce n'est pas une limite de nos outils ; c'est un compromis fondamental inscrit dans la réalité.",
"en": "John: So its 'waviness,' its momentum, becomes completely unknown. And this isn't a limit of our tools; it's a fundamental trade-off baked into reality.",
"ja": "John: したがって、その「波動性」、その「運動量」は完全に未知になります。そしてこれは私たちの道具の限界ではなく、現実の本質に組み込まれた根本的なトレードオフです。"
},
{
"fr": "Marie: C'est incroyable. Mais alors, comment les physiciens expérimentaux y parviennent-ils ?",
"en": "Mary: That is mind-bending. But then, how do experimental physicists do it?",
"ja": "Mary: それは頭が痛くなるほど難しいです。しかし、では、実験物理学者たちはどうやってそれを実現しているのでしょうか？"
},
{
"fr": "Jean: Ah!",
"en": "John: Ah!",
"ja": "John: あっ！"
},
{
"fr": "Marie: Comment obtiennent-ils une mesure précise du moment dans le monde réel ?",
"en": "Mary: How do they get a precise momentum measurement in the real world?",
"ja": "Mary: では、現実世界で彼らはどのように正確な運動量の測定を行っているのですか？"
},
{
"fr": "Jean: C'est ici que l'intelligence remarquable de la physique moderne entre en jeu.",
"en": "John: This is where the sheer cleverness of modern physics comes in.",
"ja": "John: ここが現代物理学の卓越した知恵が登場する場所です。"
},
{
"fr": "Marie: D'accord...",
"en": "Mary: Okay...",
"ja": "Mary: わかりました..."
},
{
"fr": "Jean: Ils utilisent des stratégies ingénieuses et indirectes. Mon exemple préféré est de prendre un électron et de le placer dans un champ magnétique.",
"en": "John: They use ingenious, indirect strategies. My favorite example is to take an electron and place it in a magnetic field.",
"ja": "John: 彼らは巧妙で間接的な戦略を使用します。私の好きな例は、電子を取り、それを磁場の中に置くことです。"
},
{
"fr": "Marie: D'accord, donc il va commencer à se déplacer en cercle.",
"en": "Mary: Okay, so it will start to move in a circle.",
"ja": "Mary: わかりました、それではそれが円周運動を開始するようになります。"
},
{
"fr": "Jean: Exactement. Maintenant, vous le laissez accomplir exactement une demi-tour.",
"en": "John: Correct. Now, you let it complete exactly one half-turn.",
"ja": "John: 正しいです。今度は、それを正確に半回転させるようにします。"
},
{
"fr": "Marie: D'accord.",
"en": "Mary: Okay.",
"ja": "Mary: わかりました。"
},
{
"fr": "Jean: Et à ce moment précis, vous mesurez sa position.",
"en": "John: And at that precise moment, you measure its position.",
"ja": "John: その正確な時刻に、その位置を測定します。"
},
{
"fr": "Marie: Vous mesurez sa position. Et… qu'est-ce que cela vous apprend ?",
"en": "Mary: You measure its position. And… what does that tell you?",
"ja": "Mary: その位置を測定します。そして…それはあなたに何を教えてくれるでしょうか？"
},
{
"fr": "Jean: C'est là que réside la magie. Cette mesure unique de sa position finale vous dit, avec une précision incroyable, quelle était sa quantité de mouvement initiale…",
"en": "John: Here’s the magic. That single measurement of its final position tells you, with incredible precision, what its initial momentum was...",
"ja": "John: これが魔法の部分です。その最終的な位置に関する単一の測定は、驚くほど正確に、その初期の運動量をあなたに教えてくれます…"
},
{
"fr": "Marie: Wow.",
"en": "Mary: Wow.",
"ja": "Mary: すごい！"
},
{
"fr": "Jean: ...exactement au début.",
"en": "John: ...right back at the start.",
"ja": "John: ...最初の時点に戻って。"
},
{
"fr": "Marie: Attendez, vous me dites que mesurer où il est maintenant nous apprend comment il se déplaçait autrefois ?",
"en": "Mary: Wait, you're telling me that measuring where it is now tells you how it was moving back then?",
"ja": "Mary: ちょっと待って、今いる場所を測定することで、かつてどう動いていたかがわかるって言ってるの？"
},
{
"fr": "Jean: Oui.",
"en": "John: Yeah.",
"ja": "John: はい。"
},
{
"fr": "Marie: Ça semble impossible.",
"en": "Mary: That sounds impossible.",
"ja": "Mary: それは不可能に聞こえる。"
},
{
"fr": "Jean: C'est une belle idée appelée « mesure généralisée ». Au lieu d'essayer de mesurer directement le moment, vous laissez le système évoluer d'une manière qui traduit proprement l'information que vous souhaitez — le moment — en un autre type d'information plus facile à mesurer, comme la position.",
"en": "John: It's a beautiful concept called a 'generalized measurement.' Instead of trying to measure momentum directly, you... you let the system evolve in a way that neatly translates the information you want—the momentum—into a different kind of information that's easier to measure, like position.",
"ja": "John: 「一般化された測定」と呼ばれる美しい概念です。運動量を直接測定するのではなく、システムを進化させ、測定したい情報を（運動量）を、測定しやすい別の情報（例えば位置）にうまく変換する方法です。"
},
{
"fr": "Marie: Donc, une mesure n'est pas simplement un regard passif.",
"en": "Mary: So, a measurement isn't just a passive look.",
"ja": "Mary: つまり、測定は単なる受動的な観察ではない。"
},
{
"fr": "Jean: Non",
"en": "John: No.",
"ja": "John: いいえ"
},
{
"fr": "Marie: C'est un processus actif, une stratégie. Vous manipulez le système pour qu'il vous révèle ses secrets.",
"en": "Mary: It's an active process, a strategy. You're manipulating the system to make it tell you its secrets.",
"ja": "Mary: それは能動的なプロセスであり、戦略です。システムを操作して、その秘密を引き出そうとするのです。"
},
{
"fr": "Jean: Vous l'avez parfaitement capturé. Une grandeur physique dans le monde quantique n'est pas une propriété statique attendant d'être lue.",
"en": "John: You've captured it perfectly. A physical quantity in the quantum world is not a static property waiting to be read.",
"ja": "John: あなたはそれを完璧に捉えています。量子世界における物理量は、読み取られるのを待っている静的な性質ではありません。"
},
{
"fr": "Marie: Hmm.",
"en": "Mary: Hmm.",
"ja": "Mary: ふむ。"
},
{
"fr": "Jean: C'est le résultat d'une action dynamique que vous effectuez sur le système. La question de l'auditeur révèle vraiment cette toute nouvelle révolution dans la pensée.",
"en": "John: It is the outcome of a dynamic action you perform on the system. That listener's question, it really uncovers that entire, revolutionary shift in thinking.",
"ja": "John: それはあなたがシステムに対して行う動的な「行動」の結果です。聞き手の質問は、その全体的な、革命的な思考の転換を本当に明らかにしています。"
},
{
"fr": "Marie: Cela remet complètement en question le monde. Jean, merci. C'était d'une clarté saisissante.",
"en": "Mary: That completely reframes the world. John, thank you. That was stunningly clear.",
"ja": "Mary: それは世界を完全に再構成する。ジョン、ありがとう。それは驚くほど明確だった。"
},
{
"fr": "Jean: C’était un plaisir, Marie.",
"en": "John: It was my pleasure, Mary.",
"ja": "John: それは良かったです、メアリーさん。"
},
{
"fr": "Marie: Maintenant, voici une question à laquelle nous aimerions que vous réfléchissiez. Si la nature vous forçait à faire un choix, préféreriez-vous connaître avec une absolue et parfaite certitude : exactement où vous êtes en ce moment...",
"en": "Mary: Now, here's a question we'd like you to think about. If nature forced you to make a choice, which would you rather know with absolute, perfect certainty: exactly where you are in this moment...",
"ja": "Mary: では、ここで皆さんに考えていただきたい質問があります。もし自然があなたに選択を迫ったとしたら、絶対的で完璧な確信で知りたいのは、この瞬間に あなたがどこにいるか でしょうか..."
},
{
"fr": "Jean: Hmm.",
"en": "John: Hmm.",
"ja": "John: ふむ。"
},
{
"fr": "Marie: ou la direction et la quantité de mouvement exactes avec lesquelles vous avancez ?",
"en": "Mary: ...or the exact direction and momentum with which you are moving forward?",
"ja": "Mary: それとも、あなたがどの方向に、どの勢いで 進んでいるか の正確な情報でしょうか？"
},
{
"fr": "Jean: Et comment ce choix changerait-il votre vision de votre propre existence ?",
"en": "John: And how would that choice change your view of your own existence?",
"ja": "John: では、その選択は、あなた自身の存在に対する見方をどのように変えるでしょうか？"
},
{
"fr": "Marie: À la prochaine sur « Bonds Quantiques », restez curieux.",
"en": "Mary: Until next time on \"Quantum Leaps,\" stay curious.",
"ja": "Mary: 『量子の跳躍』の次の放送まで、好奇心を持ち続けてください。"
}
]);
