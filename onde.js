// Initialize datasets array if undefined
if (typeof datasets === 'undefined') {
    var datasets = [];
}

// Add dataset to datasets array
datasets.push(
[{
"speaker": "Camille",
"fr": "Bonjour à toutes et à tous, et bienvenue dans « Passerelles en Physique ». Le podcast où, eh bien, on jette un pont entre les mystères du monde quantique et la physique de notre quotidien.",
"en": "Hello everyone, and welcome to \"Bridges in Physics\". The podcast where, well, we build a bridge between the mysteries of the quantum world and the physics of our everyday lives.",
"ja": "皆さん、こんにちは。「物理の架け橋」へようこそ。量子世界の神秘と、私たちの日常生活に潜む物理学の間に橋を架けるポッドキャストです。"
},{
"speaker": "Luc",
"fr": "C'est exactement ça ! Bonjour tout le monde.",
"en": "That's exactly right! Hello everyone.",
"ja": "その通りだね！皆さん、こんにちは。"
},{
"speaker": "Camille",
"fr": "Je suis Camille, physicienne théoricienne.",
"en": "I'm Camille, a theoretical physicist.",
"ja": "私はカミーユ、理論物理学者です。"
},{
"speaker": "Luc",
"fr": "Et je suis Luc, physicien expérimentateur. Camille, pour commencer, j'aimerais qu'on plonge directement dans une image que... que tout le monde connaît, en fait.",
"en": "And I'm Luc, an experimental physicist. Camille, to start, I'd like to dive right into an image that... that everyone knows, in fact.",
"ja": "そして僕はリュック、実験物理学者だ。カミーユ、まず、誰もが知っているイメージから話を始めたいんだ。"
},{
"speaker": "Camille",
"fr": "Oui ?",
"en": "Yes?",
"ja": "なあに？"
},{
"speaker": "Luc",
"fr": "On nous dit tout le temps que les particules, comme les électrons, se comportent comme des ondes. Mais... est-ce que ça veut dire qu'il y a une véritable petite vague matérielle qui ondule dans l'espace ? Un peu comme une ride à la surface de l'eau ?",
"en": "We're constantly told that particles, like electrons, behave like waves. But... does that mean there's a real little material wave that undulates in space? A bit like a ripple on the surface of water?",
"ja": "電子のような粒子は波のように振る舞うと、よく言われるよね。でも…それって、空間を実際にうねって進む、物質の小さな波が本当にあるっていうことなのかな？水面に広がる波紋みたいにさ。"
},{
"speaker": "Camille",
"fr": "C'est une question absolument fondamentale, Luc, parce que ça touche à notre intuition la plus profonde.",
"en": "It's an absolutely fundamental question, Luc, because it touches on our deepest intuition.",
"ja": "それはとても根源的な問いね、リュック。だって、私たちの最も深い直感に触れる問題だから。"
},{
"speaker": "Luc",
"fr": "Oui.",
"en": "Yes.",
"ja": "うん。"
},{
"speaker": "Camille",
"fr": "Et la réponse, qui a mis un siècle à s'imposer, est à la fois simple et… déroutante : non. Non, cette onde, que les physiciens nomment la fonction d'onde, psi... n'est pas une onde de matière.",
"en": "And the answer, which took a century to become established, is both simple and... perplexing: no. No, this wave, which physicists call the wave function, psi... is not a wave of matter.",
"ja": "そして、定着するのに1世紀もかかったその答えは、単純でありながら…人を惑わせるものでもあるの。答えは「ノー」。物理学者が波動関数、プサイと呼ぶこの波は、物質の波ではないのよ。"
},{
"speaker": "Luc",
"fr": "D'accord...",
"en": "I see...",
"ja": "なるほど…"
},{
"speaker": "Camille",
"fr": "C'est une onde de… possibilités.",
"en": "It's a wave of... possibilities.",
"ja": "それは…可能性の波。"
},{
"speaker": "Luc",
"fr": "Une onde de possibilités… Vous voulez dire qu'elle ne décrit pas un objet réel, mais plutôt la... la probabilité de trouver l'objet quelque part ?",
"en": "A wave of possibilities... Do you mean it doesn't describe a real object, but rather the... the probability of finding the object somewhere?",
"ja": "可能性の波…つまり、それは実在する物体を記述しているんじゃなくて、その物体がどこかで見つかる…確率を表しているということかい？"
},{
"speaker": "Camille",
"fr": "Exactement. Et pour être tout à fait précis, ce n'est pas l'onde elle-même qui est la probabilité.",
"en": "Exactly. And to be perfectly precise, it's not the wave itself that is the probability.",
"ja": "その通り。でも正確に言うと、確率そのものが波というわけではないの。"
},{
"speaker": "Luc",
"fr": "D'accord.",
"en": "Okay.",
"ja": "わかった。"
},{
"speaker": "Camille",
"fr": "C'est le carré de son amplitude. Ou de sa « hauteur », si vous préférez.",
"en": "It's the square of its amplitude. Or its \"height\", if you prefer.",
"ja": "その振幅の2乗よ。あるいは、分かりやすく言えばその「高さ」の2乗ね。"
},{
"speaker": "Luc",
"fr": "Ah oui.",
"en": "Ah yes.",
"ja": "ああ、なるほど。"
},{
"speaker": "Camille",
"fr": "On note ça psi au carré. C'est la fameuse règle de Born, un des piliers de la mécanique quantique.",
"en": "We denote that as psi squared. That's the famous Born rule, one of the pillars of quantum mechanics.",
"ja": "それをプサイの2乗と書くの。これが有名なボルンの規則で、量子力学の根幹を成す考え方の一つよ。"
},{
"speaker": "Luc",
"fr": "Ah, ça, c'est un phénomène que je vois tous les jours au labo !",
"en": "Ah, that's a phenomenon I see every day in the lab!",
"ja": "ああ、それは僕がラボで毎日目にしている現象だよ！"
},{
"speaker": "Camille",
"fr": "Ah oui ?",
"en": "Ah yes?",
"ja": "あら、そうなの？"
},{
"speaker": "Luc",
"fr": "Quand on fait l'expérience des fentes de Young en envoyant des électrons un par un, chaque électron laisse un seul impact sur l'écran, comme une particule.",
"en": "When we perform the double-slit experiment by sending electrons one by one, each electron leaves a single impact on the screen, like a particle.",
"ja": "ヤングの二重スリット実験で電子を一つずつ撃つと、個々の電子は粒子みたいに、スクリーンに一つの点としてぶつかる。"
},{
"speaker": "Camille",
"fr": "Oui...",
"en": "Yes...",
"ja": "ええ…"
},{
"speaker": "Luc",
"fr": "Mais... après en avoir envoyé des milliers, on voit se dessiner cette figure avec des franges... une figure d'interférence.",
"en": "But... after sending thousands of them, you see this pattern emerge with fringes... an interference pattern.",
"ja": "でも…何千個も撃った後には、縞模様が…干渉縞が現れるんだ。"
},{
"speaker": "Camille",
"fr": "Hmm.",
"en": "Hmm.",
"ja": "ふむ。"
},{
"speaker": "Luc",
"fr": "Et cette distribution, elle est magnifique, elle suit à la perfection la loi en psi au carré.",
"en": "And this distribution, it's magnificent, it perfectly follows the law of psi squared.",
"ja": "そして、この分布は見事なまでに、プサイの2乗 の法則にぴったり一致するんだ。"
},{
"speaker": "Camille",
"fr": "C'est la preuve expérimentale irréfutable. Mais ça nous amène à la question... pourquoi le carré ?",
"en": "That's the irrefutable experimental proof. But that brings us to the question... why the square?",
"ja": "これが反論のしようがない実験的な証拠ね。でも、ここから次の疑問が生まれる…なぜ2乗なのか？"
},{
"speaker": "Luc",
"fr": "Oui !",
"en": "Yes!",
"ja": "そうだ！"
},{
"speaker": "Camille",
"fr": "Pourquoi la nature a-t-elle choisi cette complexité ? Une probabilité directe, juste liée à psi, ça semblerait tellement plus simple, non ?",
"en": "Why did nature choose this complexity? A direct probability, just linked to psi, would seem so much simpler, wouldn't it?",
"ja": "なぜ自然はこんなに複雑な仕組みを選んだのかしら？単にプサイに比例する確率のほうが、ずっと単純でしょう？"
},{
"speaker": "Luc",
"fr": "Tout à fait ! Pourquoi cette étape en plus ?",
"en": "Exactly! Why this extra step?",
"ja": "まったくその通りだ！ なぜ、わざわざ一手間加える必要があるんだろう？"
},{
"speaker": "Camille",
"fr": "Alors, il y a une raison mathématique, euh... implacable : la conservation.",
"en": "So, there's a mathematical reason, uh... implacable: conservation.",
"ja": "それには、数学的な、ええと…動かしがたい理由があるの。それは「保存」よ。"
},{
"speaker": "Luc",
"fr": "D'accord.",
"en": "I understand.",
"ja": "なるほど。"
},{
"speaker": "Camille",
"fr": "La probabilité totale de trouver la particule quelque part dans l'univers, elle doit toujours être de 100%.",
"en": "The total probability of finding the particle somewhere in the universe must always be 100%.",
"ja": "宇宙のどこかである粒子を見つける確率の合計は、常に100%でなければならない。"
},{
"speaker": "Luc",
"fr": "Toujours.",
"en": "Always.",
"ja": "いつでも。"
},{
"speaker": "Camille",
"fr": "Elle ne peut pas apparaître ou disparaître. Et il se trouve que seule la forme psi au carré garantit que cette règle est respectée. Tout le temps.",
"en": "It cannot appear or disappear. And it happens that only the form psi squared guarantees that this rule is respected. All the time.",
"ja": "勝手に現れたり消えたりはできない。そして、プサイの2乗という形だけが、このルールが常に守られることを保証してくれるのよ。"
},{
"speaker": "Luc",
"fr": "D'accord.",
"en": "Okay.",
"ja": "なるほど。"
},{
"speaker": "Camille",
"fr": "Mais... il y a une raison encore plus belle. Une raison qui fait le lien avec votre domaine, Luc.",
"en": "But... there's an even more beautiful reason. A reason that connects to your field, Luc.",
"ja": "でも…もっと美しい理由もあるの。あなたの専門分野につながる理由がね、リュック。"
},{
"speaker": "Luc",
"fr": "Ah ? Laquelle ?",
"en": "Ah? Which one?",
"ja": "え？どんな？"
},{
"speaker": "Camille",
"fr": "En optique classique, l'énergie d'une onde lumineuse, ce qui fait sa brillance, est elle aussi proportionnelle au carré de l'amplitude. E au carré.",
"en": "In classical optics, the energy of a light wave, which gives it its brilliance, is also proportional to the square of the amplitude. E squared.",
"ja": "古典光学では、光波のエネルギー、つまりその明るさは、同じく振幅の2乗に比例するの。Eの2乗にね。"
},{
"speaker": "Luc",
"fr": "Wow.",
"en": "Wow.",
"ja": "へえ。"
},{
"speaker": "Camille",
"fr": "C'est un parallèle absolument stupéfiant.",
"en": "That's an absolutely stunning parallel.",
"ja": "これは本当に驚くべき類似点だわ。"
},{
"speaker": "Luc",
"fr": "Attends. Donc la « probabilité de présence » d'une particule quantique... se calcule de la même manière que « l'énergie » d'une onde lumineuse classique.",
"en": "Wait. So the 'probability of presence' of a quantum particle... is calculated in the same way as 'the energy' of a classical light wave.",
"ja": "待ってくれ。ということは、量子的な粒子の「存在確率」は…古典的な光の波の「エネルギー」と、まったく同じ方法で計算されるということかい？"
},{
"speaker": "Camille",
"fr": "Oui.",
"en": "Yes.",
"ja": "ええ。"
},{
"speaker": "Luc",
"fr": "C'est la même loi mathématique pour deux mondes si différents. Ce n'est pas une coïncidence.",
"en": "It's the same mathematical law for two such different worlds. It's not a coincidence.",
"ja": "こんなに違う2つの世界で、同じ数学法則が成り立っているなんて。これは偶然じゃないはずだ。"
},{
"speaker": "Camille",
"fr": "Non. C'est un des plus beaux exemples de l'unité de la physique. Et ça nous amène à une autre intuition à questionner.",
"en": "No. It's one of the most beautiful examples of the unity of physics. And that leads us to another intuition to question.",
"ja": "ええ。物理学の統一性を示す、最も美しい例の1つよ。そして、ここからまた別の直感に疑問を投げかけることになるわ。"
},{
"speaker": "Luc",
"fr": "Ah ?",
"en": "Ah?",
"ja": "ほう？"
},{
"speaker": "Camille",
"fr": "Parlons de l'amplitude et de la largeur spatiale d'une onde. Une onde très « haute » est-elle forcément très « large » ?",
"en": "Let's talk about the amplitude and spatial width of a wave. Is a very 'high' wave necessarily very 'wide'?",
"ja": "波の振幅と空間的な幅について話しましょうか。とても「高い」波は、必ずしも「広い」波なのかな？"
},{
"speaker": "Luc",
"fr": "Mon premier réflexe serait de dire oui. Mais... quand je pense à mon laser de labo...",
"en": "My first reflex would be to say yes. But... when I think about my lab laser...",
"ja": "直感的には「はい」と言いたいところだけど…でも、研究室のレーザーを考えると…"
},{
"speaker": "Camille",
"fr": "Oui...",
"en": "Yes...",
"ja": "うん…"
},{
"speaker": "Luc",
"fr": "Je peux facilement augmenter sa puissance, donc l'amplitude, tout en gardant un faisceau super fin.",
"en": "I can easily increase its power, so the amplitude, while maintaining an extremely thin beam.",
"ja": "ビームを極細に保ったまま、パワー、つまり振幅だけを簡単に上げることができる。"
},{
"speaker": "Camille",
"fr": "D'accord.",
"en": "Okay.",
"ja": "なるほど。"
},{
"speaker": "Luc",
"fr": "Donc non. En fait, non, ces deux paramètres, amplitude et largeur, semblent indépendants.",
"en": "So no. In fact, no, these two parameters, amplitude and width, seem independent.",
"ja": "ということは、違う。実際、振幅と幅というこの2つのパラメータは、独立しているように思える。"
},{
"speaker": "Camille",
"fr": "Vous avez parfaitement raison. Ce sont deux paramètres indépendants.",
"en": "You are absolutely right. These are two independent parameters.",
"ja": "まったくその通り。その2つは独立したパラメータよ。"
},{
"speaker": "Luc",
"fr": "Hmm.",
"en": "Hmm.",
"ja": "ふむ。"
},{
"speaker": "Camille",
"fr": "Mais que se passe-t-il si on pousse la logique jusqu'au bout, et qu'on essaie de rendre la largeur... infiniment petite ?",
"en": "But what if we take the logic to the extreme, and try to make the width... infinitely small?",
"ja": "でも、この考えを突き詰めて、幅を…無限に小さくしようとしたらどうなるかしら？"
},{
"speaker": "Luc",
"fr": "Oui ?",
"en": "Yes?",
"ja": "というと？"
},{
"speaker": "Camille",
"fr": "De concentrer toute l'onde en un seul, unique point ?",
"en": "Of concentrating the entire wave into a single, unique point?",
"ja": "波全体を、たった一つの点に集中させるの？"
},{
"speaker": "Luc",
"fr": "Ah, là, la nature nous dit stop. C'est le fameux principe d'incertitude de Heisenberg.",
"en": "Ah, there, nature says stop. It's the famous Heisenberg uncertainty principle.",
"ja": "ああ、そこで自然が「ストップ」をかける。かの有名なハイゼンベルクの不確定性原理だ。"
},{
"speaker": "Camille",
"fr": "Exactement.",
"en": "Exactly.",
"ja": "その通り。"
},{
"speaker": "Luc",
"fr": "En voulant localiser une onde avec une précision extrême, donc une petite largeur delta x, on perd toute information sur sa direction. On a un grand delta k.",
"en": "When trying to localize a wave with extreme precision, i.e., a small width delta x, we lose all information about its direction. We have a large delta k.",
"ja": "波の位置を極めて正確に、つまり幅（Δx）を小さく特定しようとすると、その運動量（Δk）に関する情報が全く分からなくなってしまうんだ。"
},{
"speaker": "Camille",
"fr": "Oui.",
"en": "Yes.",
"ja": "ええ。"
},{
"speaker": "Luc",
"fr": "Concrètement, un faisceau ultra-fin diverge énormément, juste après son point de focalisation.",
"en": "Concretely, an ultra-thin beam diverges enormously, right after its focal point.",
"ja": "具体的には、極細のビームは焦点の直後で、ものすごく広がってしまう。"
},{
"speaker": "Camille",
"fr": "Et ce phénomène de divergence, en optique, il porte un nom que tout le monde connaît.",
"en": "And this phenomenon of divergence, in optics, it has a name that everyone knows.",
"ja": "そして光学の分野では、この発散という現象に、誰もが知っている名前がついているのよ。"
},{
"speaker": "Luc",
"fr": "Oui...",
"en": "Yes...",
"ja": "うん…"
},{
"speaker": "Camille",
"fr": "La diffraction. C'est la diffraction qui impose une limite fondamentale à la résolution de nos microscopes.",
"en": "Diffraction. It's diffraction that imposes a fundamental limit on the resolution of our microscopes.",
"ja": "回折よ。顕微鏡の分解能に根本的な限界を与えているのは、この回折という現象なの。"
},{
"speaker": "Luc",
"fr": "La fameuse limite d'Abbe !",
"en": "The famous Abbe limit!",
"ja": "あの有名なアッベの限界だね！"
},{
"speaker": "Camille",
"fr": "Voilà !",
"en": "Voilà!",
"ja": "その通り！"
},{
"speaker": "Luc",
"fr": "On nous apprend qu'avec de la lumière de longueur d'onde lambda, il est impossible de voir des détails plus petits que... en gros, la moitié de cette longueur d'onde, lambda sur deux.",
"en": "We are taught that with light of wavelength lambda, it is impossible to see details smaller than... roughly half of that wavelength, lambda over two.",
"ja": "波長ラムダの光では、その波長の約半分、2分のラムダより小さいものは見ることができない、と習うよね。"
},{
"speaker": "Camille",
"fr": "Hmm hmm.",
"en": "Hmm hmm.",
"ja": "ええ、そうね。"
},{
"speaker": "Luc",
"fr": "Mais... mais attention à ce que ça veut dire vraiment...",
"en": "But... but be careful about what that really means...",
"ja": "でも…それが本当は何を意味しているのか、注意が必要だ…"
},{
"speaker": "Camille",
"fr": "Allez-y, expliquez-nous cette nuance, elle est capitale.",
"en": "Go on, explain that nuance to us, it's crucial.",
"ja": "ええ、お願い。そのニュアンスを説明してくれる？とても重要なことよ。"
},{
"speaker": "Luc",
"fr": "Cette limite, ça ne veut pas dire qu'on ne peut pas créer un spot lumineux plus petit que lambda sur deux.",
"en": "This limit doesn't mean that we can't create a light spot smaller than lambda over two.",
"ja": "この限界は、2分のラムダより小さい光のスポットを作れない、という意味じゃないんだ。"
},{
"speaker": "Camille",
"fr": "Ah !",
"en": "Ah!",
"ja": "あら！"
},{
"speaker": "Luc",
"fr": "Ça veut dire que l'information sur les détails plus fins est transportée par des ondes très spéciales, « les ondes évanescentes ».",
"en": "That means that information about finer details is transported by very special waves, 'the evanescent waves'.",
"ja": "もっと細かい部分の情報は、「エバネッセント波」っていう特殊な波が運んでいる、ということなんだ。"
},{
"speaker": "Camille",
"fr": "D'accord.",
"en": "Okay.",
"ja": "なるほど。"
},{
"speaker": "Luc",
"fr": "Et ces ondes, elles ne se propagent pas, elles s'atténuent si vite qu'elles n'atteignent jamais la lentille du microscope. L'information est là, mais... inaccessible. À moins d'être malin.",
"en": "And these waves, they don't propagate, they attenuate so quickly that they never reach the microscope lens. The information is there, but... inaccessible. Unless you're clever.",
"ja": "そして、この波は伝播せず、あまりに速く減衰してしまうので、顕微鏡のレンズまで届かないんだ。情報はそこにあるのに…アクセスできない。よほど上手くやらない限りはね。"
},{
"speaker": "Camille",
"fr": "Et c'est là qu'intervient l'ingéniosité des physiciens !",
"en": "And that's where the ingenuity of physicists comes in!",
"ja": "そこに物理学者の創意工夫が光るわけね！"
},{
"speaker": "Luc",
"fr": "Oui !",
"en": "Yes!",
"ja": "そう！"
},{
"speaker": "Camille",
"fr": "Avec des techniques comme le microscope à champ proche, le NSOM, où on vient carrément détecter le champ avec une pointe ultra-fine, directement sur l'objet.",
"en": "With techniques like the near-field microscope, the NSOM, where we directly detect the field with an ultra-fine tip, directly on the object.",
"ja": "近接場顕微鏡（NSOM）のような技術を使って、超極細の探針で、対象のすぐそばの場を直接検出するの。"
},{
"speaker": "Luc",
"fr": "Exactement ! On ne viole aucune loi, on va juste chercher l'info là où elle se trouve, avant qu'elle disparaisse.",
"en": "Exactly! We're not violating any laws, we're just looking for the information where it exists, before it disappears.",
"ja": "その通り！法則を破るんじゃなくて、情報が消える前に、その場所まで迎えに行くだけさ。"
},{
"speaker": "Camille",
"fr": "C'est ça.",
"en": "That's it.",
"ja": "そういうことね。"
},{
"speaker": "Luc",
"fr": "La super-résolution, ce n'est pas de la magie. C'est juste une compréhension profonde de la nature des ondes.",
"en": "Super-resolution isn't magic. It's just a deep understanding of the nature of waves.",
"ja": "超解像は魔法じゃない。波の性質を深く理解した結果なんだ。"
},{
"speaker": "Camille",
"fr": "Donc, pour résumer notre petit voyage : la fonction d'onde quantique, ce n'est pas une vague réelle, mais une onde de probabilité.",
"en": "So, to summarize our little journey: the quantum wave function isn't a real wave, but a probability wave.",
"ja": "というわけで、今回の小さな旅をまとめると、量子的な波動関数は、現実の波ではなく、確率の波だということ。"
},{
"speaker": "Luc",
"fr": "Oui.",
"en": "Yes.",
"ja": "うん。"
},{
"speaker": "Camille",
"fr": "La probabilité est donnée par son amplitude au carré... un écho parfait de la loi sur l'énergie des ondes classiques.",
"en": "Probability is given by its square amplitude... a perfect echo of the law on the energy of classical waves.",
"ja": "確率は振幅の2乗で与えられ…これは古典的な波のエネルギーに関する法則を、完璧に反映している。"
},{
"speaker": "Luc",
"fr": "Incroyable.",
"en": "Incredible.",
"ja": "すごいな。"
},{
"speaker": "Camille",
"fr": "Amplitude et largeur, c'est indépendant, mais la largeur est liée à la résolution par le principe d'incertitude, qui se manifeste par la diffraction.",
"en": "Amplitude and width are independent, but width is linked to resolution by the uncertainty principle, which manifests through diffraction.",
"ja": "振幅と幅は独立しているけれど、幅は不確定性原理によって解像度と結びついていて、それが回折という形で現れるの。"
},{
"speaker": "Luc",
"fr": "Hmm hmm.",
"en": "Hmm hmm.",
"ja": "ふむふむ。"
},{
"speaker": "Camille",
"fr": "Et cette limite de résolution, on peut la contourner par des techniques astucieuses.",
"en": "And this resolution limit can be circumvented by clever techniques.",
"ja": "そして、この解像度の限界も、賢い技術で乗り越えることができる。"
},{
"speaker": "Luc",
"fr": "C'est fascinant de voir comment tous ces concepts, de la nature de la réalité quantique jusqu'aux limites d'un microscope, sont tous tissés ensemble par les mêmes lois sur les ondes.",
"en": "It's fascinating to see how all these concepts, from the nature of quantum reality to the limits of a microscope, are all woven together by the same laws of waves.",
"ja": "量子という現実の性質から、顕微鏡の限界に至るまで、これらすべての概念が、同じ波の法則によって一つに織りなされているのを見るのは、本当に興味深いね。"
},{
"speaker": "Camille",
"fr": "Hmm.",
"en": "Hmm.",
"ja": "ええ。"
},{
"speaker": "Luc",
"fr": "Le monde est vraiment... cohérent.",
"en": "The world is really... coherent.",
"ja": "この世界は本当に…うまくできている。"
},{
"speaker": "Camille",
"fr": "Absolument. Et ça nous laisse avec une dernière question. Une question pour vous qui nous écoutez.",
"en": "Absolutely. And that leaves us with a final question. A question for you who are listening to us.",
"ja": "本当にそうね。そして、最後に一つ質問が残るわ。聴いている皆さんへの質問よ。"
},{
"speaker": "Luc",
"fr": "Oh ?",
"en": "Oh?",
"ja": "お？"
},{
"speaker": "Camille",
"fr": "Si la « probabilité de présence » en quantique et « l'énergie » en classique suivent toutes les deux la même règle de l'amplitude au carré…",
"en": "If the 'probability of presence' in quantum mechanics and 'the energy' in classical mechanics both follow the same rule of the square of the amplitude…",
"ja": "量子力学の「存在確率」と、古典力学の「エネルギー」が、どちらも振幅の2乗という同じ法則に従うのなら…"
},{
"speaker": "Luc",
"fr": "…est-ce que ça signifie que la probabilité n'est pas qu'un simple outil de calcul ?",
"en": "…does that mean that probability is not just a simple calculating tool?",
"ja": "…それは、確率が単なる計算の道具ではない、ということなのだろうか？"
},{
"speaker": "Camille",
"fr": "Oui...",
"en": "Yes...",
"ja": "そう…"
},{
"speaker": "Luc",
"fr": "Se pourrait-il que la probabilité soit, d'une certaine manière, une quantité physique aussi réelle... aussi fondamentale que l'énergie elle-même ?",
"en": "Could it be that probability is, in a certain way, a physical quantity as real... as fundamental as energy itself?",
"ja": "もしかしたら確率って、ある意味、エネルギーそのものと同じくらいリアルで…根本的な物理量だったりするんだろうか？"
},{
"speaker": "Camille",
"fr": "C'est une pensée vertigineuse. Qu'en pensez-vous ?",
"en": "It's a dizzying thought. What do you think?",
"ja": "気が遠くなるような話ね。皆さんはどう思いますか？"
},{
"speaker": "Luc",
"fr": "Hmm.",
"en": "Hmm.",
"ja": "ふむ。"
},{
"speaker": "Camille",
"fr": "Merci de nous avoir écoutés, et à bientôt sur « Passerelles en Physique ».",
"en": "Thank you for listening to us, and see you soon on \"Bridges in Physics\".",
"ja": "ご清聴ありがとうございました。また「物理の架け橋」でお会いしましょう。"
}]
);
