from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Cambia esto por una clave secreta para las sesiones

# Diccionario de versículos
versiculos = {
    "Amor ❤️": [
    "Cantares 8:7: 'Las aguas no pueden apagar el amor, ni los ríos lo ahogarían; si alguien diese todos los bienes de su casa por este amor, de cierto lo menospreciarían.'",
    "1 Corintios 13:4-7: 'El amor es paciente, es bondadoso. El amor no es envidioso ni jactancioso, ni orgulloso. No se porta con rudeza, no busca lo suyo, no se irrita, no guarda rencor. No se goza de la injusticia, sino que se goza de la verdad. Todo lo sufre, todo lo cree, todo lo espera, todo lo soporta.'",
    "Proverbios 3:3-4: 'Que no se aparten de ti la misericordia y la verdad; átalas a tu cuello, escríbelas en la tabla de tu corazón; y hallarás gracia y buena opinión ante los ojos de Dios y de los hombres.'",
    "Efesios 5:25: 'Maridos, amad a vuestras mujeres, así como Cristo amó a la iglesia y se entregó a sí mismo por ella.'",
    "Cantares 2:16: 'Mi amado es mío, y yo soy suya; él apacienta entre los lirios.'",
    "Colosenses 3:14: 'Y sobre todas estas cosas vestíos de amor, que es el vínculo perfecto.'",
    "1 Juan 4:7: 'Amados, amémonos unos a otros, porque el amor es de Dios; todo aquel que ama es nacido de Dios y conoce a Dios.'",
    "Proverbios 17:17: 'En todo tiempo ama el amigo, y el hermano nace para el tiempo de angustia.'",
    "1 Corintios 16:14: 'Que todo lo que hagáis sea hecho con amor.'",
    "Romanos 13:10: 'El amor no hace mal al prójimo; así que el amor es el cumplimiento de la ley.'",
    "1 Pedro 4:8: 'Sobre todo, tened entre vosotros ferviente amor, porque el amor cubrirá multitud de pecados.'",
    "Mateo 22:37-39: 'Jesús le dijo: Amarás al Señor tu Dios con todo tu corazón, con toda tu alma y con toda tu mente. Este es el primero y grande mandamiento. Y el segundo es semejante a este: Amarás a tu prójimo como a ti mismo.'",
    "1 Juan 4:18: 'En el amor no hay temor, sino que el perfecto amor echa fuera el temor. Porque el temor lleva en sí castigo, de donde el que teme no ha sido perfeccionado en el amor.'",
    "Efesios 4:2: 'Con toda humildad y mansedumbre, soportándoos con paciencia los unos a los otros en amor.'",
    "1 Juan 4:19: 'Nosotros le amamos a él, porque él nos amó primero.'",
    "Romanos 5:8: 'Pero Dios muestra su amor para con nosotros, en que siendo aún pecadores, Cristo murió por nosotros.'",
    "Proverbios 10:12: 'El odio despierta rencillas, pero el amor cubre todas las faltas.'",
    "1 Corintios 13:13: 'Y ahora permanecen la fe, la esperanza y el amor, estos tres; pero el mayor de ellos es el amor.'",
    "Cantares 4:9: 'Has cautivado mi corazón, hermana mía, esposa mía; has cautivado mi corazón con uno de tus ojos, con una cadena de tu cuello.'",
    "Juan 15:13: 'Nadie tiene mayor amor que este, que uno ponga su vida por sus amigos.'",
    "Lucas 6:32-33: 'Si amáis a los que os aman, ¿qué mérito tenéis? Porque también los pecadores aman a los que los aman. Y si hacéis bien a los que os hacen bien, ¿qué mérito tenéis? También los pecadores hacen lo mismo.'",
    "Salmo 136:1: 'Alabad a Jehová, porque él es bueno; porque para siempre es su misericordia.'",
    "Isaías 54:10: 'Porque los montes se apartarán, y los collados temblarán; pero mi misericordia no se apartará de ti, ni el pacto de mi paz temblará, dijo Jehová el que te ama.'",
    "1 Corintios 13:5: 'No hace nada indebido, no busca lo suyo, no se irrita, no guarda rencor.'",
    "1 Juan 4:12: 'Nadie ha visto jamás a Dios; si nos amamos unos a otros, Dios permanece en nosotros, y su amor se ha perfeccionado en nosotros.'",
    "Cantares 8:6: 'Ponme como un sello sobre tu corazón, como una marca sobre tu brazo; porque el amor es fuerte como la muerte, celos como el sepulcro; sus brasas, brasas de fuego, llama vehemente.'",
    "1 Corintios 13:4: 'El amor es paciente, el amor es bondadoso; no tiene envidia, el amor no es jactancioso, no se embanece.'",
    "Proverbios 31:10: 'Mujer virtuosa, ¿quién la hallará? Porque su estima sobrepasa largamente a la de las piedras preciosas.'",
    "1 Corintios 13:6: 'El amor no se goza de la injusticia, sino que se goza de la verdad.'",
    "Cantares 3:4: 'Apenas la hallé, la traje a casa de mi madre, y al cuarto de la que me concibió.'",
    "Filipenses 2:2: 'Completad mi gozo, sintiendo lo mismo, teniendo el mismo amor, unánimes, sintiendo una misma cosa.'",
    "Proverbios 15:17: 'Mejor es la comida de legumbres donde hay amor, que el buey engordado y con él el odio.'",
    "1 Juan 3:18: 'Hijitos míos, no amemos de palabra ni de lengua, sino de hecho y en verdad.'",
    "Mateo 5:44: 'Pero yo os digo: Amad a vuestros enemigos, bendecid a los que os maldicen, haced bien a los que os aborrecen, y orad por los que os ultrajan y os persiguen.'",
    "Cantares 7:10: 'Yo soy de mi amado, y su deseo es hacia mí.'",
    "Romanos 12:10: 'Amados los unos a los otros con amor fraternal; en cuanto a honra, prefiriéndoos los unos a los otros.'",
    "1 Corintios 7:3: 'El marido cumpla con la mujer el deber conyugal, y asimismo la mujer con el marido.'",
    "Efesios 5:21: 'Someteos unos a otros en el temor de Dios.'",
    "Romanos 8:39: 'Ni lo alto, ni lo profundo, ni ninguna otra cosa creada nos podrá separar del amor de Dios, que es en Cristo Jesús Señor nuestro.'",
    "1 Corintios 7:4: 'La mujer no tiene potestad sobre su propio cuerpo, sino el marido; y asimismo el marido no tiene potestad sobre su propio cuerpo, sino la mujer.'",
    "Proverbios 24:3-4: 'Con sabiduría se edifica la casa, y con prudencia se afirma; con ciencia se llenan las cámaras de todo bien preciado y deseable.'",
    "1 Pedro 3:7: 'Vosotros, maridos, igualmente, vivid con ellas sabiamente, dando honor a la mujer como a vaso más frágil, y como a coherederas de la gracia de la vida, para que vuestras oraciones no tengan estorbo.'",
    "Cantares 4:16: 'Levántate, norte, y ven, sur; sople mi viento en mi huerto, y derramen sus aromas. Venga mi amado a su huerto y coma de su dulce fruta.'",
    "Proverbios 14:1: 'La mujer sabia edifica su casa; mas la necia con sus manos la derriba.'",
    "Mateo 19:6: 'Así que no son ya más dos, sino una sola carne. Por tanto, lo que Dios juntó, no lo separe el hombre.'",
    "Colosenses 3:18: 'Casadas, estad sujetas a vuestros maridos, como conviene en el Señor.'",
    "1 Juan 3:16: 'En esto hemos conocido el amor, en que él puso su vida por nosotros; también nosotros debemos poner nuestras vidas por los hermanos.'",
    "Proverbios 18:22: 'El que halla esposa halla el bien, y alcanza la benevolencia de Jehová.'",
    "1 Timoteo 5:8: 'Pero si alguno no provee para los suyos, y especialmente para los de su casa, ha negado la fe, y es peor que el impío.'",
    "Eclesiastés 4:9-12: 'Mejor son dos que uno; porque tienen mejor paga de su trabajo. Porque si cayeren, el uno levantará a su compañero; pero ay del solo que cuando cayere no habrá segundo que lo levante.'",
    ],
    "Tristeza 😔": [
    "Salmo 34:18: El Señor está cerca de los quebrantados de corazón, y salva a los de espíritu abatido.",
    "Mateo 5:4: Bienaventurados los que lloran, porque ellos recibirán consolación.",
    "Juan 16:33: En el mundo tendréis aflicción; pero confiad, yo he vencido al mundo.",
    "Salmo 42:11: ¿Por qué te abates, alma mía, y por qué te turbas dentro de mí? Espera en Dios.",
    "Isaías 41:10: No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios que te esfuerzo; siempre te ayudaré, siempre te sustentaré con la diestra de mi justicia.",
    "Salmo 30:5: Porque un momento será su ira, pero su favor dura toda la vida; por la noche durará el lloro, y a la mañana vendrá la alegría.",
    "2 Corintios 1:3-4: Bendito sea el Dios y Padre de nuestro Señor Jesucristo, Padre de misericordias y Dios de toda consolación, el cual nos consuela en todas nuestras tribulaciones, para que podamos también nosotros consolar a los que están en cualquier tribulación, por medio de la consolación con que nosotros somos consolados por Dios.",
    "Lamentaciones 3:22-23: Por la misericordia de Jehová no hemos sido consumidos, porque nunca decayeron sus misericordias. Nuevas son cada mañana; grande es tu fidelidad.",
    "Isaías 61:3: A ordenar que a los afligidos de Sion se les dé gloria en lugar de ceniza, aceite de gozo en lugar de luto, manto de alegría en lugar del espíritu angustiado; y serán llamados árboles de justicia, plantío de Jehová, para gloria suya.",
    "Salmo 56:8: Tú has contado mis huidas; pon mis lágrimas en tu redoma; ¿no están ellas en tu libro?",
    "Salmo 73:26: Mi carne y mi corazón desfallecen; mas la roca de mi corazón es Dios, y mi porción para siempre.",
    "Romanos 8:18: Porque considero que los sufrimientos de este tiempo presente no son comparables con la gloria que en nosotros ha de ser revelada.",
    "Filipenses 4:6-7: Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración y ruego, con acción de gracias. Y la paz de Dios, que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos en Cristo Jesús.",
    "2 Corintios 4:8-9: Que estamos atribulados en todo, pero no angustiados; en apuros, pero no desesperados; perseguidos, pero no desamparados; derribados, pero no destruidos.",
    "Salmo 51:17: Los sacrificios de Dios son el espíritu quebrantado; al corazón contrito y humillado no despreciarás tú, oh Dios.",
    "Isaías 61:1: El Espíritu de Jehová el Señor está sobre mí, porque me ha ungido Jehová; me ha enviado a predicar buenas nuevas a los abatidos, a vendar a los quebrantados de corazón...",
    "Salmo 126:5: Los que sembraron con lágrimas, con regocijo segarán.",
    "Mateo 11:28: Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar.",
    "Salmo 9:9: Jehová será refugio del pobre, refugio para el tiempo de angustia.",
    "Salmo 147:3: Él sana a los quebrantados de corazón, y venda sus heridas.",
    "1 Pedro 5:7: Echad toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.",
    "Hebreos 4:15-16: Porque no tenemos un sumo sacerdote que no pueda compadecerse de nuestras debilidades, sino uno que fue tentado en todo según nuestra semejanza, pero sin pecado. Acerquémonos, pues, con confianza al trono de la gracia, para alcanzar misericordia y hallar gracia para el oportuno socorro.",
    "Mateo 26:38: Entonces Jesús les dijo: Mi alma está muy triste, hasta la muerte; quedaos aquí y velad conmigo.",
    "Salmo 40:1-3: Pacientemente esperé a Jehová, y se inclinó a mí, y oyó mi clamor. Me sacó del pozo de la desesperación, del lodo cenagoso; puso mis pies sobre peña, y enderezó mis pasos.",
    "Isaías 40:31: Pero los que esperan a Jehová tendrán nuevas fuerzas; levantarán alas como las águilas; correrán, y no se cansarán; caminarán, y no se fatigarán.",
    "Filipenses 4:13: Todo lo puedo en Cristo que me fortalece.",
    "Romanos 15:13: Y el Dios de esperanza os llene de todo gozo y paz en el creer, para que abundéis en esperanza por el poder del Espíritu Santo.",
    "1 Tesalonicenses 5:11: Por lo cual, animaos unos a otros, y edificaos unos a otros, así como lo hacéis.",
    "2 Corintios 12:9-10: Y me ha dicho: Bástate mi gracia; porque mi poder se perfecciona en la debilidad. Por lo cual, de buena gana me gloriaré más bien en mis debilidades, para que repose sobre mí el poder de Cristo.",
    "Salmo 55:22: Echa sobre Jehová tu carga, y él te sustentará; no dejará para siempre caído al justo."
  ],
  "Depresión 😞": [
    "Salmo 42:5: ¿Por qué te abates, alma mía, y por qué te turbas dentro de mí? Espera en Dios, porque aún he de alabarle, salvación mía y Dios mío.",
    "Isaías 57:15: Porque así dijo el Alto y Sublime, el que habita la eternidad, y cuyo nombre es el Santo: Yo habito en la altura y la santidad, y con el quebrantado y humilde de espíritu, para hacer vivir el espíritu de los humildes, y para vivificar el corazón de los quebrantados.",
    "Mateo 11:28: Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar.",
    "Salmo 34:17-18: Claman los justos, y Jehová oye, y los libra de todas sus angustias. Cercano está Jehová a los quebrantados de corazón; y salva a los contritos de espíritu.",
    "Isaías 41:10: No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios que te esfuerzo; siempre te ayudaré, siempre te sustentaré con la diestra de mi justicia.",
    "Salmo 40:1-3: Pacientemente esperé a Jehová, y se inclinó a mí, y oyó mi clamor. Me sacó del pozo de la desesperación, del lodo cenagoso; puso mis pies sobre peña, y enderezó mis pasos.",
    "Salmo 30:5: Porque un momento será su ira, pero su favor dura toda la vida; por la noche durará el lloro, y a la mañana vendrá la alegría.",
    "Romanos 8:18: Porque considero que los sufrimientos de este tiempo presente no son comparables con la gloria que en nosotros ha de ser revelada.",
    "Filipenses 4:6-7: Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración y ruego, con acción de gracias. Y la paz de Dios, que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos en Cristo Jesús.",
    "1 Pedro 5:7: Echad toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.",
    "Salmo 73:26: Mi carne y mi corazón desfallecen; mas la roca de mi corazón es Dios, y mi porción para siempre.",
    "Filipenses 4:13: Todo lo puedo en Cristo que me fortalece.",
    "Juan 14:27: La paz os dejo, mi paz os doy; yo no os la doy como el mundo la da. No se turbe vuestro corazón, ni tenga miedo.",
    "Isaías 40:29-31: Él da esfuerzo al cansado, y multiplica las fuerzas al que no tiene ningunas. Los muchachos se cansan y se fatigan, los jóvenes flaquean y caen; pero los que esperan a Jehová tendrán nuevas fuerzas; levantarán alas como las águilas; correrán, y no se cansarán; caminarán, y no se fatigarán.",
    "2 Corintios 1:3-4: Bendito sea el Dios y Padre de nuestro Señor Jesucristo, Padre de misericordias y Dios de toda consolación, el cual nos consuela en todas nuestras tribulaciones, para que podamos también nosotros consolar a los que están en cualquier tribulación, por medio de la consolación con que nosotros somos consolados por Dios."
  ],
  "Ansiedad 😟": [
    "Filipenses 4:6-7: Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración y ruego, con acción de gracias. Y la paz de Dios, que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos en Cristo Jesús.",
    "Mateo 6:34: No os afanéis, pues, por el día de mañana, porque el día de mañana traerá su afán. Bástale a cada día su propio mal.",
    "Salmo 55:22: Echa sobre Jehová tu carga, y él te sustentará; no dejará para siempre caído al justo.",
    "1 Pedro 5:7: Echad toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.",
    "Isaías 41:10: No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios que te esfuerzo; siempre te ayudaré, siempre te sustentaré con la diestra de mi justicia.",
    "Juan 14:27: La paz os dejo, mi paz os doy; yo no os la doy como el mundo la da. No se turbe vuestro corazón, ni tenga miedo.",
    "Proverbios 3:5-6: Confía en Jehová con todo tu corazón, y no te apoyes en tu propia prudencia; reconócelo en todos tus caminos, y él enderezará tus veredas.",
    "Salmo 94:19: En la multitud de mis pensamientos dentro de mí, tus consolaciones alegraban mi alma.",
    "Mateo 11:28: Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar.",
    "Isaías 26:3: Tú guardarás en paz perfecta a aquel cuyo pensamiento en ti persevera; porque en ti ha confiado.",
    "Romanos 15:13: Y el Dios de esperanza os llene de todo gozo y paz en el creer, para que abundéis en esperanza por el poder del Espíritu Santo.",
    "Proverbios 12:25: La congoja en el corazón del hombre lo abate; mas la buena palabra lo alegra."
  ],
  "Felicidad 😊": [
    "Salmo 16:11: Me mostrarás la senda de la vida; en tu presencia hay plenitud de gozo; delicias a tu diestra para siempre.",
    "Proverbios 3:13: Bienaventurado el hombre que halla sabiduría, y que obtiene inteligencia.",
    "Juan 15:11: Estas cosas os he hablado, para que mi gozo esté en vosotros, y vuestro gozo sea completo.",
    "Salmo 118:24: Este es el día que hizo Jehová; nos gozaremos y alegraremos en él.",
    "Filipenses 4:4: Regocijaos en el Señor siempre. Otra vez digo: ¡Regocijaos!",
    "Salmo 126:3: Grandes cosas ha hecho Jehová con nosotros; estaremos alegres.",
    "Lucas 10:20: Pero no os regocijéis de que los espíritus se os sujetan, sino regocijaos de que vuestros nombres están escritos en los cielos.",
    "1 Tesalonicenses 5:16: Estad siempre gozosos.",
    "Proverbios 15:13: El corazón alegre hermosea el rostro, pero por el dolor del corazón el espíritu se abate.",
    "Romanos 15:13: Y el Dios de esperanza os llene de todo gozo y paz en el creer, para que abundéis en esperanza por el poder del Espíritu Santo.",
    "Salmo 4:7: Pusiste alegría en mi corazón, más que la de ellos cuando abundan su grano y su mosto.",
    "Isaías 55:12: Porque con alegría saldréis, y con paz seréis vueltos; los montes y los collados levantarán canción delante de vosotros, y todos los árboles del campo darán palmadas de aplauso.",
    "Salmo 97:12: Alegraos, justos, en Jehová; y alabad la memoria de su santidad.",
    "Mateo 5:3-12: Bienaventurados los pobres en espíritu, porque de ellos es el reino de los cielos. Bienaventurados los que lloran, porque ellos recibirán consolación... (continúa).",
    "Gálatas 5:22: Pero el fruto del Espíritu es amor, gozo, paz, paciencia, benignidad, bondad, fe.",
    "Salmo 100:2: Servid a Jehová con alegría; venid ante su presencia con regocijo.",
    "1 Crónicas 16:27: Gloria y honra están en su presencia; poder y alegría en su morada.",
    "Isaías 61:10: Me gozaré mucho en Jehová, mi alma se alegrará en mi Dios; porque me vistió con vestiduras de salvación, me rodeó con manto de justicia, como a novio que se adorna con atavíos, y como a novia que se adorna con sus joyas.",
    "Proverbios 17:22: El corazón alegre es buena medicina; mas el espíritu triste seca los huesos.",
    "Salmo 84:10: Porque mejor es un día en tus atrios que mil fuera de ellos; escogería antes estar a la puerta de la casa de mi Dios, que habitar en las moradas de maldad.",
    "Lucas 15:10: Así os digo que hay gozo delante de los ángeles de Dios por un pecador que se arrepiente."
  ],
  "Escuela 📚": [
    "Proverbios 1:7: El temor de Jehová es el principio de la sabiduría; los insensatos desprecian la sabiduría y la enseñanza.",
    "Proverbios 2:6: Porque Jehová da la sabiduría, y de su boca viene el conocimiento y la inteligencia.",
    "Proverbios 4:7: Sabiduría es la principal cosa; adquiere sabiduría, y con todos tus bienes adquiere inteligencia.",
    "Mateo 7:24: Cualquiera, pues, que oye estas palabras mías, y las hace, le compararé a un hombre prudente que edificó su casa sobre la roca.",
    "Filipenses 4:13: Todo lo puedo en Cristo que me fortalece.",
    "Colosenses 3:23: Y todo lo que hagáis, hacedlo de corazón, como para el Señor y no para los hombres.",
    "Salmo 119:105: Lámpara es a mis pies tu palabra, y lumbrera a mi camino.",
    "Proverbios 3:5-6: Confía en Jehová con todo tu corazón, y no te apoyes en tu propia prudencia; reconócelo en todos tus caminos, y él enderezará tus veredas.",
    "Eclesiastés 7:12: Porque la sabiduría es protección, como la plata es protección; mas la excelencia de la sabiduría es que da vida a quienes la poseen.",
    "2 Timoteo 2:15: Procura con diligencia presentarte a Dios aprobado, como obrero que no tiene de qué avergonzarse, que usa bien la palabra de verdad.",
    "Salmo 37:5: Encomienda a Jehová tu camino, y confía en él; y él hará.",
    "Proverbios 9:9: Da al sabio, y será más sabio; enseña al justo, y aumentará su saber.",
    "Proverbios 4:23: Sobre toda cosa guardada, guarda tu corazón; porque de él mana la vida.",
    "Salmo 25:4: Muéstrame, oh Jehová, tus caminos; enséñame tus sendas.",
    "Isaías 50:4: El Señor Jehová me dio lengua de sabios, para saber hablar palabras al cansado; despertará mañana tras mañana, despertará mi oído para que oiga como los sabios.",
    "Proverbios 22:6: Instruye al niño en su camino, y aun cuando fuere viejo no se apartará de él.",
    "Santiago 1:5: Y si alguno de vosotros tiene falta de sabiduría, pídala a Dios, el cual da a todos abundantemente y sin reproche, y le será dada.",
    "Salmo 111:10: El principio de la sabiduría es el temor de Jehová; buen entendimiento tienen todos los que practican sus mandamientos; su loor permanece para siempre.",
    "Colosenses 1:9: Por lo cual también nosotros, desde el día que lo oímos, no cesamos de orar por vosotros, y de pedir que seáis llenos del conocimiento de su voluntad en toda sabiduría e inteligencia espiritual.",
    "Proverbios 3:13: Bienaventurado el hombre que halla sabiduría, y que obtiene inteligencia."
  ],
  "Trabajo 💼": [
    "Colosenses 3:23: Y todo lo que hagáis, hacedlo de corazón, como para el Señor y no para los hombres.",
    "Proverbios 12:11: El que labra su tierra se saciará de pan; mas el que sigue a los ociosos es falto de entendimiento.",
    "2 Tesalonicenses 3:10: Porque también cuando estábamos con vosotros, os ordenábamos esto: Si alguno no quiere trabajar, tampoco coma.",
    "Proverbios 14:23: En todo trabajo hay fruto, pero las vanas palabras de los labios empobrecen.",
    "Eclesiastés 9:10: Todo lo que te viniere a la mano para hacer, hazlo según tus fuerzas, porque en el sepulcro, adonde vas, no hay obra, ni trabajo, ni ciencia, ni sabiduría.",
    "Proverbios 22:29: ¿Has visto hombre solícito en su trabajo? Estará delante de los reyes; no estará delante de los de baja condición.",
    "Romanos 12:11: En lo que requiere diligencia, no perezosos; fervientes en espíritu, sirviendo al Señor.",
    "Salmo 90:17: Y sea la luz de Jehová nuestro Dios sobre nosotros; y la obra de nuestras manos confirme sobre nosotros, sí, la obra de nuestras manos confirme.",
    "Proverbios 31:17: Ceñió de fuerza sus lomos, y esforzó sus brazos.",
    "1 Corintios 10:31: Si, pues, coméis o bebéis, o hacéis otra cosa, hacedlo todo para la gloria de Dios."
  ],
  "Fe ✝️": [
    "Hebreos 11:1: Es, pues, la fe la certeza de lo que se espera, la convicción de lo que no se ve.",
    "Mateo 17:20: Y les dijo: Por vuestra poca fe; porque de cierto os digo que si tuviereis fe como un grano de mostaza, diréis a este monte: Pásate de aquí allá, y se pasará; y nada os será imposible.",
    "Marcos 9:23: Jesús le dijo: Si puedes creer, al que cree todo le es posible.",
    "Romanos 10:17: Así que la fe es por el oír, y el oír, por la palabra de Dios.",
    "2 Corintios 5:7: Porque por fe andamos, no por vista.",
    "Santiago 1:6: Pero pida con fe, no dudando nada, porque el que duda es semejante a la onda del mar, que es arrastrada por el viento y echada de una parte a otra.",
    "Mateo 21:22: Y todo lo que pidiereis en oración, creyendo, lo recibiréis.",
    "Marcos 11:24: Por tanto os digo que todo lo que pidáis orando, creed que lo recibiréis, y os vendrá.",
    "Juan 14:1: No se turbe vuestro corazón; creéis en Dios, creed también en mí.",
    "1 Juan 5:4: Porque todo lo que es nacido de Dios vence al mundo; y esta es la victoria que ha vencido al mundo, nuestra fe."
  ],
  "Perdón 🙏": [
    "Efesios 4:32: Antes sed benignos unos con otros, misericordiosos, perdonándoos unos a otros, como Dios también os perdonó en Cristo.",
    "Mateo 6:14-15: Porque si perdonáis a los hombres sus ofensas, os perdonará también a vosotros vuestro Padre celestial; pero si no perdonáis a los hombres sus ofensas, tampoco vuestro Padre os perdonará vuestras ofensas.",
    "Colosenses 3:13: Soportándoos unos a otros, y perdonándoos unos a otros, si alguno tuviera queja contra otro; de la manera que Cristo os perdonó, así también hacedlo vosotros.",
    "Lucas 6:37: No juzguéis, y no seréis juzgados; no condenéis, y no seréis condenados; perdonad, y seréis perdonados.",
    "Mateo 18:21-22: Entonces Pedro se le acercó y le dijo: Señor, ¿cuántas veces perdonaré a mi hermano que peque contra mí? ¿Hasta siete? Jesús le dijo: No te digo hasta siete, sino hasta setenta veces siete."
  ],
  "Desamor 💔": [
    "Salmo 34:18: El Señor está cerca de los quebrantados de corazón, y salva a los de espíritu abatido.",
    "Isaías 41:10: No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios; te fortaleceré, te ayudaré, te sustentaré con la diestra de mi justicia.",
    "1 Corintios 13:4-7: El amor es sufrido, es benigno; el amor no tiene envidia, el amor no es jactancioso, no se embanece; no hace nada indebido, no busca lo suyo, no se irrita, no guarda rencor; no se goza de la injusticia, mas se goza de la verdad; todo lo sufre, todo lo cree, todo lo espera, todo lo soporta.",
    "Romanos 8:28: Y sabemos que a los que aman a Dios, todas las cosas les ayudan a bien, esto es, a los que conforme a su propósito son llamados.",
    "Salmo 147:3: Él sana a los quebrantados de corazón, y venda sus heridas.",
    "1 Pedro 5:7: Echando toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.",
    "Mateo 11:28: Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar.",
    "Isaías 43:18-19: No os acordéis de las cosas pasadas, ni consideréis las cosas antiguas. He aquí que yo hago cosa nueva; pronto saldrá a luz; ¿no la conoceréis?",
    "Salmo 30:5: Porque su ira dura un momento, pero su favor dura toda la vida; por la noche may endurecer el llanto, y a la mañana vendrá la alegría.",
    "Romanos 12:15: Gozaos con los que se gozan; llorad con los que lloran.",
    "2 Corintios 1:3-4: Bendito sea el Dios y Padre de nuestro Señor Jesucristo, el Padre de misericordias y Dios de toda consolación, el cual nos consuela en todas nuestras tribulaciones, para que podamos también nosotros consolar a los que están en cualquier tribulación, por el consuelo con que nosotros somos consolados por Dios.",
    "Filipenses 3:13-14: Hermanos, yo mismo no pretendo haberlo alcanzado; pero una cosa hago: olvidando ciertamente lo que queda atrás, y extendiéndome a lo que está adelante, prosigo al blanco, al premio del supremo llamamiento de Dios en Cristo Jesús.",
    "Romanos 5:3-5: Y no sólo esto, sino que también nos gloriamos en las tribulaciones, sabiendo que la tribulación produce paciencia; y la paciencia, prueba; y la prueba, esperanza; y la esperanza no avergüenza, porque el amor de Dios ha sido derramado en nuestros corazones por el Espíritu Santo que nos fue dado.",
    "Isaías 61:1-3: El Espíritu de Jehová el Señor está sobre mí, porque me ungió Jehová; me ha enviado a predicar buenas nuevas a los abatidos; a vendar a los quebrantados de corazón; a proclamar libertad a los cautivos, y a los prisioneros apertura de la cárcel; a proclamar el año de la buena voluntad de Jehová, y el día de venganza del Dios nuestro; a consolar a todos los enlutados; a ordenar que a los afligidos de Sion se les dé gloria en lugar de ceniza, óleo de gozo en lugar de luto, manto de alegría en lugar de espíritu angustiado.",
    "2 Corintios 4:17: Porque esta leve tribulación momentánea produce en nosotros un cada vez más excelente y eterno peso de gloria.",
    "1 Juan 4:18: En el amor no hay temor, sino que el perfecto amor echa fuera el temor; porque el temor lleva en sí castigo, de donde el que teme no ha sido perfeccionado en el amor.",
    "Salmo 73:26: Mi carne y mi corazón desfallecen; mas la roca de mi corazón y mi porción es Dios para siempre."
  ],
  "Pérdida de familiares 💔": [
    "Juan 14:1-3: No se turbe vuestro corazón; creéis en Dios, creed también en mí. En la casa de mi Padre muchas moradas hay; si así no fuera, yo os lo hubiera dicho; voy a preparar lugar para vosotros. Y si me fuere, y os preparare lugar, vendré otra vez, y os tomaré a mí mismo; para que donde yo estoy, vosotros también estéis.",
    "1 Tesalonicenses 4:13-14: Tampoco queremos, hermanos, que ignoréis acerca de los que duermen, para que no os entristezcáis como los otros que no tienen esperanza. Porque si creemos que Jesús murió y resucitó, así también traerá Dios con Jesús a los que durmieron en él.",
    "Salmo 34:18: El Señor está cerca de los quebrantados de corazón, y salva a los de espíritu abatido.",
    "Apocalipsis 21:4: Enjugará Dios toda lágrima de los ojos de ellos, y no habrá más muerte, ni habrá más llanto, ni clamor, ni dolor; porque las primeras cosas pasaron.",
    "Isaías 41:10: No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios; te fortaleceré, te ayudaré, te sustentaré con la diestra de mi justicia.",
    "2 Corintios 1:3-4: Bendito sea el Dios y Padre de nuestro Señor Jesucristo, el Padre de misericordias y Dios de toda consolación, el cual nos consuela en todas nuestras tribulaciones, para que podamos también nosotros consolar a los que están en cualquier tribulación, por el consuelo con que nosotros somos consolados por Dios.",
    "Romanos 8:18: Pues tengo por cierto que las aflicciones del tiempo presente no son comparables con la gloria venidera que en nosotros ha de manifestarse.",
    "Mateo 5:4: Bienaventurados los que lloran, porque ellos recibirán consolación.",
    "2 Corintios 4:17: Porque esta leve tribulación momentánea produce en nosotros un cada vez más excelente y eterno peso de gloria.",
    "Salmo 147:3: Él sana a los quebrantados de corazón, y venda sus heridas.",
    "Juan 11:25-26: Jesús le dijo: Yo soy la resurrección y la vida; el que cree en mí, aunque esté muerto, vivirá; y todo aquel que vive y cree en mí, no morirá eternamente.",
    "Filipenses 1:21-23: Porque para mí el vivir es Cristo, y el morir es ganancia. Pero si el vivir en la carne resulta para mí en beneficio de la obra, no sé entonces qué escoger. Porque de ambas cosas estoy puesto en estrecho, teniendo deseo de partir y estar con Cristo, lo cual ciertamente es mucho mejor.",
    "Isaías 57:1-2: El justo perece, y no hay quien lo entienda; y los piadosos son recogidos, y nadie lo considera; que de la presencia del mal es recogido el justo. Entrará en paz; descansarán en sus lechos los que andan delante de Dios.",
    "1 Pedro 5:7: Echando toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.",
    "Salmo 46:1-2: Dios es nuestro amparo y fortaleza, nuestro pronto auxilio en las tribulaciones. Por tanto, no temeremos, aunque la tierra sea removida, y se traspasen los montes al corazón del mar.",
    "Romanos 14:8: Si vivimos, para el Señor vivimos; y si morimos, para el Señor morimos. Así pues, ya sea que vivamos o que muramos, somos del Señor.",
    "Salmo 23:4: Aunque ande en valle de sombra de muerte, no temeré mal alguno, porque tú estarás conmigo; tu vara y tu cayado me infundirán aliento.",
    "Mateo 11:28: Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar.",
    "2 Samuel 12:23: Pero ahora que ha muerto, ¿por qué he de ayunar? ¿Puedo yo hacerle volver? Yo iré a él, pero él no volverá a mí.",
    "Revelación 21:4: Enjugará Dios toda lágrima de los ojos de ellos, y no habrá más muerte, ni habrá más llanto, ni clamor, ni dolor; porque las primeras cosas pasaron."
  ]
    # Agrega más categorías aquí
}

@app.route('/', methods=['GET', 'POST'])
def index():
    # Ahora no necesitamos revisar la sesión para el nombre, ya que lo manejará el frontend
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')  # El mensaje enviado por el usuario
    category = request.json.get('category', None)  # La categoría enviada por el usuario
    index = request.json.get('index', 0)  # El índice (si aplica)

    # Obtener el nombre del usuario enviado desde el frontend (se espera que venga en cada solicitud)
    user_name = request.json.get('user_name', 'Usuario')  # Si no hay nombre, usamos 'Usuario' como valor predeterminado

    # Lógica para manejar la entrada del usuario y responder
    if user_input == "Regresar al menú principal":
        response = {
            "message": f"Hola {user_name}, selecciona una opción:",
            "options": list(versiculos.keys())
        }
    elif category and user_input == "Más":
        verses = versiculos.get(category, [])
        if index < len(verses):
            response = {
                "message": verses[index],
                "options": ["Más", "Regresar al menú principal"],
                "category": category,
                "index": index + 1
            }
        else:
            response = {
                "message": "Ya no hay más versículos en esta categoría.",
                "options": ["Regresar al menú principal"]
            }
    elif user_input in versiculos:
        response = {
            "message": versiculos[user_input][0],
            "options": ["Más", "Regresar al menú principal"],
            "category": user_input,
            "index": 1
        }
    else:
        response = {
            "message": f"Hola {user_name}, selecciona una opción:",  # Se asegura que solo se use el nombre del frontend
            "options": list(versiculos.keys())
        }

    return jsonify(response)


@app.route('/exit', methods=['POST'])
def exit():
    # No es necesario eliminar nada de la sesión ya que no la estamos utilizando
    return jsonify({"message": "Sesión cerrada. Vuelve pronto!"})

if __name__ == '__main__':
    app.run(debug=True)
