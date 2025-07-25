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
"ja": "John: 僕はジョン。ここに来られて光栄だよ。"
},
{
"fr": "Marie: Jean, aujourd'hui nous avons une question d'auditeur qui est juste... fantastique.",
"en": "Mary: John, today we've got a listener question that's just... fantastic.",
"ja": "Mary: ジョン、今日はリスナーから、もう…最高の質問が届いているの。"
},
{
"fr": "Jean: Oh?",
"en": "John: Oh?",
"ja": "John: ほう？"
},
{
"fr": "Marie: Ça touche au cœur de ce qui rend la mécanique quantique si… si étrange.",
"en": "Mary: It gets right to the core of what makes quantum mechanics so… well, so weird.",
"ja": "Mary: 量子力学がどうしてこんなに…奇妙なのか、その核心に触れるものよ。"
},
{
"fr": "Jean: J'adore ceux-ci. Qu'est-ce que c'est ?",
"en": "John: I love those. What is it?",
"ja": "John: そういうの、大好きだよ。どんな質問なんだい？"
},
{
"fr": "Marie: Ils demandent, euh, « en mécanique quantique, on obtient le moment cinétique à partir de quelque chose appelé un « opérateur » ».",
"en": "Mary: They ask, uh, \"In quantum mechanics, you get momentum from something called an 'operator.'\"",
"ja": "Mary: えっとね、「量子力学では、『演算子』と呼ばれるものから運動量を得るそうですが」って。"
},
{
"fr": "Jean: D'accord",
"en": "John: Okay.",
"ja": "John: うん"
},
{
"fr": "Marie: Mais dans ma tête, le momentum vient de regarder quelque chose se déplacer — d’un changement de position. Comment peut-il être une chose que l’on mesure toute seule ?",
"en": "Mary: \"But in my head, momentum comes from watching something move—from a change in position. How can it be a thing you measure all by itself?\"",
"ja": "Mary: 「でも、私の感覚では、運動量って何かが動くのを、つまり位置の変化を見てわかるものですよね。どうして運動量だけを単独で測定できるものなんでしょうか？」って。"
},
{
"fr": "Jean: C’est une question véritablement brillante.",
"en": "John: That is a truly brilliant question.",
"ja": "John: それは本当に見事な質問だね。"
},
{
"fr": "Marie: Vraiment?",
"en": "Mary: Right?",
"ja": "Mary: でしょう？"
},
{
"fr": "Jean: Cela rend parfaitement compte du passage que nous devons faire de notre intuition quotidienne, classique à la réalité quantique.",
"en": "John: It perfectly captures the jump we have to make from our everyday, classical intuition to the quantum reality.",
"ja": "John: 僕たちの日常的な、古典的な直感から、量子の現実へと頭を切り替える必要性を、完璧に言い表しているよ。"
},
{
"fr": "Marie: Exactement. Pour une balle de baseball, je la suis de la colline du lanceur jusqu'à la plaque.",
"en": "Mary: Exactly. For a baseball, I track it from the pitcher's mound to the plate.",
"ja": "Mary: まさに。野球のボールなら、ピッチャーマウンドからホームベースまで、その軌道を追いかけるわ。"
},
{
"fr": "Jean: D'accord.",
"en": "John: Sure.",
"ja": "John: そうだね。"
},
{
"fr": "Marie: Je vois son changement de position. Simple.",
"en": "Mary: I see its position change. Simple.",
"ja": "Mary: 位置の変化を見て、速さがわかる。単純な話よ。"
},
{
"fr": "Jean: Et c'est là qu'on doit, vous savez, reprogrammer nos cerveaux. Pour un électron, le manuel des règles est complètement différent.",
"en": "John: And that’s where we have to, you know, rewire our brains. For an electron, the rulebook is entirely different.",
"ja": "John: そして、そこが僕たちの脳を書き換えないといけない部分なんだ。電子の場合、ルールブックが全く違う。"
},
{
"fr": "Marie: D'accord.",
"en": "Mary: Okay.",
"ja": "Mary: なるほど。"
},
{
"fr": "Jean: L'essentiel, c'est que l'électron n'est pas seulement une petite balle ; c'est aussi une onde... une onde.",
"en": "John: The key is that an electron isn't just a tiny ball; it's also a wave... a wave.",
"ja": "John: 重要なのは、電子はただの小さなボールじゃなくて、波でもある…ということなんだ。"
},
{
"fr": "Marie: La dualité onde-particule. C’est vrai.",
"en": "Mary: The wave-particle duality. Right.",
"ja": "Mary: 波と粒子の二重性。そうね。"
},
{
"fr": "Jean: Et son moment n'est pas une vitesse que nous calculons, mais une... une propriété fondamentale de cette onde.",
"en": "John: And its momentum isn't a speed we calculate, but a... a fundamental property of that wave.",
"ja": "John: そして、その運動量は僕たちが計算する速さじゃなくて、その波そのものが持つ…基本的な性質なんだ。"
},
{
"fr": "Marie: Hmm.",
"en": "Mary: Hmm.",
"ja": "Mary: ふむ。"
},
{
"fr": "Jean: Imaginez des rides sur un étang. Le moment d'une particule quantique est comme la « ondulation » de son onde dans l'espace — la distance entre les crêtes.",
"en": "John: Imagine ripples on a pond. The momentum of a quantum particle is like the 'waviness' of its wave in space—how close together the crests are.",
"ja": "John: 池に広がる波紋を想像してみて。量子粒子の運動量っていうのは、空間におけるその波の「波っぽさ」、つまり波の山と山がどれだけ詰まっているか、ということなんだ。"
},
{
"fr": "Marie: Alors, une onde très serrée et très ondulée signifie un moment élevé ?",
"en": "Mary: So, a very tightly packed, wiggly wave means high momentum?",
"ja": "Mary: じゃあ、波がぎゅっと詰まっていて、小刻みに波打っているほど、運動量が大きいってこと？"
},
{
"fr": "Jean: Vous avez raison. Et l'« opérateur de moment » n'est rien d'autre qu'un outil mathématique qui pose une question à l'onde : « Combien es-tu ondulée ? »",
"en": "John: You've got it. And the 'momentum operator' is simply the mathematical tool that asks the wave a question: 'How wavy are you?'",
"ja": "John: その通り。「運動量演算子」っていうのは、その波に「君はどれくらい波打ってるんだい？」って問いかけるための、数学的な道具にすぎないんだ。"
},
{
"fr": "Marie: Exactement.",
"en": "Mary: Right.",
"ja": "Mary: なるほど。"
},
{
"fr": "Jean: Il mesure le taux de changement de la forme de l'onde. Nous ne suivons pas un point en mouvement ; nous analysons la forme intrinsèque de l'onde elle-même.",
"en": "John: It measures the rate of change of the wave's shape. We're not tracking a moving dot; we're analyzing the inherent form of the wave itself.",
"ja": "John: それは波の形の変化率を測るものなんだ。動いている点を追いかけるんじゃなくて、波そのものに固有の形を分析しているんだよ。"
},
{
"fr": "Marie: Ah, je vois ! Donc, cela ne dépend pas d'un changement de position, car c'est une caractéristique de l'onde à un seul moment. Mais attendez… si la position et le moment ne sont que deux aspects différents de la même onde…",
"en": "Mary: Ah, I see! So it doesn't depend on a change in position, because it's a feature of the wave at a single moment. But wait… if position and momentum are just two different aspects of the same wave...",
"ja": "Mary: ああ、なるほど！だから位置の変化とは関係ないのね。その瞬間の波自体の特徴だから。でも待って…もし位置と運動量が、同じ一つの波の、違う側面にすぎないとしたら…"
},
{
"fr": "Jean: Oui...",
"en": "John: Yes...",
"ja": "John: うん…"
},
{
"fr": "Marie: ...ils doivent être connectés de quelque manière. Cela... cela me semble nous mener quelque part de très célèbre.",
"en": "Mary: ...they have to be connected somehow. This... this feels like it's leading us somewhere very famous.",
"ja": "Mary: …それらは何らかの形で繋がっているはずよね。これって…何かすごく有名な話につながっていきそう。"
},
{
"fr": "Jean: C'est le chemin direct vers le principe d'incertitude de Heisenberg.",
"en": "John: It's the direct path to Heisenberg's Uncertainty Principle.",
"ja": "John: まさに、ハイゼンベルクの不確定性原理へまっすぐ続く道だよ。"
},
{
"fr": "Marie: Ah.",
"en": "Mary: Ah.",
"ja": "Mary: やっぱり。"
},
{
"fr": "Jean: Pensez-y. Pour avoir un momentum parfaitement défini, vous avez besoin d'une onde parfaite et uniforme — comme une note musicale pure — qui s'étend sans fin.",
"en": "John: Think it through. To have a perfectly defined momentum, you need a perfect, uniform wave—like a pure musical note—that stretches on and on.",
"ja": "John: 考えてみて。運動量を完璧に一つに定めるには、どこまでも無限に続く、澄んだ音のような、完璧で均一な波が必要なんだ。"
},
{
"fr": "Marie: D'accord, une onde parfaitement régulière.",
"en": "Mary: Okay, a perfectly regular wave.",
"ja": "Mary: なるほど、完全に均一な波ね。"
},
{
"fr": "Jean: Mais si votre onde s'étend partout, à travers l'ensemble de l'univers…",
"en": "John: But if your wave extends everywhere, across the entire universe…",
"ja": "John: でも、もしその波が宇宙の隅々まで広がっていたとしたら…"
},
{
"fr": "Marie: Oui?",
"en": "Mary: Yeah?",
"ja": "Mary: ええ。"
},
{
"fr": "Jean: ...où se trouve la particule ?",
"en": "John: ...where is the particle?",
"ja": "John: …その粒子は、どこに「ある」と言える？"
},
{
"fr": "Marie: Vous n'avez aucune idée. Sa position est complètement incertaine. Et… laissez-moi deviner… si vous voulez connaître sa position parfaitement…",
"en": "Mary: You have no idea. Its position is completely uncertain. And… let me guess… if you want to know its position perfectly...",
"ja": "Mary: どこにも。位置が完全に不確定になる。…ということは、逆に、その位置を完璧に知りたいなら…"
},
{
"fr": "Jean: Allez-y.",
"en": "John: Go on.",
"ja": "John: どうなるかな？"
},
{
"fr": "Marie: l'onde doit être un pic unique et net.",
"en": "Mary: ...the wave has to be a single, sharp spike.",
"ja": "Mary: …波は、たった一点だけの、鋭いトゲみたいな形にならないと。"
},
{
"fr": "Jean: Exactement. Mais une pointe n'a pas de longueur d'onde définie. C'est juste… une pointe.",
"en": "John: Exactly. But a spike has no defined wavelength. It's just… a spike.",
"ja": "John: その通り。でも、そんなトゲには決まった波長がない。ただの…トゲだからね。"
},
{
"fr": "Marie: Exactement.",
"en": "Mary: Right.",
"ja": "Mary: ですよね。"
},
{
"fr": "Jean: Donc, sa « ondulation », son moment, deviennent complètement inconnus. Et ce n'est pas une limite de nos outils ; c'est un compromis fondamental inscrit dans la réalité.",
"en": "John: So its 'waviness,' its momentum, becomes completely unknown. And this isn't a limit of our tools; it's a fundamental trade-off baked into reality.",
"ja": "John: だから、その「波っぽさ」、つまり運動量は完全に未知のものになる。これは測定器の限界じゃなくて、この現実そのものに組み込まれた、根本的なトレードオフなんだ。"
},
{
"fr": "Marie: C'est incroyable. Mais alors, comment les physiciens expérimentaux y parviennent-ils ?",
"en": "Mary: That is mind-bending. But then, how do experimental physicists do it?",
"ja": "Mary: 頭がクラクラするわ。でも、それなら実験物理学者の人たちはどうしてるの？"
},
{
"fr": "Jean: Ah!",
"en": "John: Ah!",
"ja": "John: ああ！"
},
{
"fr": "Marie: Comment obtiennent-ils une mesure précise du moment dans le monde réel ?",
"en": "Mary: How do they get a precise momentum measurement in the real world?",
"ja": "Mary: 現実の世界で、どうやって正確な運動量を測っているのかしら？"
},
{
"fr": "Jean: C'est ici que l'intelligence remarquable de la physique moderne entre en jeu.",
"en": "John: This is where the sheer cleverness of modern physics comes in.",
"ja": "John: そこにこそ、現代物理学の真の賢さがあるんだよ。"
},
{
"fr": "Marie: D'accord...",
"en": "Mary: Okay...",
"ja": "Mary: へえ…"
},
{
"fr": "Jean: Ils utilisent des stratégies ingénieuses et indirectes. Mon exemple préféré est de prendre un électron et de le placer dans un champ magnétique.",
"en": "John: They use ingenious, indirect strategies. My favorite example is to take an electron and place it in a magnetic field.",
"ja": "John: 彼らは、巧妙で間接的な戦略を使う。僕の好きな例は、電子を磁場の中に入れる方法だ。"
},
{
"fr": "Marie: D'accord, donc il va commencer à se déplacer en cercle.",
"en": "Mary: Okay, so it will start to move in a circle.",
"ja": "Mary: なるほど、そうすると円を描いて動き始めるわね。"
},
{
"fr": "Jean: Exactement. Maintenant, vous le laissez accomplir exactement une demi-tour.",
"en": "John: Correct. Now, you let it complete exactly one half-turn.",
"ja": "John: その通り。そして、電子にちょうど半周だけ回転させる。"
},
{
"fr": "Marie: D'accord.",
"en": "Mary: Okay.",
"ja": "Mary: ええ。"
},
{
"fr": "Jean: Et à ce moment précis, vous mesurez sa position.",
"en": "John: And at that precise moment, you measure its position.",
"ja": "John: そして、その瞬間に、電子の位置を測定するんだ。"
},
{
"fr": "Marie: Vous mesurez sa position. Et… qu'est-ce que cela vous apprend ?",
"en": "Mary: You measure its position. And… what does that tell you?",
"ja": "Mary: 位置を測るのね。それで…何がわかるの？"
},
{
"fr": "Jean: C'est là que réside la magie. Cette mesure unique de sa position finale vous dit, avec une précision incroyable, quelle était sa quantité de mouvement initiale…",
"en": "John: Here’s the magic. That single measurement of its final position tells you, with incredible precision, what its initial momentum was...",
"ja": "John: ここからがマジックだ。その最終的な位置を一度測るだけで、信じられないほど正確に、その電子が最初に持っていた運動量がわかるんだ…"
},
{
"fr": "Marie: Wow.",
"en": "Mary: Wow.",
"ja": "Mary: すごい！"
},
{
"fr": "Jean: ...exactement au début.",
"en": "John: ...right back at the start.",
"ja": "John: …一番最初のね。"
},
{
"fr": "Marie: Attendez, vous me dites que mesurer où il est maintenant nous apprend comment il se déplaçait autrefois ?",
"en": "Mary: Wait, you're telling me that measuring where it is now tells you how it was moving back then?",
"ja": "Mary: 待って、今どこにいるかを測ることで、過去にどう動いていたかがわかるってこと？"
},
{
"fr": "Jean: Oui.",
"en": "John: Yeah.",
"ja": "John: そう。"
},
{
"fr": "Marie: Ça semble impossible.",
"en": "Mary: That sounds impossible.",
"ja": "Mary: そんなの、不可能に聞こえるわ。"
},
{
"fr": "Jean: C'est une belle idée appelée « mesure généralisée ». Au lieu d'essayer de mesurer directement le moment, vous laissez le système évoluer d'une manière qui traduit proprement l'information que vous souhaitez — le moment — en un autre type d'information plus facile à mesurer, comme la position.",
"en": "John: It's a beautiful concept called a 'generalized measurement.' Instead of trying to measure momentum directly, you... you let the system evolve in a way that neatly translates the information you want—the momentum—into a different kind of information that's easier to measure, like position.",
"ja": "John: これは「一般化測定」と呼ばれる美しい概念なんだ。運動量を直接測ろうとするんじゃなくて、システムをうまく変化させて、知りたい情報を、もっと測りやすい別の情報に変換してやるんだよ。"
},
{
"fr": "Marie: Donc, une mesure n'est pas simplement un regard passif.",
"en": "Mary: So, a measurement isn't just a passive look.",
"ja": "Mary: じゃあ、測定っていうのは、ただ受動的に眺めることじゃないのね。"
},
{
"fr": "Jean: Non",
"en": "John: No.",
"ja": "John: 違う。"
},
{
"fr": "Marie: C'est un processus actif, une stratégie. Vous manipulez le système pour qu'il vous révèle ses secrets.",
"en": "Mary: It's an active process, a strategy. You're manipulating the system to make it tell you its secrets.",
"ja": "Mary: 能動的なプロセスで、戦略なのね。システムを操作して、秘密を吐き出させる、みたいな。"
},
{
"fr": "Jean: Vous l'avez parfaitement capturé. Une grandeur physique dans le monde quantique n'est pas une propriété statique attendant d'être lue.",
"en": "John: You've captured it perfectly. A physical quantity in the quantum world is not a static property waiting to be read.",
"ja": "John: まさにその通り。量子世界における物理的な量というのは、ただそこにあって読み取られるのを待っている静的な特性じゃないんだ。"
},
{
"fr": "Marie: Hmm.",
"en": "Mary: Hmm.",
"ja": "Mary: ふむ。"
},
{
"fr": "Jean: C'est le résultat d'une action dynamique que vous effectuez sur le système. La question de l'auditeur révèle vraiment cette toute nouvelle révolution dans la pensée.",
"en": "John: It is the outcome of a dynamic action you perform on the system. That listener's question, it really uncovers that entire, revolutionary shift in thinking.",
"ja": "John: それは、君がシステムに対して行う動的な「行為」の結果なんだ。あのリスナーの質問は、まさにこの革命的な思考の転換を、見事に言い当てているよ。"
},
{
"fr": "Marie: Cela remet complètement en question le monde. Jean, merci. C'était d'une clarté saisissante.",
"en": "Mary: That completely reframes the world. John, thank you. That was stunningly clear.",
"ja": "Mary: 世界の見方がまったく変わってしまうわ。ジョン、ありがとう。息をのむほど分かりやすかった。"
},
{
"fr": "Jean: C’était un plaisir, Marie.",
"en": "John: It was my pleasure, Mary.",
"ja": "John: どういたしまして、メアリー。"
},
{
"fr": "Marie: Maintenant, voici une question à laquelle nous aimerions que vous réfléchissiez. Si la nature vous forçait à faire un choix, préféreriez-vous connaître avec une absolue et parfaite certitude : exactement où vous êtes en ce moment...",
"en": "Mary: Now, here's a question we'd like you to think about. If nature forced you to make a choice, which would you rather know with absolute, perfect certainty: exactly where you are in this moment...",
"ja": "Mary: さて、ここでリスナーの皆さんに考えていただきたい質問があります。もし自然があなたに選択を迫るとしたら、絶対に、完璧な確実性をもって知りたいのは…今この瞬間、自分が「どこにいるか」ということ？"
},
{
"fr": "Jean: Hmm.",
"en": "John: Hmm.",
"ja": "John: ふむ。"
},
{
"fr": "Marie: ou la direction et la quantité de mouvement exactes avec lesquelles vous avancez ?",
"en": "Mary: ...or the exact direction and momentum with which you are moving forward?",
"ja": "Mary: …それとも、自分が「どの方向へ、どんな勢いで進んでいるか」ということ？"
},
{
"fr": "Jean: Et comment ce choix changerait-il votre vision de votre propre existence ?",
"en": "John: And how would that choice change your view of your own existence?",
"ja": "John: そして、その選択は、あなた自身の存在についての考え方を、どう変えるだろうか？"
},
{
"fr": "Marie: À la prochaine sur « Bonds Quantiques », restez curieux.",
"en": "Mary: Until next time on \"Quantum Leaps,\" stay curious.",
"ja": "Mary: 次回の『量子の跳躍』まで、好奇心を持ち続けてくださいね。"
}
]);
