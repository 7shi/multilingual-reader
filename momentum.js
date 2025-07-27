// Initialize datasets array if undefined
if (typeof datasets === 'undefined') {
    var datasets = [];
}

// Add dataset to datasets array
datasets.push(
[{
"speaker": "Camille",
"fr": "Bienvenue dans « Passerelles en Physique », l'émission qui donne un sens à l'univers, un mystère à la fois. Je suis Camille.",
"de": "Willkommen bei „Brücken in die Physik“, der Sendung, die das Universum Stück für Stück verständlich macht. Ich bin Camille.",
"en": "Welcome to \"Bridges in Physics,\" the show that makes sense of the universe, one puzzle at a time. I'm Camille.",
"zh": "欢迎收看《物理之桥》，本节目将带您一步步解开宇宙的奥秘。我是卡米尔。",
"ja": "『物理の架け橋』へようこそ。この番組では、1つずつ謎を解きながら、宇宙の意味を明らかにします。私はカミーユです。"
},{
"speaker": "Luc",
"fr": "Et je suis Luc. C'est un plaisir d'être ici.",
"de": "Und ich bin Luc. Es ist mir eine Freude, hier zu sein.",
"en": "And I'm Luc. It's a pleasure to be here.",
"zh": "我是卢克。很高兴来到这里。",
"ja": "僕はリュック。ここに来られて光栄だよ。"
},{
"speaker": "Camille",
"fr": "Luc, aujourd'hui nous avons une question d'auditeur qui est juste... fantastique.",
"de": "Luc, heute haben wir eine Hörerfrage, die einfach... fantastisch ist.",
"en": "Luc, today we've got a listener question that's just... fantastic.",
"zh": "卢克，今天我们有一个听众提问，简直太棒了。",
"ja": "リュック、今日はリスナーから、もう…最高の質問が届いているの。"
},{
"speaker": "Luc",
"fr": "Oh?",
"de": "Oh?",
"en": "Oh?",
"zh": "哦？",
"ja": "ほう？"
},{
"speaker": "Camille",
"fr": "Ça touche au cœur de ce qui rend la mécanique quantique si… si étrange.",
"de": "Sie zielt direkt auf den Kern dessen, was die Quantenmechanik so... nun ja, so seltsam macht.",
"en": "It gets right to the core of what makes quantum mechanics so… well, so weird.",
"zh": "它触及了量子力学的核心，也就是它为何如此……嗯，如此奇特。",
"ja": "量子力学がどうしてこんなに…奇妙なのか、その核心に触れるものよ。"
},{
"speaker": "Luc",
"fr": "J'adore ceux-ci. Qu'est-ce que c'est ?",
"de": "Solche Fragen liebe ich. Wie lautet sie?",
"en": "I love those. What is it?",
"zh": "我喜欢这样的问题。是什么问题呢？",
"ja": "そういうの、大好きだよ。どんな質問なんだい？"
},{
"speaker": "Camille",
"fr": "Ils demandent, euh, « en mécanique quantique, on obtient le moment cinétique à partir de quelque chose appelé un « opérateur » ».",
"de": "Die Frage lautet, äh, „In der Quantenmechanik erhält man den Impuls von etwas, das als ‚Operator‘ bezeichnet wird.“",
"en": "They ask, uh, \"In quantum mechanics, you get momentum from something called an 'operator.'\"",
"zh": "他们问，呃，“在量子力学中，动量来自一个叫做‘算符’的东西。”",
"ja": "えっとね、「量子力学では、『演算子』と呼ばれるものから運動量を得るそうですが」って。"
},{
"speaker": "Luc",
"fr": "D'accord",
"de": "Okay.",
"en": "Okay.",
"zh": "好的。",
"ja": "うん"
},{
"speaker": "Camille",
"fr": "Mais dans ma tête, le momentum vient de regarder quelque chose se déplacer — d’un changement de position. Comment peut-il être une chose que l’on mesure toute seule ?",
"de": "„Aber in meinem Kopf entsteht der Impuls, wenn man etwas beobachtet, das sich bewegt – durch eine Positionsänderung. Wie kann er etwas sein, das man für sich allein misst?“",
"en": "\"But in my head, momentum comes from watching something move—from a change in position. How can it be a thing you measure all by itself?\"",
"zh": "“但在我看来，动量来自于观察物体的运动——来自于位置的变化。它怎么能是一个可以独立测量的东西呢？”",
"ja": "「でも、私の感覚では、運動量って何かが動くのを、つまり位置の変化を見てわかるものですよね。どうして運動量だけを単独で測定できるものなんでしょうか？」って。"
},{
"speaker": "Luc",
"fr": "C’est une question véritablement brillante.",
"de": "Das ist wirklich eine brillante Frage.",
"en": "That is a truly brilliant question.",
"zh": "这真是一个非常棒的问题。",
"ja": "それは本当に見事な質問だね。"
},{
"speaker": "Camille",
"fr": "Vraiment?",
"de": "Nicht wahr?",
"en": "Right?",
"zh": "是吧？",
"ja": "でしょう？"
},{
"speaker": "Luc",
"fr": "Cela rend parfaitement compte du passage que nous devons faire de notre intuition quotidienne, classique à la réalité quantique.",
"de": "Sie erfasst perfekt den Sprung, den wir von unserer alltäglichen, klassischen Intuition zur Quantenrealität machen müssen.",
"en": "It perfectly captures the jump we have to make from our everyday, classical intuition to the quantum reality.",
"zh": "它完美地捕捉了我们从日常的经典直觉到量子现实所必须完成的飞跃。",
"ja": "僕たちの日常的な、古典的な直感から、量子の現実へと頭を切り替える必要性を、完璧に言い表しているよ。"
},{
"speaker": "Camille",
"fr": "Exactement. Pour une balle de baseball, je la suis de la colline du lanceur jusqu'à la plaque.",
"de": "Genau. Bei einem Baseball verfolge ich ihn vom Werferhügel bis zur Heimatplatte.",
"en": "Exactly. For a baseball, I track it from the pitcher's mound to the plate.",
"zh": "没错。对于一个棒球，我可以追踪它从投手丘到本垒板的轨迹。",
"ja": "まさに。野球のボールなら、ピッチャーマウンドからホームベースまで、その軌道を追いかけるわ。"
},{
"speaker": "Luc",
"fr": "D'accord.",
"de": "Sicher.",
"en": "Sure.",
"zh": "当然。",
"ja": "そうだね。"
},{
"speaker": "Camille",
"fr": "Je vois son changement de position. Simple.",
"de": "Ich sehe, wie sich seine Position ändert. Ganz einfach.",
"en": "I see its position change. Simple.",
"zh": "我看到它位置的变化。很简单。",
"ja": "位置の変化を見て、速さがわかる。単純な話よ。"
},{
"speaker": "Luc",
"fr": "Et c'est là qu'on doit, vous savez, reprogrammer nos cerveaux. Pour un électron, le manuel des règles est complètement différent.",
"de": "Und genau da müssen wir unser Gehirn neu programmieren. Für ein Elektron gelten völlig andere Regeln.",
"en": "And that’s where we have to, you know, rewire our brains. For an electron, the rulebook is entirely different.",
"zh": "而这里就是我们需要“重塑”我们大脑的地方。对于电子来说，规则是完全不同的。",
"ja": "そして、そこが僕たちの脳を書き換えないといけない部分なんだ。電子の場合、ルールブックが全く違う。"
},{
"speaker": "Camille",
"fr": "D'accord.",
"de": "Okay.",
"en": "Okay.",
"zh": "好的。",
"ja": "なるほど。"
},{
"speaker": "Luc",
"fr": "L'essentiel, c'est que l'électron n'est pas seulement une petite balle ; c'est aussi une onde... une onde.",
"de": "Der Schlüssel ist, dass ein Elektron nicht nur ein winziger Ball ist; es ist auch eine Welle.",
"en": "The key is that an electron isn't just a tiny ball; it's also a wave... a wave.",
"zh": "关键在于，电子不仅仅是一个微小的球体，它也是一种波……一种波。",
"ja": "重要なのは、電子はただの小さなボールじゃなくて、波でもある…ということなんだ。"
},{
"speaker": "Camille",
"fr": "La dualité onde-particule. C’est vrai.",
"de": "Die Welle-Teilchen-Dualität. Richtig.",
"en": "The wave-particle duality. Right.",
"zh": "波粒二象性。没错。",
"ja": "波と粒子の二重性。そうね。"
},{
"speaker": "Luc",
"fr": "Et son moment n'est pas une vitesse que nous calculons, mais une... une propriété fondamentale de cette onde.",
"de": "Und sein Impuls ist keine Geschwindigkeit, die wir berechnen, sondern eine... eine fundamentale Eigenschaft dieser Welle.",
"en": "And its momentum isn't a speed we calculate, but a... a fundamental property of that wave.",
"zh": "它的动量不是我们计算出的速度，而是……波的一个基本属性。",
"ja": "そして、その運動量は僕たちが計算する速さじゃなくて、その波そのものが持つ…基本的な性質なんだ。"
},{
"speaker": "Camille",
"fr": "Hmm.",
"de": "Hmm.",
"en": "Hmm.",
"zh": "嗯。",
"ja": "ふむ。"
},{
"speaker": "Luc",
"fr": "Imaginez des rides sur un étang. Le moment d'une particule quantique est comme « l'ondulation » de son onde dans l'espace — la distance entre les crêtes.",
"de": "Stellen Sie sich Wellen auf einem Teich vor. Der Impuls eines Quantenteilchens ist wie die ‚Welligkeit‘ seiner Welle im Raum – wie eng die Wellenberge beieinander liegen.",
"en": "Imagine ripples on a pond. The momentum of a quantum particle is like 'the waviness' of its wave in space—how close together the crests are.",
"zh": "想象一下池塘里的涟漪。量子粒子的动量就像是它在空间中波的‘波纹度’——波峰之间的距离有多近。",
"ja": "池に広がる波紋を想像してみて。量子粒子の運動量っていうのは、空間におけるその波の「波っぽさ」、つまり波の山と山がどれだけ詰まっているか、ということなんだ。"
},{
"speaker": "Camille",
"fr": "Alors, une onde très serrée et très ondulée signifie un moment élevé ?",
"de": "Eine sehr dicht gepackte, stark gekräuselte Welle bedeutet also einen hohen Impuls?",
"en": "So, a very tightly packed, wiggly wave means high momentum?",
"zh": "所以，一个非常紧密、波动的波意味着高动量？",
"ja": "じゃあ、波がぎゅっと詰まっていて、小刻みに波打っているほど、運動量が大きいってこと？"
},{
"speaker": "Luc",
"fr": "Vous avez raison. Et « l'opérateur de moment » n'est rien d'autre qu'un outil mathématique qui pose une question à l'onde : « Combien es-tu ondulée ? »",
"de": "Sie haben es erfasst. Und der ‚Impulsoperator‘ ist einfach das mathematische Werkzeug, das der Welle eine Frage stellt: ‚Wie wellig bist du?‘",
"en": "You've got it. And 'the momentum operator' is simply the mathematical tool that asks the wave a question: 'How wavy are you?'",
"zh": "你明白了。而‘动量算符’只是一个向波提问的数学工具：‘你的波纹度如何？’",
"ja": "その通り。「運動量演算子」っていうのは、その波に「君はどれくらい波打ってるんだい？」って問いかけるための、数学的な道具にすぎないんだ。"
},{
"speaker": "Camille",
"fr": "Exactement.",
"de": "Richtig.",
"en": "Right.",
"zh": "对了。",
"ja": "なるほど。"
},{
"speaker": "Luc",
"fr": "Il mesure le taux de changement de la forme de l'onde. Nous ne suivons pas un point en mouvement ; nous analysons la forme intrinsèque de l'onde elle-même.",
"de": "Er misst die Änderungsrate der Wellenform. Wir verfolgen keinen sich bewegenden Punkt; wir analysieren die inhärente Form der Welle selbst.",
"en": "It measures the rate of change of the wave's shape. We're not tracking a moving dot; we're analyzing the inherent form of the wave itself.",
"zh": "它测量的是波形变化的速率。我们不是在追踪一个移动的点，而是在分析波本身固有的形式。",
"ja": "それは波の形の変化率を測るものなんだ。動いている点を追いかけるんじゃなくて、波そのものに固有の形を分析しているんだよ。"
},{
"speaker": "Camille",
"fr": "Ah, je vois ! Donc, cela ne dépend pas d'un changement de position, car c'est une caractéristique de l'onde à un seul moment. Mais attendez… si la position et le moment ne sont que deux aspects différents de la même onde…",
"de": "Ah, ich verstehe! Es hängt also nicht von einer Positionsänderung ab, weil es eine Eigenschaft der Welle in einem einzigen Augenblick ist. Aber warten Sie… wenn Ort und Impuls nur zwei verschiedene Aspekte derselben Welle sind...",
"en": "Ah, I see! So it doesn't depend on a change in position, because it's a feature of the wave at a single moment. But wait… if position and momentum are just two different aspects of the same wave...",
"zh": "啊，我明白了！所以它并不依赖于位置的变化，因为它是在一个特定时刻波的一个特征。等等…如果位置和动量只是同一波的不同方面……",
"ja": "ああ、なるほど！だから位置の変化とは関係ないのね。その瞬間の波自体の特徴だから。でも待って…もし位置と運動量が、同じ一つの波の、違う側面にすぎないとしたら…"
},{
"speaker": "Luc",
"fr": "Oui...",
"de": "Ja...",
"en": "Yes...",
"zh": "是的……",
"ja": "うん…"
},{
"speaker": "Camille",
"fr": "...ils doivent être connectés de quelque manière. Cela... cela me semble nous mener quelque part de très célèbre.",
"de": "...müssen sie irgendwie miteinander verbunden sein. Das... das fühlt sich an, als würde es uns zu etwas sehr Berühmtem führen.",
"en": "...they have to be connected somehow. This... this feels like it's leading us somewhere very famous.",
"zh": "……它们一定有某种联系。这……这感觉像是要引出一个非常著名的理论。",
"ja": "…それらは何らかの形で繋がっているはずよね。これって…何かすごく有名な話につながっていきそう。"
},{
"speaker": "Luc",
"fr": "C'est le chemin direct vers le principe d'incertitude de Heisenberg.",
"de": "Es ist der direkte Weg zum Heisenbergschen Unschärfeprinzip.",
"en": "It's the direct path to Heisenberg's Uncertainty Principle.",
"zh": "这就是通往海森堡不确定性原理的直接路径。",
"ja": "まさに、ハイゼンベルクの不確定性原理へまっすぐ続く道だよ。"
},{
"speaker": "Camille",
"fr": "Ah.",
"de": "Ah.",
"en": "Ah.",
"zh": "啊。",
"ja": "やっぱり。"
},{
"speaker": "Luc",
"fr": "Pensez-y. Pour avoir un momentum parfaitement défini, vous avez besoin d'une onde parfaite et uniforme — comme une note musicale pure — qui s'étend sans fin.",
"de": "Denken Sie es durch. Um einen perfekt definierten Impuls zu haben, braucht man eine perfekte, gleichmäßige Welle – wie eine reine musikalische Note –, die sich endlos ausdehnt.",
"en": "Think it through. To have a perfectly defined momentum, you need a perfect, uniform wave—like a pure musical note—that stretches on and on.",
"zh": "仔细想想。要有一个精确定义的动量，你需要一个完美、均匀的波——就像一个纯粹的音符，它持续不断地延伸。",
"ja": "考えてみて。運動量を完璧に一つに定めるには、どこまでも無限に続く、澄んだ音のような、完璧で均一な波が必要なんだ。"
},{
"speaker": "Camille",
"fr": "D'accord, une onde parfaitement régulière.",
"de": "Okay, eine perfekt regelmäßige Welle.",
"en": "Okay, a perfectly regular wave.",
"zh": "好的，一个非常规则的波。",
"ja": "なるほど、完全に均一な波ね。"
},{
"speaker": "Luc",
"fr": "Mais si votre onde s'étend partout, à travers l'ensemble de l'univers…",
"de": "Aber wenn sich Ihre Welle überall erstreckt, über das gesamte Universum…",
"en": "But if your wave extends everywhere, across the entire universe…",
"zh": "但是如果你的波延伸到整个宇宙……",
"ja": "でも、もしその波が宇宙の隅々まで広がっていたとしたら…"
},{
"speaker": "Camille",
"fr": "Oui?",
"de": "Ja?",
"en": "Yeah?",
"zh": "然后呢？",
"ja": "ええ。"
},{
"speaker": "Luc",
"fr": "...où se trouve la particule ?",
"de": "...wo ist dann das Teilchen?",
"en": "...where is the particle?",
"zh": "……粒子在哪里？",
"ja": "…その粒子は、どこに「ある」と言える？"
},{
"speaker": "Camille",
"fr": "Vous n'avez aucune idée. Sa position est complètement incertaine. Et… laissez-moi deviner… si vous voulez connaître sa position parfaitement…",
"de": "Man hat keine Ahnung. Sein Ort ist völlig unbestimmt. Und… lassen Sie mich raten… wenn man seinen Ort perfekt kennen will...",
"en": "You have no idea. Its position is completely uncertain. And… let me guess… if you want to know its position perfectly...",
"zh": "你根本不知道。它的位置是完全不确定的。而且……让我猜猜……如果你想精确地知道它的位置……",
"ja": "どこにも。位置が完全に不確定になる。…ということは、逆に、その位置を完璧に知りたいなら…"
},{
"speaker": "Luc",
"fr": "Allez-y.",
"de": "Fahren Sie fort.",
"en": "Go on.",
"zh": "继续。",
"ja": "どうなるかな？"
},{
"speaker": "Camille",
"fr": "l'onde doit être un pic unique et net.",
"de": "...muss die Welle eine einzige, scharfe Spitze sein.",
"en": "...the wave has to be a single, sharp spike.",
"zh": "……波必须是一个单一的尖峰。",
"ja": "…波は、たった一点だけの、鋭いトゲみたいな形にならないと。"
},{
"speaker": "Luc",
"fr": "Exactement. Mais une pointe n'a pas de longueur d'onde définie. C'est juste… une pointe.",
"de": "Genau. Aber eine Spitze hat keine definierte Wellenlänge. Sie ist nur… eine Spitze.",
"en": "Exactly. But a spike has no defined wavelength. It's just… a spike.",
"zh": "没错。但一个尖峰没有确定的波长。它只是……一个尖峰。",
"ja": "その通り。でも、そんなトゲには決まった波長がない。ただの…トゲだからね。"
},{
"speaker": "Camille",
"fr": "Exactement.",
"de": "Richtig.",
"en": "Right.",
"zh": "没错。",
"ja": "ですよね。"
},{
"speaker": "Luc",
"fr": "Donc, son « ondulation », son moment, deviennent complètement inconnus. Et ce n'est pas une limite de nos outils ; c'est un compromis fondamental inscrit dans la réalité.",
"de": "Ihre ‚Welligkeit‘, ihr Impuls, wird also völlig unbekannt. Und das ist keine Grenze unserer Instrumente; es ist ein fundamentaler Kompromiss, der in die Realität eingebaut ist.",
"en": "So its 'waviness,' its momentum, becomes completely unknown. And this isn't a limit of our tools; it's a fundamental trade-off baked into reality.",
"zh": "所以它的‘波纹度’，也就是它的动量，就变得完全未知了。这并非我们工具的限制，而是现实中一种根本的内在权衡。",
"ja": "だから、その「波っぽさ」、つまり運動量は完全に未知のものになる。これは測定器の限界じゃなくて、この現実そのものに組み込まれた、根本的なトレードオフなんだ。"
},{
"speaker": "Camille",
"fr": "C'est incroyable. Mais alors, comment les physiciens expérimentaux y parviennent-ils ?",
"de": "Das ist umwerfend. Aber wie machen es dann die Experimentalphysiker?",
"en": "That is mind-bending. But then, how do experimental physicists do it?",
"zh": "这太令人费解了。但实验物理学家是怎么做到的呢？",
"ja": "頭がクラクラするわ。でも、それなら実験物理学者の人たちはどうしてるの？"
},{
"speaker": "Luc",
"fr": "Ah!",
"de": "Ah!",
"en": "Ah!",
"zh": "啊！",
"ja": "ああ！"
},{
"speaker": "Camille",
"fr": "Comment obtiennent-ils une mesure précise du moment dans le monde réel ?",
"de": "Wie erhalten sie in der realen Welt eine präzise Impulsmessung?",
"en": "How do they get a precise momentum measurement in the real world?",
"zh": "在现实世界中，他们是如何获得精确的动量测量的呢？",
"ja": "現実の世界で、どうやって正確な運動量を測っているのかしら？"
},{
"speaker": "Luc",
"fr": "C'est ici que l'intelligence remarquable de la physique moderne entre en jeu.",
"de": "Hier kommt die schiere Genialität der modernen Physik ins Spiel.",
"en": "This is where the sheer cleverness of modern physics comes in.",
"zh": "这正是现代物理学精妙绝伦之处。",
"ja": "そこにこそ、現代物理学の真の賢さがあるんだよ。"
},{
"speaker": "Camille",
"fr": "D'accord...",
"de": "Okay...",
"en": "Okay...",
"zh": "好吧……",
"ja": "へえ…"
},{
"speaker": "Luc",
"fr": "Ils utilisent des stratégies ingénieuses et indirectes. Mon exemple préféré est de prendre un électron et de le placer dans un champ magnétique.",
"de": "Sie verwenden ausgeklügelte, indirekte Strategien. Mein Lieblingsbeispiel ist, ein Elektron in ein Magnetfeld zu bringen.",
"en": "They use ingenious, indirect strategies. My favorite example is to take an electron and place it in a magnetic field.",
"zh": "他们使用巧妙的、间接的策略。我最喜欢的一个例子是取一个电子，并将其置于磁场中。",
"ja": "彼らは、巧妙で間接的な戦略を使う。僕の好きな例は、電子を磁場の中に入れる方法だ。"
},{
"speaker": "Camille",
"fr": "D'accord, donc il va commencer à se déplacer en cercle.",
"de": "Okay, dann wird es sich im Kreis bewegen.",
"en": "Okay, so it will start to move in a circle.",
"zh": "好的，所以它会开始做圆周运动。",
"ja": "なるほど、そうすると円を描いて動き始めるわね。"
},{
"speaker": "Luc",
"fr": "Exactement. Maintenant, vous le laissez accomplir exactement une demi-tour.",
"de": "Richtig. Nun lässt man es genau eine halbe Umdrehung vollziehen.",
"en": "Correct. Now, you let it complete exactly one half-turn.",
"zh": "正确。现在，让它刚好转半圈。",
"ja": "その通り。そして、電子にちょうど半周だけ回転させる。"
},{
"speaker": "Camille",
"fr": "D'accord.",
"de": "Okay.",
"en": "Okay.",
"zh": "好的。",
"ja": "ええ。"
},{
"speaker": "Luc",
"fr": "Et à ce moment précis, vous mesurez sa position.",
"de": "Und in genau diesem Moment misst man seine Position.",
"en": "And at that precise moment, you measure its position.",
"zh": "而在那个精确的时刻，你测量它的位置。",
"ja": "そして、その瞬間に、電子の位置を測定するんだ。"
},{
"speaker": "Camille",
"fr": "Vous mesurez sa position. Et… qu'est-ce que cela vous apprend ?",
"de": "Man misst seine Position. Und… was sagt Ihnen das?",
"en": "You measure its position. And… what does that tell you?",
"zh": "你测量它的位置。然后呢……这能告诉我们什么？",
"ja": "位置を測るのね。それで…何がわかるの？"
},{
"speaker": "Luc",
"fr": "C'est là que réside la magie. Cette mesure unique de sa position finale vous dit, avec une précision incroyable, quelle était sa quantité de mouvement initiale…",
"de": "Hier kommt der Clou. Diese einzige Messung seiner Endposition verrät Ihnen mit unglaublicher Präzision, was sein anfänglicher Impuls war...",
"en": "Here’s the magic. That single measurement of its final position tells you, with incredible precision, what its initial momentum was...",
"zh": "奇妙之处就在于此。对它最终位置的单次测量，就能以惊人的精度告诉你，它最初的动量是多少……",
"ja": "ここからがマジックだ。その最終的な位置を一度測るだけで、信じられないほど正確に、その電子が最初に持っていた運動量がわかるんだ…"
},{
"speaker": "Camille",
"fr": "Wow.",
"de": "Wow.",
"en": "Wow.",
"zh": "哇！",
"ja": "すごい！"
},{
"speaker": "Luc",
"fr": "...exactement au début.",
"de": "...ganz am Anfang.",
"en": "...right back at the start.",
"zh": "……在它开始运动时的动量。",
"ja": "…一番最初のね。"
},{
"speaker": "Camille",
"fr": "Attendez, vous me dites que mesurer où il est maintenant nous apprend comment il se déplaçait autrefois ?",
"de": "Warten Sie, Sie sagen mir, dass die Messung, wo es jetzt ist, Ihnen sagt, wie es sich damals bewegt hat?",
"en": "Wait, you're telling me that measuring where it is now tells you how it was moving back then?",
"zh": "等等，你的意思是，测量它现在的位置，就能知道它过去是如何运动的吗？",
"ja": "待って、今どこにいるかを測ることで、過去にどう動いていたかがわかるってこと？"
},{
"speaker": "Luc",
"fr": "Oui.",
"de": "Ja.",
"en": "Yeah.",
"zh": "是的。",
"ja": "そう。"
},{
"speaker": "Camille",
"fr": "Ça semble impossible.",
"de": "Das klingt unmöglich.",
"en": "That sounds impossible.",
"zh": "这听起来不可能。",
"ja": "そんなの、不可能に聞こえるわ。"
},{
"speaker": "Luc",
"fr": "C'est une belle idée appelée « mesure généralisée ». Au lieu d'essayer de mesurer directement le moment, vous laissez le système évoluer d'une manière qui traduit proprement l'information que vous souhaitez — le moment — en un autre type d'information plus facile à mesurer, comme la position.",
"de": "Es ist ein wunderschönes Konzept, das als ‚verallgemeinerte Messung‘ bezeichnet wird. Anstatt zu versuchen, den Impuls direkt zu messen, lässt man das System sich so entwickeln, dass die gewünschte Information – der Impuls – sauber in eine andere, leichter zu messende Information, wie den Ort, übersetzt wird.",
"en": "It's a beautiful concept called a 'generalized measurement.' Instead of trying to measure momentum directly, you... you let the system evolve in a way that neatly translates the information you want—the momentum—into a different kind of information that's easier to measure, like position.",
"zh": "这是一个很巧妙的概念，叫做‘广义测量’。你不是直接去测量动量，而是让系统以一种巧妙的方式演化，把你想要的信息——动量——转换成另一种更容易测量的、不同的信息，比如位置。",
"ja": "これは「一般化測定」と呼ばれる美しい概念なんだ。運動量を直接測ろうとするんじゃなくて、システムをうまく変化させて、知りたい情報を、もっと測りやすい別の情報に変換してやるんだよ。"
},{
"speaker": "Camille",
"fr": "Donc, une mesure n'est pas simplement un regard passif.",
"de": "Eine Messung ist also nicht nur ein passiver Blick.",
"en": "So, a measurement isn't just a passive look.",
"zh": "所以，测量不仅仅是被动的观察。",
"ja": "じゃあ、測定っていうのは、ただ受動的に眺めることじゃないのね。"
},{
"speaker": "Luc",
"fr": "Non",
"de": "Nein.",
"en": "No.",
"zh": "不。",
"ja": "違う。"
},{
"speaker": "Camille",
"fr": "C'est un processus actif, une stratégie. Vous manipulez le système pour qu'il vous révèle ses secrets.",
"de": "Es ist ein aktiver Prozess, eine Strategie. Man manipuliert das System, damit es einem seine Geheimnisse verrät.",
"en": "It's an active process, a strategy. You're manipulating the system to make it tell you its secrets.",
"zh": "这是一个主动的过程，一种策略。你是在操控系统，让它告诉你它的秘密。",
"ja": "能動的なプロセスで、戦略なのね。システムを操作して、秘密を吐き出させる、みたいな。"
},{
"speaker": "Luc",
"fr": "Vous l'avez parfaitement capturé. Une grandeur physique dans le monde quantique n'est pas une propriété statique attendant d'être lue.",
"de": "Sie haben es perfekt erfasst. Eine physikalische Größe in der Quantenwelt ist keine statische Eigenschaft, die darauf wartet, abgelesen zu werden.",
"en": "You've captured it perfectly. A physical quantity in the quantum world is not a static property waiting to be read.",
"zh": "你总结得非常到位。量子世界中的物理量不是一个等待被读取的静态属性。",
"ja": "まさにその通り。量子世界における物理的な量というのは、ただそこにあって読み取られるのを待っている静的な特性じゃないんだ。"
},{
"speaker": "Camille",
"fr": "Hmm.",
"de": "Hmm.",
"en": "Hmm.",
"zh": "嗯。",
"ja": "ふむ。"
},{
"speaker": "Luc",
"fr": "C'est le résultat d'une action dynamique que vous effectuez sur le système. La question de l'auditeur révèle vraiment cette toute nouvelle révolution dans la pensée.",
"de": "Sie ist das Ergebnis einer dynamischen Handlung, die man am System vornimmt. Die Frage des Hörers deckt wirklich diesen gesamten, revolutionären Denkwandel auf.",
"en": "It is the outcome of a dynamic action you perform on the system. That listener's question, it really uncovers that entire, revolutionary shift in thinking.",
"zh": "它是你对系统进行动态作用的结果。那位听众的问题，真正揭示了这种思想上革命性的转变。",
"ja": "それは、君がシステムに対して行う動的な「行為」の結果なんだ。あのリスナーの質問は、まさにこの革命的な思考の転換を、見事に言い当てているよ。"
},{
"speaker": "Camille",
"fr": "Cela remet complètement en question le monde. Luc, merci. C'était d'une clarté saisissante.",
"de": "Das stellt die Welt völlig neu dar. Luc, vielen Dank. Das war erstaunlich klar.",
"en": "That completely reframes the world. Luc, thank you. That was stunningly clear.",
"zh": "这完全重塑了我们对世界的看法。卢克，谢谢你。你解释得太清楚了。",
"ja": "世界の見方がまったく変わってしまうわ。リュック、ありがとう。息をのむほど分かりやすかった。"
},{
"speaker": "Luc",
"fr": "C’était un plaisir, Camille.",
"de": "Gern geschehen, Camille.",
"en": "It was my pleasure, Camille.",
"zh": "我的荣幸，卡米尔。",
"ja": "どういたしまして、カミーユ。"
},{
"speaker": "Camille",
"fr": "Maintenant, voici une question à laquelle nous aimerions que vous réfléchissiez. Si la nature vous forçait à faire un choix, préféreriez-vous connaître avec une absolue et parfaite certitude : exactement où vous êtes en ce moment...",
"de": "Nun eine Frage, über die wir Sie zum Nachdenken anregen möchten. Wenn die Natur Sie zwingen würde, eine Wahl zu treffen, was wüssten Sie lieber mit absoluter, perfekter Sicherheit: genau, wo Sie sich in diesem Moment befinden...",
"en": "Now, here's a question we'd like you to think about. If nature forced you to make a choice, which would you rather know with absolute, perfect certainty: exactly where you are in this moment...",
"zh": "现在，我们想请大家思考一个问题。如果自然法则迫使你做出选择，你更希望确切地知道以下哪一个：是你此刻的精确位置……",
"ja": "さて、ここでリスナーの皆さんに考えていただきたい質問があります。もし自然があなたに選択を迫るとしたら、絶対に、完璧な確実性をもって知りたいのは…今この瞬間、自分が「どこにいるか」ということ？"
},{
"speaker": "Luc",
"fr": "Hmm.",
"de": "Hmm.",
"en": "Hmm.",
"zh": "嗯。",
"ja": "ふむ。"
},{
"speaker": "Camille",
"fr": "ou la direction et la quantité de mouvement exactes avec lesquelles vous avancez ?",
"de": "...oder die genaue Richtung und den Impuls, mit dem Sie sich vorwärtsbewegen?",
"en": "...or the exact direction and momentum with which you are moving forward?",
"zh": "……还是你前进的确切方向和动量？",
"ja": "…それとも、自分が「どの方向へ、どんな勢いで進んでいるか」ということ？"
},{
"speaker": "Luc",
"fr": "Et comment ce choix changerait-il votre vision de votre propre existence ?",
"de": "Und wie würde diese Wahl Ihre Sicht auf Ihre eigene Existenz verändern?",
"en": "And how would that choice change your view of your own existence?",
"zh": "这个选择会如何改变你对自身存在的看法呢？",
"ja": "そして、その選択は、あなた自身の存在についての考え方を、どう変えるだろうか？"
},{
"speaker": "Camille",
"fr": "À la prochaine sur « Passerelles en Physique », restez curieux.",
"de": "Bis zum nächsten Mal bei „Brücken in die Physik“, bleiben Sie neugierig.",
"en": "Until next time on \"Bridges in Physics,\" stay curious.",
"zh": "《物理之桥》节目，我们下期再会。保持好奇。",
"ja": "次回の『物理の架け橋』まで、好奇心を持ち続けてくださいね。"
}]
);
