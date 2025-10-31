// Initialize datasets array if undefined
if (typeof datasets === 'undefined') {
    var datasets = [];
}

// Add dataset to datasets array
datasets.push(
[{
"speaker": "Camille",
"fr": "Bonjour à toutes et à tous, et bienvenue dans « Passerelles en Physique ». Le podcast où, eh bien, on jette un pont entre les mystères du monde quantique et la physique de notre quotidien.",
"de": "Hallo an alle, und herzlich willkommen bei \"Brücken in die Physik\". Der Podcast, in dem wir eine Brücke zwischen den Geheimnissen der Quantenwelt und der Physik unseres Alltags schlagen.",
"en": "Hello everyone, and welcome to \"Bridges in Physics\". The podcast where, well, we build a bridge between the mysteries of the quantum world and the physics of our everyday lives.",
"zh": "大家好，欢迎来到《物理之桥》。这是一个播客节目，在这里我们将量子世界的奥秘与我们日常生活中的物理原理连接起来。",
"ja": "皆さん、こんにちは。「物理の架け橋」へようこそ。量子世界の神秘と、私たちの日常生活に潜む物理学の間に橋を架けるポッドキャストです。",
"es": "Hola a todos y a todas, y bienvenidos a \"Puentes en Física\". El podcast donde, bueno, tendemos un puente entre los misterios del mundo cuántico y la física de nuestro día a día."
},{
"speaker": "Luc",
"fr": "C'est exactement ça ! Bonjour tout le monde.",
"de": "Genau! Hallo an alle!",
"en": "That's exactly right! Hello everyone.",
"zh": "完全正确！大家好。",
"ja": "その通りだね！皆さん、こんにちは。",
"es": "¡Exactamente! Hola a todos."
},{
"speaker": "Camille",
"fr": "Je suis Camille, physicienne théoricienne.",
"de": "Ich bin Camille, theoretische Physikerin.",
"en": "I'm Camille, a theoretical physicist.",
"zh": "我是Camille，一位理论物理学家。",
"ja": "私はカミーユ、理論物理学者です。",
"es": "Soy Camille, física teórica."
},{
"speaker": "Luc",
"fr": "Et je suis Luc, physicien expérimentateur. Camille, pour commencer, j'aimerais qu'on plonge directement dans une image que... que tout le monde connaît, en fait.",
"de": "Und ich bin Luc, experimenteller Physiker. Camille, um zu beginnen, möchte ich gleich in ein Bild eintauchen, das... naja, jeder kennt.",
"en": "And I'm Luc, an experimental physicist. Camille, to start, I'd like to dive right into an image that... that everyone knows, in fact.",
"zh": "我是Luc，一位实验物理学家。Camille，我们先从一个大家都知道的图像开始吧。",
"ja": "そして僕はリュック、実験物理学者だ。カミーユ、まず、誰もが知っているイメージから話を始めたいんだ。",
"es": "Y yo soy Luc, físico experimental. Camille, para empezar, me gustaría que nos sumergiéramos directamente en una imagen que... que todo el mundo conoce, de hecho."
},{
"speaker": "Camille",
"fr": "Oui ?",
"de": "Ja?",
"en": "Yes?",
"zh": "好的？",
"ja": "なあに？",
"es": "¿Sí?"
},{
"speaker": "Luc",
"fr": "On nous dit tout le temps que les particules, comme les électrons, se comportent comme des ondes. Mais... est-ce que ça veut dire qu'il y a une véritable petite vague matérielle qui ondule dans l'espace ? Un peu comme une ride à la surface de l'eau ?",
"de": "Man sagt uns ständig, dass Teilchen wie Elektronen sich wie Wellen verhalten. Aber... bedeutet das wirklich, dass es eine echte kleine materielle Welle gibt, die im Raum schwingt? Ein bisschen so wie eine Welle auf der Wasseroberfläche?",
"en": "We're constantly told that particles, like electrons, behave like waves. But... does that mean there's a real little material wave that undulates in space? A bit like a ripple on the surface of water?",
"zh": "我们总被告知像电子这样的粒子表现得像波一样。但是……难道这就意味着有一个真正的小型物质波在空间中起伏不定吗？就好比水面上的涟漪一样？",
"ja": "電子のような粒子は波のように振る舞うと、よく言われるよね。でも…それって、空間を実際にうねって進む、物質の小さな波が本当にあるっていうことなのかな？水面に広がる波紋みたいにさ。",
"es": "Nos dicen constantemente que las partículas, como los electrones, se comportan como ondas. Pero... ¿significa eso que hay una verdadera pequeña onda material que ondula en el espacio? ¿Un poco como una onda en la superficie del agua?"
},{
"speaker": "Camille",
"fr": "C'est une question absolument fondamentale, Luc, parce que ça touche à notre intuition la plus profonde.",
"de": "Das ist eine absolut grundlegende Frage, Luc, weil sie unsere tiefste Intuition berührt.",
"en": "It's an absolutely fundamental question, Luc, because it touches on our deepest intuition.",
"zh": "Luc，这是一个非常根本的问题，因为它触及我们最深刻的直觉。",
"ja": "それはとても根源的な問いね、リュック。だって、私たちの最も深い直感に触れる問題だから。",
"es": "Es una pregunta absolutamente fundamental, Luc, porque toca nuestra intuición más profunda."
},{
"speaker": "Luc",
"fr": "Oui.",
"de": "Ja.",
"en": "Yes.",
"zh": "是的。",
"ja": "うん。",
"es": "Sí."
},{
"speaker": "Camille",
"fr": "Et la réponse, qui a mis un siècle à s'imposer, est à la fois simple et… déroutante : non. Non, cette onde, que les physiciens nomment la fonction d'onde, psi... n'est pas une onde de matière.",
"de": "Und die Antwort, die sich nach einem Jahrhundert durchgesetzt hat, ist zugleich einfach und… verblüffend: nein. Nein, diese Welle, die Physiker die Wellenfunktion, Psi, nennen... ist keine materielle Welle.",
"en": "And the answer, which took a century to become established, is both simple and... perplexing: no. No, this wave, which physicists call the wave function, psi... is not a wave of matter.",
"zh": "答案花了一个世纪才得以确立，它既简单又……令人困惑：不。不，这个波，物理学家称之为波函数，psi……它不是物质波。",
"ja": "そして、定着するのに1世紀もかかったその答えは、単純でありながら…人を惑わせるものでもあるの。答えは「ノー」。物理学者が波動関数、プサイと呼ぶこの波は、物質の波ではないのよ。",
"es": "Y la respuesta, que tardó un siglo en imponerse, es a la vez simple y… desconcertante: no. No, esta onda, que los físicos llaman la función de onda, psi... no es una onda de materia."
},{
"speaker": "Luc",
"fr": "D'accord...",
"de": "Verstehe...",
"en": "I see...",
"zh": "我明白了……",
"ja": "なるほど…",
"es": "De acuerdo..."
},{
"speaker": "Camille",
"fr": "C'est une onde de… possibilités.",
"de": "Es ist eine Welle von… Möglichkeiten.",
"en": "It's a wave of... possibilities.",
"zh": "这是一个……可能性的波。",
"ja": "それは…可能性の波。",
"es": "Es una onda de… posibilidades."
},{
"speaker": "Luc",
"fr": "Une onde de possibilités… Vous voulez dire qu'elle ne décrit pas un objet réel, mais plutôt la... la probabilité de trouver l'objet quelque part ?",
"de": "Eine Welle von Möglichkeiten... Sie meinen also, sie beschreibt kein reales Objekt, sondern eher die... die Wahrscheinlichkeit, das Objekt irgendwo zu finden?",
"en": "A wave of possibilities... Do you mean it doesn't describe a real object, but rather the... the probability of finding the object somewhere?",
"zh": "可能性的波……你是说它描述的不是一个真实的物体，而是……在某个地方找到这个物体的概率？",
"ja": "可能性の波…つまり、それは実在する物体を記述しているんじゃなくて、その物体がどこかで見つかる…確率を表しているということかい？",
"es": "Una onda de posibilidades… ¿Quiere decir que no describe un objeto real, sino más bien la… la probabilidad de encontrar el objeto en algún lugar?"
},{
"speaker": "Camille",
"fr": "Exactement. Et pour être tout à fait précis, ce n'est pas l'onde elle-même qui est la probabilité.",
"de": "Genau. Und um ganz präzise zu sein: Nicht die Welle selbst ist die Wahrscheinlichkeit.",
"en": "Exactly. And to be perfectly precise, it's not the wave itself that is the probability.",
"zh": "正是如此。更准确地说，波本身并不是概率。",
"ja": "その通り。でも正確に言うと、確率そのものが波というわけではないの。",
"es": "Exactamente. Y para ser del todo preciso, no es la onda en sí misma la probabilidad."
},{
"speaker": "Luc",
"fr": "D'accord.",
"de": "Okay.",
"en": "Okay.",
"zh": "好的。",
"ja": "わかった。",
"es": "De acuerdo."
},{
"speaker": "Camille",
"fr": "C'est le carré de son amplitude. Ou de sa « hauteur », si vous préférez.",
"de": "Sondern das Quadrat ihrer Amplitude. Oder ihrer \"Höhe\", wenn Sie so wollen.",
"en": "It's the square of its amplitude. Or its \"height\", if you prefer.",
"zh": "是它振幅的平方。或者，如果你愿意，也可以说是它的‘高度’。",
"ja": "その振幅の2乗よ。あるいは、分かりやすく言えばその「高さ」の2乗ね。",
"es": "Es el cuadrado de su amplitud. O de su \"altura\", si lo prefieres."
},{
"speaker": "Luc",
"fr": "Ah oui.",
"de": "Ah ja.",
"en": "Ah yes.",
"zh": "啊，是的。",
"ja": "ああ、なるほど。",
"es": "Ah sí."
},{
"speaker": "Camille",
"fr": "On note ça psi au carré. C'est la fameuse règle de Born, un des piliers de la mécanique quantique.",
"de": "Man schreibt das als Psi-Quadrat. Das ist die berühmte Bornsche Regel, einer der Grundpfeiler der Quantenmechanik.",
"en": "We denote that as psi squared. That's the famous Born rule, one of the pillars of quantum mechanics.",
"zh": "我们将其记为ψ的平方。这就是著名的玻恩定则，量子力学的支柱之一。",
"ja": "それをプサイの2乗と書くの。これが有名なボルンの規則で、量子力学の根幹を成す考え方の一つよ。",
"es": "Lo notamos como psi al cuadrado. Es la famosa regla de Born, uno de los pilares de la mecánica cuántica."
},{
"speaker": "Luc",
"fr": "Ah, ça, c'est un phénomène que je vois tous les jours au labo !",
"de": "Ah, das ist ein Phänomen, das ich jeden Tag im Labor sehe!",
"en": "Ah, that's a phenomenon I see every day in the lab!",
"zh": "哦，这是我在实验室每天都能看到的现象！",
"ja": "ああ、それは僕がラボで毎日目にしている現象だよ！",
"es": "¡Ah, eso es un fenómeno que veo todos los días en el laboratorio!"
},{
"speaker": "Camille",
"fr": "Ah oui ?",
"de": "Ah ja?",
"en": "Ah yes?",
"zh": "啊，是的？",
"ja": "あら、そうなの？",
"es": "¡Ah, sí?"
},{
"speaker": "Luc",
"fr": "Quand on fait l'expérience des fentes de Young en envoyant des électrons un par un, chaque électron laisse un seul impact sur l'écran, comme une particule.",
"de": "Wenn wir das Doppelspaltexperiment durchführen, indem wir Elektronen einzeln aussenden, hinterlässt jedes Elektron einen einzigen Einschlag auf dem Schirm, wie ein Teilchen.",
"en": "When we perform the double-slit experiment by sending electrons one by one, each electron leaves a single impact on the screen, like a particle.",
"zh": "当我们通过逐个发射电子来进行双缝实验时，每个电子都会在屏幕上留下一个单一的撞击点，就像粒子一样。",
"ja": "ヤングの二重スリット実験で電子を一つずつ撃つと、個々の電子は粒子みたいに、スクリーンに一つの点としてぶつかる。",
"es": "Cuando hacemos el experimento de las rendijas de Young enviando electrones uno por uno, cada electrón deja un solo impacto en la pantalla, como una partícula."
},{
"speaker": "Camille",
"fr": "Oui...",
"de": "Ja...",
"en": "Yes...",
"zh": "是的……",
"ja": "ええ…",
"es": "Sí..."
},{
"speaker": "Luc",
"fr": "Mais... après en avoir envoyé des milliers, on voit se dessiner cette figure avec des franges... une figure d'interférence.",
"de": "Aber... nachdem wir Tausende davon ausgesandt haben, sehen wir, wie sich dieses Muster mit Streifen abzeichnet... ein Interferenzmuster.",
"en": "But... after sending thousands of them, you see this pattern emerge with fringes... an interference pattern.",
"zh": "但是……在发射了数千个电子之后，你会看到带有干涉条纹的图案出现。",
"ja": "でも…何千個も撃った後には、縞模様が…干渉縞が現れるんだ。",
"es": "Pero... después de haber enviado miles, vemos dibujarse esta figura con franjas... una figura de interferencia."
},{
"speaker": "Camille",
"fr": "Hmm.",
"de": "Hm.",
"en": "Hmm.",
"zh": "嗯。",
"ja": "ふむ。",
"es": "Hmm."
},{
"speaker": "Luc",
"fr": "Et cette distribution, elle est magnifique, elle suit à la perfection la loi en psi au carré.",
"de": "Und diese Verteilung ist wunderschön; sie folgt perfekt dem Gesetz von Psi-Quadrat.",
"en": "And this distribution, it's magnificent, it perfectly follows the law of psi squared.",
"zh": "而这个分布非常壮观，它完美地遵循了psi平方定律。",
"ja": "そして、この分布は見事なまでに、プサイの2乗 の法則にぴったり一致するんだ。",
"es": "Y esta distribución es magnífica, sigue a la perfección la ley en psi al cuadrado."
},{
"speaker": "Camille",
"fr": "C'est la preuve expérimentale irréfutable. Mais ça nous amène à la question... pourquoi le carré ?",
"de": "Das ist der unwiderlegbare experimentelle Beweis. Aber das bringt uns zu der Frage... warum das Quadrat?",
"en": "That's the irrefutable experimental proof. But that brings us to the question... why the square?",
"zh": "这是无可辩驳的实验证据。但这就引出了一个问题……为什么要平方？",
"ja": "これが反論のしようがない実験的な証拠ね。でも、ここから次の疑問が生まれる…なぜ2乗なのか？",
"es": "Es la prueba experimental irrefutable. Pero eso nos lleva a la pregunta... ¿por qué el cuadrado?"
},{
"speaker": "Luc",
"fr": "Oui !",
"de": "Ja!",
"en": "Yes!",
"zh": "是的！",
"ja": "そうだ！",
"es": "¡Sí!"
},{
"speaker": "Camille",
"fr": "Pourquoi la nature a-t-elle choisi cette complexité ? Une probabilité directe, juste liée à psi, ça semblerait tellement plus simple, non ?",
"de": "Warum hat die Natur diese Komplexität gewählt? Eine direkte Wahrscheinlichkeit, die nur mit Psi verknüpft ist, würde doch viel einfacher erscheinen, oder?",
"en": "Why did nature choose this complexity? A direct probability, just linked to psi, would seem so much simpler, wouldn't it?",
"zh": "为什么自然选择了这种复杂性？一个与psi直接关联的概率，看起来会简单得多，不是吗？",
"ja": "なぜ自然はこんなに複雑な仕組みを選んだのかしら？単にプサイに比例する確率のほうが、ずっと単純でしょう？",
"es": "Camille: ¿Por qué la naturaleza ha elegido esta complejidad? Una probabilidad directa, simplemente relacionada con psi, parecería mucho más simple, ¿no?"
},{
"speaker": "Luc",
"fr": "Tout à fait ! Pourquoi cette étape en plus ?",
"de": "Absolut! Warum dieser zusätzliche Schritt?",
"en": "Exactly! Why this extra step?",
"zh": "正是！为什么需要这额外的一步？",
"ja": "まったくその通りだ！ なぜ、わざわざ一手間加える必要があるんだろう？",
"es": "¡Exactamente! ¿Por qué este paso adicional?"
},{
"speaker": "Camille",
"fr": "Alors, il y a une raison mathématique, euh... implacable : la conservation.",
"de": "Also, es gibt einen unumstößlichen mathematischen Grund: die Erhaltung.",
"en": "So, there's a mathematical reason, uh... implacable: conservation.",
"zh": "嗯，有一个不可动摇的数学原因：守恒。",
"ja": "それには、数学的な、ええと…動かしがたい理由があるの。それは「保存」よ。",
"es": "Entonces, hay una razón matemática, eh... implacable: la conservación."
},{
"speaker": "Luc",
"fr": "D'accord.",
"de": "Verstehe.",
"en": "I understand.",
"zh": "我明白。",
"ja": "なるほど。",
"es": "De acuerdo."
},{
"speaker": "Camille",
"fr": "La probabilité totale de trouver la particule quelque part dans l'univers, elle doit toujours être de 100%.",
"de": "Die Gesamtwahrscheinlichkeit, das Teilchen irgendwo im Universum zu finden, muss immer 100 % betragen.",
"en": "The total probability of finding the particle somewhere in the universe must always be 100%.",
"zh": "在宇宙中任何地方找到粒子的总概率必须始终是100%。",
"ja": "宇宙のどこかである粒子を見つける確率の合計は、常に100%でなければならない。",
"es": "La probabilidad total de encontrar la partícula en algún lugar del universo siempre debe ser del 100%."
},{
"speaker": "Luc",
"fr": "Toujours.",
"de": "Immer.",
"en": "Always.",
"zh": "始终如此。",
"ja": "いつでも。",
"es": "Siempre."
},{
"speaker": "Camille",
"fr": "Elle ne peut pas apparaître ou disparaître. Et il se trouve que seule la forme psi au carré garantit que cette règle est respectée. Tout le temps.",
"de": "Es kann nicht einfach erscheinen oder verschwinden. Und es stellt sich heraus, dass nur die Form Psi-Quadrat garantiert, dass diese Regel jederzeit eingehalten wird.",
"en": "It cannot appear or disappear. And it happens that only the form psi squared guarantees that this rule is respected. All the time.",
"zh": "它不能出现或消失。而只有psi平方这种形式才能保证这条规则始终成立。",
"ja": "勝手に現れたり消えたりはできない。そして、プサイの2乗という形だけが、このルールが常に守られることを保証してくれるのよ。",
"es": "No puede aparecer ni desaparecer. Y resulta que solo la forma psi al cuadrado garantiza que esta regla se respete. Todo el tiempo."
},{
"speaker": "Luc",
"fr": "D'accord.",
"de": "Okay.",
"en": "Okay.",
"zh": "好的。",
"ja": "なるほど。",
"es": "De acuerdo."
},{
"speaker": "Camille",
"fr": "Mais... il y a une raison encore plus belle. Une raison qui fait le lien avec votre domaine, Luc.",
"de": "Aber... es gibt einen noch schöneren Grund. Ein Grund, der eine Verbindung zu Ihrem Fachgebiet herstellt, Luc.",
"en": "But... there's an even more beautiful reason. A reason that connects to your field, Luc.",
"zh": "但是……还有一个更妙的理由。一个与你的领域相关的理由，Luc。",
"ja": "でも…もっと美しい理由もあるの。あなたの専門分野につながる理由がね、リュック。",
"es": "Pero... hay una razón aún más hermosa. Una razón que conecta con tu campo, Luc."
},{
"speaker": "Luc",
"fr": "Ah ? Laquelle ?",
"de": "Aha? Welcher?",
"en": "Ah? Which one?",
"zh": "哦？是什么？",
"ja": "え？どんな？",
"es": "Ah, ¿cuál?"
},{
"speaker": "Camille",
"fr": "En optique classique, l'énergie d'une onde lumineuse, ce qui fait sa brillance, est elle aussi proportionnelle au carré de l'amplitude du champ électrique. E au carré.",
"de": "In der klassischen Optik ist die Energie einer Lichtwelle, die ihre Helligkeit ausmacht, ebenfalls proportional zum Quadrat der Amplitude des elektrischen Feldes. E-Quadrat.",
"en": "In classical optics, the energy of a light wave, which gives it its brilliance, is also proportional to the square of the amplitude of the electric field. E squared.",
"zh": "在经典光学中，光波的能量（也就是它的亮度）也与电场振幅的平方成正比，即E的平方。",
"ja": "古典光学では、光波のエネルギー、つまりその明るさは、同じく電場の振幅の2乗に比例するの。Eの2乗にね。",
"es": "En óptica clásica, la energía de una onda luminosa, lo que determina su brillo, también es proporcional al cuadrado de la amplitud del campo eléctrico. E al cuadrado."
},{
"speaker": "Luc",
"fr": "Wow.",
"de": "Wow.",
"en": "Wow.",
"zh": "哇！",
"ja": "へえ。",
"es": "Vaya."
},{
"speaker": "Camille",
"fr": "C'est un parallèle absolument stupéfiant.",
"de": "Das ist eine absolut verblüffende Parallele.",
"en": "That's an absolutely stunning parallel.",
"zh": "这是一个非常惊人的相似之处。",
"ja": "これは本当に驚くべき類似点だわ。",
"es": "Es un paralelismo absolutamente asombroso."
},{
"speaker": "Luc",
"fr": "Attends. Donc la « probabilité de présence » d'une particule quantique... se calcule de la même manière que « l'énergie » d'une onde lumineuse classique.",
"de": "Moment. Die \"Anwesenheitswahrscheinlichkeit\" eines Quantenteilchens... wird also auf die gleiche Weise berechnet wie die \"Energie\" einer klassischen Lichtwelle.",
"en": "Wait. So the 'probability of presence' of a quantum particle... is calculated in the same way as 'the energy' of a classical light wave.",
"zh": "等等。那么一个量子粒子的‘存在概率’……和经典光波的‘能量’是用同样的方式计算的。",
"ja": "待ってくれ。ということは、量子的な粒子の「存在確率」は…古典的な光の波の「エネルギー」と、まったく同じ方法で計算されるということかい？",
"es": "Espera. Entonces, la \"probabilidad de presencia\" de una partícula cuántica... se calcula de la misma manera que la \"energía\" de una onda luminosa clásica."
},{
"speaker": "Camille",
"fr": "Oui.",
"de": "Ja.",
"en": "Yes.",
"zh": "是的。",
"ja": "ええ。",
"es": "Sí."
},{
"speaker": "Luc",
"fr": "C'est la même loi mathématique pour deux mondes si différents. Ce n'est pas une coïncidence.",
"de": "Es ist dasselbe mathematische Gesetz für zwei so unterschiedliche Welten. Das ist kein Zufall.",
"en": "It's the same mathematical law for two such different worlds. It's not a coincidence.",
"zh": "对于两个如此不同的世界，竟然是同一个数学定律。这不是巧合。",
"ja": "こんなに違う2つの世界で、同じ数学法則が成り立っているなんて。これは偶然じゃないはずだ。",
"es": "Es la misma ley matemática para dos mundos tan diferentes. No es una coincidencia."
},{
"speaker": "Camille",
"fr": "Non. C'est un des plus beaux exemples de l'unité de la physique. Et ça nous amène à une autre intuition à questionner.",
"de": "Nein. Das ist eines der schönsten Beispiele für die Einheit der Physik. Und das führt uns zu einer weiteren Intuition, die wir hinterfragen müssen.",
"en": "No. It's one of the most beautiful examples of the unity of physics. And that leads us to another intuition to question.",
"zh": "没错。这是物理学统一性的最美妙的例子之一。这也引导我们去质疑另一个直觉。",
"ja": "ええ。物理学の統一性を示す、最も美しい例の1つよ。そして、ここからまた別の直感に疑問を投げかけることになるわ。",
"es": "No. Es uno de los ejemplos más hermosos de la unidad de la física. Y eso nos lleva a otra intuición que cuestionar."
},{
"speaker": "Luc",
"fr": "Ah ?",
"de": "Ah?",
"en": "Ah?",
"zh": "哦？",
"ja": "ほう？",
"es": "Ah?"
},{
"speaker": "Camille",
"fr": "Parlons de l'amplitude et de la largeur spatiale d'une onde. Une onde très « haute » est-elle forcément très « large » ?",
"de": "Sprechen wir über die Amplitude und die räumliche Ausdehnung einer Welle. Ist eine sehr \"hohe\" Welle zwangsläufig auch sehr \"breit\"?",
"en": "Let's talk about the amplitude and spatial width of a wave. Is a very 'high' wave necessarily very 'wide'?",
"zh": "我们来谈谈波的振幅和空间宽度。一个非常‘高’的波一定非常‘宽’吗？",
"ja": "波の振幅と空間的な幅について話しましょうか。とても「高い」波は、必ずしも「広い」波なのかな？",
"es": "Hablemos de la amplitud y el ancho espacial de una onda. ¿Una onda muy \"alta\" es necesariamente muy \"ancha\"?"
},{
"speaker": "Luc",
"fr": "Mon premier réflexe serait de dire oui. Mais... quand je pense à mon laser de labo...",
"de": "Mein erster Impuls wäre, ja zu sagen. Aber... wenn ich an meinen Laborlaser denke...",
"en": "My first reflex would be to say yes. But... when I think about my lab laser...",
"zh": "我的第一反应会是‘是’。但是……当我想起我实验室的激光时……",
"ja": "直感的には「はい」と言いたいところだけど…でも、研究室のレーザーを考えると…",
"es": "Mi primer instinto sería decir que sí. Pero... cuando pienso en mi láser de laboratorio..."
},{
"speaker": "Camille",
"fr": "Oui...",
"de": "Ja...",
"en": "Yes...",
"zh": "是的……",
"ja": "うん…",
"es": "Sí..."
},{
"speaker": "Luc",
"fr": "Je peux facilement augmenter sa puissance, donc l'amplitude, tout en gardant un faisceau super fin.",
"de": "Ich kann seine Leistung, also die Amplitude, leicht erhöhen, während ich einen extrem dünnen Strahl beibehalte.",
"en": "I can easily increase its power, so the amplitude, while maintaining an extremely thin beam.",
"zh": "我可以很容易地增加它的功率，也就是振幅，同时保持光束非常细。",
"ja": "ビームを極細に保ったまま、パワー、つまり振幅だけを簡単に上げることができる。",
"es": "Puedo aumentar fácilmente su potencia, por lo tanto la amplitud, manteniendo un haz súper fino."
},{
"speaker": "Camille",
"fr": "D'accord.",
"de": "Okay.",
"en": "Okay.",
"zh": "好的。",
"ja": "なるほど。",
"es": "De acuerdo."
},{
"speaker": "Luc",
"fr": "Donc non. En fait, non, ces deux paramètres, amplitude et largeur, semblent indépendants.",
"de": "Also nein. Tatsächlich scheinen diese beiden Parameter, Amplitude und Breite, unabhängig zu sein.",
"en": "So no. In fact, no, these two parameters, amplitude and width, seem independent.",
"zh": "所以，不。事实上，振幅和宽度这两个参数似乎是独立的。",
"ja": "ということは、違う。実際、振幅と幅というこの2つのパラメータは、独立しているように思える。",
"es": "Entonces no. De hecho, no, estos dos parámetros, amplitud y anchura, parecen independientes."
},{
"speaker": "Camille",
"fr": "Vous avez parfaitement raison. Ce sont deux paramètres indépendants.",
"de": "Sie haben vollkommen recht. Das sind zwei unabhängige Parameter.",
"en": "You are absolutely right. These are two independent parameters.",
"zh": "你完全正确。这是两个独立的参数。",
"ja": "まったくその通り。その2つは独立したパラメータよ。",
"es": "Tienes toda la razón. Son dos parámetros independientes."
},{
"speaker": "Luc",
"fr": "Hmm.",
"de": "Hm.",
"en": "Hmm.",
"zh": "嗯。",
"ja": "ふむ。",
"es": "Hmm."
},{
"speaker": "Camille",
"fr": "Mais que se passe-t-il si on pousse la logique jusqu'au bout, et qu'on essaie de rendre la largeur... infiniment petite ?",
"de": "Aber was passiert, wenn wir die Logik auf die Spitze treiben und versuchen, die Breite... unendlich klein zu machen?",
"en": "But what if we take the logic to the extreme, and try to make the width... infinitely small?",
"zh": "但是，如果我们把这个逻辑推向极致，试图让宽度……变得无限小呢？",
"ja": "でも、この考えを突き詰めて、幅を…無限に小さくしようとしたらどうなるかしら？",
"es": "Pero, ¿qué pasa si llevamos la lógica hasta el final y tratamos de hacer que la anchura sea... infinitamente pequeña?"
},{
"speaker": "Luc",
"fr": "Oui ?",
"de": "Ja?",
"en": "Yes?",
"zh": "然后呢？",
"ja": "というと？",
"es": "Sí?"
},{
"speaker": "Camille",
"fr": "De concentrer toute l'onde en un seul, unique point ?",
"de": "Die gesamte Welle auf einen einzigen Punkt zu konzentrieren?",
"en": "Of concentrating the entire wave into a single, unique point?",
"zh": "将整个波集中在一个单点上？",
"ja": "波全体を、たった一つの点に集中させるの？",
"es": "De concentrar toda la onda en un único, único punto?"
},{
"speaker": "Luc",
"fr": "Ah, là, la nature nous dit stop. C'est le fameux principe d'incertitude de Heisenberg.",
"de": "Ah, da sagt die Natur Halt. Das ist das berühmte Heisenbergsche Unschärfeprinzip.",
"en": "Ah, there, nature says stop. It's the famous Heisenberg uncertainty principle.",
"zh": "啊，到了这里，自然规律就行不通了。这就是著名的海森堡不确定性原理。",
"ja": "ああ、そこで自然が「ストップ」をかける。かの有名なハイゼンベルクの不確定性原理だ。",
"es": "Ah, ahí, la naturaleza nos dice basta. Es el famoso principio de incertidumbre de Heisenberg."
},{
"speaker": "Camille",
"fr": "Exactement.",
"de": "Genau.",
"en": "Exactly.",
"zh": "正是。",
"ja": "その通り。",
"es": "Exactamente."
},{
"speaker": "Luc",
"fr": "En voulant localiser une onde avec une précision extrême, donc une petite largeur delta x, on perd toute information sur son impulsion. On a un grand delta p.",
"de": "Wenn man versucht, eine Welle mit extremer Präzision zu lokalisieren, also mit einer kleinen Ortsunschärfe Delta-x, verliert man alle Informationen über ihren Impuls. Man hat dann eine große Impulsunschärfe Delta-p.",
"en": "When trying to localize a wave with extreme precision, i.e., a small width delta x, we lose all information about its direction. We have a large delta p.",
"zh": "当我们试图以极高的精度定位一个波（即一个很小的宽度Δx），我们就会失去所有关于它方向的信息。我们得到一个很大的动量不确定性Δp。",
"ja": "波の位置を極めて正確に、つまり幅（Δx）を小さく特定しようとすると、その運動量（Δp）に関する情報が全く分からなくなってしまうんだ。",
"es": "Al intentar localizar una onda con extrema precisión, por lo tanto, una pequeña anchura delta x, perdemos toda la información sobre su impulso. Tenemos un gran delta p."
},{
"speaker": "Camille",
"fr": "Oui.",
"de": "Ja.",
"en": "Yes.",
"zh": "是的。",
"ja": "ええ。",
"es": "Sí."
},{
"speaker": "Luc",
"fr": "Concrètement, un faisceau ultra-fin diverge énormément, juste après son point de focalisation.",
"de": "Konkret bedeutet das, dass ein ultradünner Strahl direkt nach seinem Fokuspunkt enorm divergiert.",
"en": "Concretely, an ultra-thin beam diverges enormously, right after its focal point.",
"zh": "具体来说，一束超细的光束在焦点之后会迅速发散。",
"ja": "具体的には、極細のビームは焦点の直後で、ものすごく広がってしまう。",
"es": "Concretamente, un haz ultra-fino diverge enormemente, justo después de su punto de focalización."
},{
"speaker": "Camille",
"fr": "Et ce phénomène de divergence, en optique, il porte un nom que tout le monde connaît.",
"de": "Und dieses Phänomen der Divergenz hat in der Optik einen Namen, den jeder kennt.",
"en": "And this phenomenon of divergence, in optics, it has a name that everyone knows.",
"zh": "在光学中，这种发散现象有一个众所周知的名字。",
"ja": "そして光学の分野では、この発散という現象に、誰もが知っている名前がついているのよ。",
"es": "Y este fenómeno de divergencia, en óptica, tiene un nombre que todo el mundo conoce."
},{
"speaker": "Luc",
"fr": "Oui...",
"de": "Ja...",
"en": "Yes...",
"zh": "是的……",
"ja": "うん…",
"es": "Sí..."
},{
"speaker": "Camille",
"fr": "La diffraction. C'est la diffraction qui impose une limite fondamentale à la résolution de nos microscopes.",
"de": "Die Beugung. Es ist die Beugung, die der Auflösung unserer Mikroskope eine fundamentale Grenze setzt.",
"en": "Diffraction. It's diffraction that imposes a fundamental limit on the resolution of our microscopes.",
"zh": "衍射。正是衍射，给我们的显微镜分辨率带来了根本性的限制。",
"ja": "回折よ。顕微鏡の分解能に根本的な限界を与えているのは、この回折という現象なの。",
"es": "La difracción. Es la difracción la que impone un límite fundamental a la resolución de nuestros microscopios."
},{
"speaker": "Luc",
"fr": "La fameuse limite d'Abbe !",
"de": "Die berühmte Abbe-Grenze!",
"en": "The famous Abbe limit!",
"zh": "著名的阿贝极限！",
"ja": "あの有名なアッベの限界だね！",
"es": "¡El famoso límite de Abbe!"
},{
"speaker": "Camille",
"fr": "Voilà !",
"de": "Genau!",
"en": "Exactly!",
"zh": "没错！",
"ja": "その通り！",
"es": "¡Voilà!"
},{
"speaker": "Luc",
"fr": "On nous apprend qu'avec de la lumière de longueur d'onde lambda, il est impossible de voir des détails plus petits que... en gros, la moitié de cette longueur d'onde, lambda sur deux.",
"de": "Man lernt, dass es mit Licht der Wellenlänge Lambda unmöglich ist, Details zu sehen, die kleiner sind als... grob gesagt, die Hälfte dieser Wellenlänge, Lambda geteilt durch zwei.",
"en": "We are taught that with light of wavelength lambda, it is impossible to see details smaller than... roughly half of that wavelength, lambda over two.",
"zh": "我们学到的是，用波长为λ的光，不可能看到比大约其波长一半(λ/2)还小的细节。",
"ja": "波長ラムダの光では、その波長の約半分、2分のラムダより小さいものは見ることができない、と習うよね。",
"es": "Nos enseñan que con luz de longitud de onda lambda, es imposible ver detalles más pequeños que... más o menos, la mitad de esta longitud de onda, lambda sobre dos."
},{
"speaker": "Camille",
"fr": "Hmm hmm.",
"de": "Mhm mhm.",
"en": "Hmm hmm.",
"zh": "嗯嗯。",
"ja": "ええ、そうね。",
"es": "Hmm hmm."
},{
"speaker": "Luc",
"fr": "Mais... mais attention à ce que ça veut dire vraiment...",
"de": "Aber... Vorsicht, was das wirklich bedeutet...",
"en": "But... but be careful about what that really means...",
"zh": "但是……要小心它真正的含义……",
"ja": "でも…それが本当は何を意味しているのか、注意が必要だ…",
"es": "Pero... pero presta atención a lo que realmente significa..."
},{
"speaker": "Camille",
"fr": "Allez-y, expliquez-nous cette nuance, elle est capitale.",
"de": "Erklären Sie uns diese Nuance, sie ist entscheidend.",
"en": "Go on, explain that nuance to us, it's crucial.",
"zh": "继续，给我们解释一下其中的细微差别，这至关重要。",
"ja": "ええ、お願い。そのニュアンスを説明してくれる？とても重要なことよ。",
"es": "A ver, explícanos este matiz, es capital."
},{
"speaker": "Luc",
"fr": "Cette limite, ça ne veut pas dire qu'on ne peut pas créer un spot lumineux plus petit que lambda sur deux.",
"de": "Diese Grenze bedeutet nicht, dass wir keinen Lichtfleck erzeugen können, der kleiner als Lambda geteilt durch zwei ist.",
"en": "This limit doesn't mean that we can't create a light spot smaller than lambda over two.",
"zh": "这个极限并不意味着我们不能创造出比λ/2更小的光斑。",
"ja": "この限界は、2分のラムダより小さい光のスポットを作れない、という意味じゃないんだ。",
"es": "Este límite no significa que no podamos crear un punto luminoso más pequeño que lambda sobre dos."
},{
"speaker": "Camille",
"fr": "Ah !",
"de": "Ah!",
"en": "Ah!",
"zh": "啊！",
"ja": "あら！",
"es": "¡Ah!"
},{
"speaker": "Luc",
"fr": "Ça veut dire que l'information sur les détails plus fins est transportée par des ondes très spéciales, « les ondes évanescentes ».",
"de": "Es bedeutet, dass die Information über feinere Details von ganz besonderen Wellen getragen wird, den \"evaneszenten Wellen\".",
"en": "That means that information about finer details is transported by very special waves, 'the evanescent waves'.",
"zh": "这意味着，关于更精细细节的信息是由一种非常特殊的波——‘倏逝波’——来传输的。",
"ja": "もっと細かい部分の情報は、「エバネッセント波」っていう特殊な波が運んでいる、ということなんだ。",
"es": "Significa que la información sobre los detalles más finos se transporta mediante ondas muy especiales, las \"ondas evanescentes\"."
},{
"speaker": "Camille",
"fr": "D'accord.",
"de": "Okay.",
"en": "Okay.",
"zh": "好的。",
"ja": "なるほど。",
"es": "De acuerdo."
},{
"speaker": "Luc",
"fr": "Et ces ondes, elles ne se propagent pas, elles s'atténuent si vite qu'elles n'atteignent jamais la lentille du microscope. L'information est là, mais... inaccessible. À moins d'être malin.",
"de": "Und diese Wellen breiten sich nicht aus, sie werden so schnell gedämpft, dass sie niemals die Linse des Mikroskops erreichen. Die Information ist da, aber... unzugänglich. Es sei denn, man ist clever.",
"en": "And these waves, they don't propagate, they attenuate so quickly that they never reach the microscope lens. The information is there, but... inaccessible. Unless you're clever.",
"zh": "而这些波不传播，它们衰减得非常快，以至于永远到不了显微镜的透镜。信息就在那里，但是……无法获取。除非使用巧妙的方法。",
"ja": "そして、この波は伝播せず、あまりに速く減衰してしまうので、顕微鏡のレンズまで届かないんだ。情報はそこにあるのに…アクセスできない。よほど上手くやらない限りはね。",
"es": "Y estas ondas, no se propagan, se atenúan tan rápido que nunca alcanzan la lente del microscopio. La información está ahí, pero… inaccesible. A menos que seas astuto."
},{
"speaker": "Camille",
"fr": "Et c'est là qu'intervient l'ingéniosité des physiciens !",
"de": "Und genau hier kommt die Genialität der Physiker ins Spiel!",
"en": "And that's where the ingenuity of physicists comes in!",
"zh": "而这正是物理学家们施展才智的地方！",
"ja": "そこに物理学者の創意工夫が光るわけね！",
"es": "¡Y ahí es donde entra en juego el ingenio de los físicos!"
},{
"speaker": "Luc",
"fr": "Oui !",
"de": "Ja!",
"en": "Yes!",
"zh": "是的！",
"ja": "そう！",
"es": "¡Sí!"
},{
"speaker": "Camille",
"fr": "Avec des techniques comme le microscope à champ proche, le NSOM, où on vient carrément détecter le champ avec une pointe ultra-fine, directement sur l'objet.",
"de": "Mit Techniken wie dem Nahfeldmikroskop, dem NSOM, bei dem man das Feld mit einer ultrafeinen Spitze direkt am Objekt misst.",
"en": "With techniques like the near-field microscope, the NSOM, where we directly detect the field with an ultra-fine tip, directly on the object.",
"zh": "使用像近场扫描光学显微镜（NSOM）这样的技术，我们用一个超细的探针直接在物体上检测场。",
"ja": "近接場顕微鏡（NSOM）のような技術を使って、超極細の探針で、対象のすぐそばの場を直接検出するの。",
"es": "Con técnicas como el microscopio de campo cercano, el NSOM, donde se detecta directamente el campo con una punta ultrafina, directamente sobre el objeto."
},{
"speaker": "Luc",
"fr": "Exactement ! On ne viole aucune loi, on va juste chercher l'info là où elle se trouve, avant qu'elle disparaisse.",
"de": "Genau! Wir verletzen keine Gesetze, wir holen uns die Information einfach dort, wo sie ist, bevor sie verschwindet.",
"en": "Exactly! We're not violating any laws, we're just looking for the information where it exists, before it disappears.",
"zh": "完全正确！我们没有违反任何定律，我们只是在信息消失前，在它存在的地方寻找信息。",
"ja": "その通り！法則を破るんじゃなくて、情報が消える前に、その場所まで迎えに行くだけさ。",
"es": "¡Exactamente! No violamos ninguna ley, simplemente vamos a buscar la información donde está, antes de que desaparezca."
},{
"speaker": "Camille",
"fr": "C'est ça.",
"de": "Richtig.",
"en": "That's it.",
"zh": "就是这样。",
"ja": "そういうことね。",
"es": "Eso es."
},{
"speaker": "Luc",
"fr": "La super-résolution, ce n'est pas de la magie. C'est juste une compréhension profonde de la nature des ondes.",
"de": "Superauflösung ist keine Magie. Es ist nur ein tiefes Verständnis der Natur von Wellen.",
"en": "Super-resolution isn't magic. It's just a deep understanding of the nature of waves.",
"zh": "超分辨率不是魔法，而是对波的本质的深刻理解。",
"ja": "超解像は魔法じゃない。波の性質を深く理解した結果なんだ。",
"es": "La superresolución no es magia. Es simplemente una comprensión profunda de la naturaleza de las ondas."
},{
"speaker": "Camille",
"fr": "Donc, pour résumer notre petit voyage : la fonction d'onde quantique, ce n'est pas une vague réelle, mais une onde de probabilité.",
"de": "Um unsere kleine Reise zusammenzufassen: Die Quantenwellenfunktion ist keine reale Welle, sondern eine Wahrscheinlichkeitswelle.",
"en": "So, to summarize our little journey: the quantum wave function isn't a real wave, but a probability wave.",
"zh": "所以，简单总结一下：量子波函数不是真实的波，而是概率波。",
"ja": "というわけで、今回の小さな旅をまとめると、量子的な波動関数は、現実の波ではなく、確率の波だということ。",
"es": "Así que, para resumir nuestro pequeño viaje: la función de onda cuántica no es una onda real, sino una onda de probabilidad."
},{
"speaker": "Luc",
"fr": "Oui.",
"de": "Ja.",
"en": "Yes.",
"zh": "是的。",
"ja": "うん。",
"es": "Sí."
},{
"speaker": "Camille",
"fr": "La probabilité est donnée par son amplitude au carré... un écho parfait de la loi sur l'énergie des ondes classiques.",
"de": "Die Wahrscheinlichkeit ist durch das Quadrat ihrer Amplitude gegeben... ein perfekter Widerhall des Energiegesetzes klassischer Wellen.",
"en": "Probability is given by its square amplitude... a perfect echo of the law on the energy of classical waves.",
"zh": "概率由其振幅的平方给出……这与经典波的能量定律完美呼应。",
"ja": "確率は振幅の2乗で与えられ…これは古典的な波のエネルギーに関する法則を、完璧に反映している。",
"es": "La probabilidad se da por su amplitud al cuadrado... un eco perfecto de la ley sobre la energía de las ondas clásicas."
},{
"speaker": "Luc",
"fr": "Incroyable.",
"de": "Unglaublich.",
"en": "Incredible.",
"zh": "不可思议。",
"ja": "すごいな。",
"es": "Increíble."
},{
"speaker": "Camille",
"fr": "Amplitude et largeur, c'est indépendant, mais la largeur est liée à la résolution par le principe d'incertitude, qui se manifeste par la diffraction.",
"de": "Amplitude und Breite sind unabhängig, aber die Breite ist über das Unschärfeprinzip, das sich durch die Beugung manifestiert, mit der Auflösung verknüpft.",
"en": "Amplitude and width are independent, but width is linked to resolution by the uncertainty principle, which manifests through diffraction.",
"zh": "振幅和宽度是独立的，但宽度通过不确定性原理与分辨率相关联，这体现在衍射上。",
"ja": "振幅と幅は独立しているけれど、幅は不確定性原理によって解像度と結びついていて、それが回折という形で現れるの。",
"es": "Amplitud y anchura son independientes, pero la anchura está relacionada con la resolución por el principio de incertidumbre, que se manifiesta por la difracción."
},{
"speaker": "Luc",
"fr": "Hmm hmm.",
"de": "Hm hm.",
"en": "Hmm hmm.",
"zh": "嗯嗯。",
"ja": "ふむふむ。",
"es": "Hmm hmm."
},{
"speaker": "Camille",
"fr": "Et cette limite de résolution, on peut la contourner par des techniques astucieuses.",
"de": "Und diese Auflösungsgrenze kann durch clevere Techniken umgangen werden.",
"en": "And this resolution limit can be circumvented by clever techniques.",
"zh": "而这个分辨率极限是可以通过巧妙的技术绕过的。",
"ja": "そして、この解像度の限界も、賢い技術で乗り越えることができる。",
"es": "Y este límite de resolución, podemos sortearlo con técnicas ingeniosas."
},{
"speaker": "Luc",
"fr": "C'est fascinant de voir comment tous ces concepts, de la nature de la réalité quantique jusqu'aux limites d'un microscope, sont tous tissés ensemble par les mêmes lois sur les ondes.",
"de": "Es ist faszinierend zu sehen, wie all diese Konzepte, von der Natur der Quantenrealität bis zu den Grenzen eines Mikroskops, durch dieselben Wellengesetze miteinander verwoben sind.",
"en": "It's fascinating to see how all these concepts, from the nature of quantum reality to the limits of a microscope, are all woven together by the same laws of waves.",
"zh": "看到所有这些概念，从量子现实的本质到显微镜的极限，都是由相同的波的定律编织在一起，这真是太迷人了。",
"ja": "量子という現実の性質から、顕微鏡の限界に至るまで、これらすべての概念が、同じ波の法則によって一つに織りなされているのを見るのは、本当に興味深いね。",
"es": "Es fascinante ver cómo todos estos conceptos, desde la naturaleza de la realidad cuántica hasta los límites de un microscopio, están todos entrelazados por las mismas leyes ondulatorias."
},{
"speaker": "Camille",
"fr": "Hmm.",
"de": "Hm.",
"en": "Hmm.",
"zh": "嗯。",
"ja": "ええ。",
"es": "Hmm."
},{
"speaker": "Luc",
"fr": "Le monde est vraiment... cohérent.",
"de": "Die Welt ist wirklich... kohärent.",
"en": "The world is really... coherent.",
"zh": "世界真的是……融贯的。",
"ja": "この世界は本当に…うまくできている。",
"es": "El mundo es realmente... coherente."
},{
"speaker": "Camille",
"fr": "Absolument. Et ça nous laisse avec une dernière question. Une question pour vous qui nous écoutez.",
"de": "Absolut. Und das lässt uns mit einer letzten Frage zurück. Eine Frage an Sie, die Sie uns zuhören.",
"en": "Absolutely. And that leaves us with a final question. A question for you who are listening to us.",
"zh": "当然。这就给我们留下了最后一个问题。一个留给正在收听的你们的问题。",
"ja": "本当にそうね。そして、最後に一つ質問が残るわ。聴いている皆さんへの質問よ。",
"es": "Absolutamente. Y eso nos deja con una última pregunta. Una pregunta para ustedes que nos escuchan."
},{
"speaker": "Luc",
"fr": "Oh ?",
"de": "Oh?",
"en": "Oh?",
"zh": "哦？",
"ja": "お？",
"es": "¿Oh?"
},{
"speaker": "Camille",
"fr": "Si la « probabilité de présence » en quantique et « l'énergie » en classique suivent toutes les deux la même règle de l'amplitude au carré…",
"de": "Wenn die \"Anwesenheitswahrscheinlichkeit\" in der Quantenmechanik und die \"Energie\" in der klassischen Mechanik beide derselben Regel des Amplitudenquadrats folgen…",
"en": "If the 'probability of presence' in quantum mechanics and 'the energy' in classical mechanics both follow the same rule of the square of the amplitude…",
"zh": "如果量子力学中的‘存在概率’和经典力学中的‘能量’都遵循振幅平方这同一个规则……",
"ja": "量子力学の「存在確率」と、古典力学の「エネルギー」が、どちらも振幅の2乗という同じ法則に従うのなら…",
"es": "Si la \"probabilidad de presencia\" en la cuántica y la \"energía\" en la clásica siguen ambas la misma regla de la amplitud al cuadrado…"
},{
"speaker": "Luc",
"fr": "…est-ce que ça signifie que la probabilité n'est pas qu'un simple outil de calcul ?",
"de": "…bedeutet das, dass die Wahrscheinlichkeit nicht nur ein einfaches Rechenwerkzeug ist?",
"en": "…does that mean that probability is not just a simple calculating tool?",
"zh": "……这是否意味着概率不仅仅是一个简单的计算工具？",
"ja": "…それは、確率が単なる計算の道具ではない、ということなのだろうか？",
"es": "¿…significa eso que la probabilidad no es solo una simple herramienta de cálculo?"
},{
"speaker": "Camille",
"fr": "Oui...",
"de": "Ja...",
"en": "Yes...",
"zh": "是的……",
"ja": "そう…",
"es": "Sí..."
},{
"speaker": "Luc",
"fr": "Se pourrait-il que la probabilité soit, d'une certaine manière, une quantité physique aussi réelle... aussi fondamentale que l'énergie elle-même ?",
"de": "Könnte es sein, dass die Wahrscheinlichkeit in gewisser Weise eine ebenso reale... ebenso fundamentale physikalische Größe ist wie die Energie selbst?",
"en": "Could it be that probability is, in a certain way, a physical quantity as real... as fundamental as energy itself?",
"zh": "有没有可能，概率在某种程度上是一种物理量，像能量本身一样……真实……一样基本？",
"ja": "もしかしたら確率って、ある意味、エネルギーそのものと同じくらいリアルで…根本的な物理量だったりするんだろうか？",
"es": "¿Podría ser que la probabilidad sea, de alguna manera, una cantidad física tan real... tan fundamental como la energía misma?"
},{
"speaker": "Camille",
"fr": "C'est une pensée vertigineuse. Qu'en pensez-vous ?",
"de": "Ein schwindelerregender Gedanke. Was denken Sie?",
"en": "It's a dizzying thought. What do you think?",
"zh": "这是一个令人眩晕的想法。您怎么看？",
"ja": "気が遠くなるような話ね。皆さんはどう思いますか？",
"es": "Es un pensamiento vertiginoso. ¿Qué opina usted?"
},{
"speaker": "Luc",
"fr": "Hmm.",
"de": "Hm.",
"en": "Hmm.",
"zh": "嗯。",
"ja": "ふむ。",
"es": "Hmm."
},{
"speaker": "Camille",
"fr": "Merci de nous avoir écoutés, et à bientôt sur « Passerelles en Physique ».",
"de": "Danke, dass Sie uns zugehört haben, und bis bald bei \"Brücken in die Physik\".",
"en": "Thank you for listening to us, and see you soon on \"Bridges in Physics\".",
"zh": "感谢您的收听，我们《物理之桥》再见。",
"ja": "ご清聴ありがとうございました。また「物理の架け橋」でお会いしましょう。",
"es": "Gracias por escucharnos, y hasta pronto en \"Puentes en Física\"."
}]
);
