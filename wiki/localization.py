"""Reviewed locale copy and helpers for the shared Wiki page skeleton.

Game entity names and source identifiers intentionally stay in the source language.
The surrounding interface and editorial explanation use native player vocabulary.
"""
from __future__ import annotations

from copy import deepcopy
import html
import re


LOCALE_ORDER = ('en', 'es', 'it', 'zh-hant')
LANG = {'en': 'en', 'es': 'es', 'it': 'it', 'zh-hant': 'zh-Hant'}
LABEL = {'en': 'English', 'es': 'Español', 'it': 'Italiano', 'zh-hant': '繁體中文'}


UI = {
 'es': {
  'start':'Primeros pasos','tier':'Clasificación','arceus':'Arceus','dex':'Pokédex','moves':'Movimientos','evolutions':'Evoluciones',
  'home':'Inicio','menu':'Menú','main_nav':'Navegación principal','play':'Jugar','search':'Buscar','skip':'Saltar al contenido',
  'guide':'Guía','evolve':'Evolucionar','quick':'Accesos rápidos','related':'Continúa tu partida','sources':'Fuentes y alcance de la versión',
  'reviewed':'Referencia revisada','snapshot':'Este juego y esta versión.','snapshot_text':'Estas guías cubren el PokéSurvivor para navegador de JPTER78.','burst':'¿Juegas a Burst?',
  'on_page':'En esta página','footer':'Pie de página','tagline':'Una referencia independiente para tu próxima partida.',
  'about':'Acerca de y fuentes','privacy':'Privacidad','analytics':'Preferencias de analítica','where':'Dónde jugar','coop':'Ayuda de cooperativo y cuenta','updates':'Actualizaciones',
  'machine':'Guía para máquinas','markdown':'Resumen en Markdown','developer':'Juego del desarrollador','language':'Idioma',
  'legal':'Guía no oficial creada por fans. Sin afiliación con JPTER78, Nintendo, Creatures, GAME FREAK ni The Pokémon Company. Pokémon pertenece a sus respectivos propietarios. Datos del juego: JPTER78 / PokéSurvivor.',
  'code_license':'Licencia del código','font_license':'Licencia de la fuente','brand_sub':'WIKI Y GUÍAS DEL JUEGO',
  'source_note':'Mecánicas y datos comprobados en la versión indicada. Revisar el código fuente no equivale a probar cada situación en una partida.',
  'groups':{'Guides':'Guías','Database':'Base de datos','Home':'Inicio','Search':'Buscar','Help':'Ayuda'},
  'table_search':'Buscar en esta tabla','table_placeholder':'Nombre, movimiento o estadística…','type':'Tipo','all_types':'Todos los tipos','reset':'Restablecer','no_matches':'No hay coincidencias. Prueba otro nombre o restablece los filtros.','reference_table':'Tabla de referencia',
 },
 'it': {
  'start':'Per iniziare','tier':'Classifica','arceus':'Arceus','dex':'Pokédex','moves':'Mosse','evolutions':'Evoluzioni',
  'home':'Home','menu':'Menu','main_nav':'Navigazione principale','play':'Gioca','search':'Cerca','skip':'Vai al contenuto',
  'guide':'Guida','evolve':'Evolvi','quick':'Navigazione rapida','related':'Continua la partita','sources':'Fonti e ambito della versione',
  'reviewed':'Riferimento verificato','snapshot':'Questo gioco, questa versione.','snapshot_text':'Queste guide riguardano PokéSurvivor per browser di JPTER78.','burst':'Stai giocando a Burst?',
  'on_page':'In questa pagina','footer':'Piè di pagina','tagline':'Una guida indipendente per la tua prossima partita.',
  'about':'Informazioni e fonti','privacy':'Privacy','analytics':'Preferenze statistiche','where':'Dove giocare','coop':'Aiuto coop e account','updates':'Aggiornamenti',
  'machine':'Guida per sistemi automatici','markdown':'Panoramica Markdown','developer':'Gioco dello sviluppatore','language':'Lingua',
  'legal':'Guida non ufficiale realizzata dai fan. Nessuna affiliazione con JPTER78, Nintendo, Creatures, GAME FREAK o The Pokémon Company. Pokémon appartiene ai rispettivi titolari. Dati di gioco: JPTER78 / PokéSurvivor.',
  'code_license':'Licenza del codice','font_license':'Licenza del font','brand_sub':'WIKI E GUIDE DI GIOCO',
  'source_note':'Meccaniche e dati sono stati controllati nella versione indicata. L’analisi del codice sorgente non equivale a una prova completa in partita.',
  'groups':{'Guides':'Guide','Database':'Database','Home':'Home','Search':'Cerca','Help':'Aiuto'},
  'table_search':'Cerca nella tabella','table_placeholder':'Nome, mossa o statistica…','type':'Tipo','all_types':'Tutti i tipi','reset':'Azzera','no_matches':'Nessun risultato. Prova un altro nome o azzera i filtri.','reference_table':'Tabella di riferimento',
 },
 'zh-hant': {
  'start':'新手入門','tier':'強度排行','arceus':'阿爾宙斯','dex':'寶可夢圖鑑','moves':'招式','evolutions':'進化','home':'首頁','menu':'選單','main_nav':'主要導覽','play':'開始遊戲','search':'搜尋','skip':'跳至主要內容',
  'guide':'攻略','evolve':'進化','quick':'快速導覽','related':'繼續規劃本局','sources':'資料來源與版本範圍','reviewed':'資料核對日期','snapshot':'本遊戲、本版本。','snapshot_text':'本站攻略對應 JPTER78 的瀏覽器版 PokéSurvivor。','burst':'你玩的是 Burst 嗎？',
  'on_page':'本頁內容','footer':'頁尾','tagline':'協助你規劃下一局的獨立攻略站。','about':'關於本站與資料來源','privacy':'隱私權','analytics':'分析資料偏好','where':'遊玩方式','coop':'合作模式與帳號協助','updates':'更新紀錄',
  'machine':'機器可讀指南','markdown':'Markdown 總覽','developer':'開發者遊戲頁','language':'語言','legal':'非官方粉絲攻略站，與 JPTER78、Nintendo、Creatures、GAME FREAK 或 The Pokémon Company 無隸屬關係。Pokémon 相關權利屬各自權利人；遊戲資料來自 JPTER78 / PokéSurvivor。',
  'code_license':'程式碼授權','font_license':'字型授權','brand_sub':'維基與遊戲攻略','source_note':'本頁機制與資料依標示版本核對；檢查原始碼不等於已在每種實戰情境逐一測試。',
  'groups':{'Guides':'攻略','Database':'資料庫','Home':'首頁','Search':'搜尋','Help':'協助'},
  'table_search':'搜尋本表','table_placeholder':'輸入名稱、招式或數值…','type':'屬性','all_types':'所有屬性','reset':'重設','no_matches':'找不到符合項目，請改用其他名稱或重設篩選。','reference_table':'資料表',
 }
}


# title, description, lead, practical guidance. Copy was edited for each locale;
# it is not an English appendix and it does not claim unrecorded play tests.
PAGES = {
 'es': {
  '':('Wiki de PokéSurvivor: clasificaciones, builds y guías','Wiki independiente de PokéSurvivor con 966 Pokémon, clasificaciones, builds legales, cooperativo, evoluciones y guía de Arceus.','Planifica tu próxima partida con datos de la versión registrada: elige compañero, comprueba evoluciones y consulta tipos sin mezclar PokéSurvivor con otros proyectos.','Empieza por la guía básica si es tu primera partida. Si ya conoces los controles, compara la lista completa y confirma el requisito de evolución antes de gastar una mejora.'),
  'how-to-play':('Cómo jugar a PokéSurvivor: guía para empezar','Aprende los controles, las elecciones de nivel y la ruta de evolución para completar tu primera partida de PokéSurvivor.','PokéSurvivor es un juego de supervivencia para navegador: te mueves, recoges experiencia y eliges una mejora cuando subes de nivel. El ataque funciona solo, así que la colocación importa.','Primero aprende a mantener distancia y a recoger experiencia sin quedar rodeado. Después sube tu movimiento inicial hasta el máximo, toma la carta de estadística indicada y busca la carta dorada de evolución.'),
  'mobile':('PokéSurvivor en Android y iPhone: controles y soluciones','Guía para jugar a PokéSurvivor en Android o iPhone, instalarlo como PWA y proteger la partida guardada.','En móvil se juega desde el navegador oficial. Usa el control táctil, evita cambiar de pestaña durante una partida y añade el sitio a la pantalla de inicio si quieres una experiencia más parecida a una aplicación.','El guardado pertenece al navegador y al perfil que estás usando. Antes de borrar datos, cambiar de teléfono o usar modo privado, vincula la cuenta cuando el juego lo permita y conserva una copia de la información importante.'),
  'builds':('Builds de PokéSurvivor: planificador de movimientos y evoluciones','Planifica una build legal con compañero inicial, segundo movimiento compatible y requisitos de evolución.','Una build útil parte del movimiento inicial real y añade un movimiento compatible con el tipo del compañero. El planificador no abre tu guardado ni altera la partida.','Elige primero una forma de atacar que puedas controlar, reserva las cartas de estadística necesarias para evolucionar y equilibra daño con movilidad o supervivencia. Comprueba el resultado en tus propias partidas.'),
  'download':('¿Descargar PokéSurvivor? Web, PWA y APK','Dónde jugar a PokéSurvivor, cómo instalar la PWA y qué revisar antes de confiar en un APK no oficial.','La versión de referencia funciona en el navegador de pokesurvivor.com. Puedes añadirla a la pantalla de inicio como PWA; no necesitas pagar una descarga para usar el juego oficial.','Si encuentras un APK o un puerto de terceros, comprueba quién lo publica, qué permisos solicita y si corresponde a la misma versión. Un nombre parecido no garantiza el mismo contenido ni el mismo sistema de guardado.'),
  'co-op':('Cooperativo de PokéSurvivor: salas, invitaciones y soluciones','Crea una sala, invita a otra persona y resuelve los fallos habituales del modo cooperativo de PokéSurvivor.','Para jugar en cooperativo, una persona crea la sala y comparte el código; la otra se une desde la misma versión del juego. No publiques códigos de cuenta ni datos privados.','Si la invitación falla, recargad ambos la versión más reciente, comprobad la red y cread una sala nueva. Las diferencias de versión y una sesión caducada suelen ser más relevantes que repetir el mismo código.'),
  'survivor-vs-burst':('PokéSurvivor y Pokémon Survivor Burst: diferencias','Identifica si juegas al PokéSurvivor de JPTER78 o a Pokémon Survivor Burst antes de seguir una guía.','Son proyectos distintos. Esta wiki documenta el juego para navegador de JPTER78; una captura, un APK o una mecánica de Burst no demuestra que exista en esta versión.','Comprueba la dirección web, el desarrollador y los nombres de los modos. Si Arceus, las descargas o las reglas no coinciden, usa una guía específica del proyecto que tienes abierto.'),
  'about':('Acerca de esta wiki y método editorial','Cómo se verifican los datos, las recomendaciones y los recursos multimedia de Pokémon Survivor Wiki.','Esta es una referencia independiente. Los números y requisitos proceden de una instantánea identificada del código público; las recomendaciones editoriales se presentan como criterios, no como resultados de partidas inventados.','Conservamos los nombres internos necesarios para comprobar los datos, indicamos la versión revisada y distinguimos las capturas del juego de los diagramas explicativos. Las correcciones deben mantener esa trazabilidad.'),
  'privacy':('Privacidad y herramientas locales','Qué datos utiliza esta wiki, cómo funciona la analítica opcional y qué hacen los calculadores en tu navegador.','Las búsquedas, los filtros y los calculadores se ejecutan en tu navegador. Las herramientas no abren la partida guardada ni piden credenciales del juego.','La analítica depende de tu preferencia. Puedes cambiarla desde el pie de página; evita introducir códigos de sala, correos u otros datos personales en búsquedas o enlaces compartidos.'),
  'pokedex':('Pokédex de PokéSurvivor: estadísticas y obtención','Busca los 966 compañeros de PokéSurvivor por nombre o tipo y compara PS, velocidad, ataque y forma de obtención.','Esta Pokédex reúne los 966 compañeros de la instantánea registrada. Sus valores pertenecen a PokéSurvivor y no son las estadísticas de combate de los juegos principales.','Busca por nombre o número y combina el filtro de tipo. La columna de obtención distingue el gacha regional de las opciones iniciales y de los encuentros que quedan fuera de esa reserva.'),
  'moves':('Movimientos de PokéSurvivor: daño, patrones y evoluciones','Consulta 64 movimientos con daño base, enfriamiento, patrón, nivel máximo y evolución.','Compara cada movimiento por su funcionamiento y por sus valores. El daño y el enfriamiento de nivel uno no bastan para calcular DPS: cambian el alcance, la duración y la frecuencia de impacto.','Usa el patrón para decidir si puedes mantener una buena posición. Después abre la evolución correspondiente y reserva la carta de estadística exacta durante la misma partida.'),
  'move-evolutions':('Evoluciones de movimientos y comprobador de requisitos','Consulta 59 evoluciones de movimientos, nivel requerido y carta de estadística necesaria en PokéSurvivor.','Lleva el movimiento a su nivel máximo, toma la mejora de estadística indicada en esa partida y elige la carta dorada cuando aparezca. Cumplir los requisitos solo habilita la evolución.','Si no aparece la carta dorada, revisa el nivel y el requisito exacto. Una mejora permanente distinta no sustituye la carta de la partida, y los buffs sin evolución no pueden transformarse.'),
  'starters':('Mejores iniciales de PokéSurvivor: las 29 opciones','Compara los 29 compañeros iniciales por movimiento, PS, velocidad, ataque y requisito de evolución.','El cuestionario propone un compañero, pero puedes rechazarlo. Elige una apertura cuyo patrón de ataque puedas controlar y consulta qué estadística necesita para evolucionar.','No todos los compañeros del mismo tipo empiezan con el mismo movimiento. Compara alcance, movilidad y requisito de la carta antes de fijarte solo en el multiplicador de ataque.'),
  'starter-tier-list':('Clasificación de iniciales de PokéSurvivor','Compara los 29 iniciales con bandas transparentes de estadísticas, movimiento inicial y requisitos de evolución.','La puntuación pondera PS, velocidad y ataque para comparar el comienzo de una partida. No representa victorias, tiempo de supervivencia ni una clasificación oficial.','Usa la banda como primer filtro. La forma del movimiento, el alcance, el clima y tu control pueden hacer que una opción con menos puntuación funcione mejor para ti.'),
  'tier-list':('Tier list de PokéSurvivor: 966 Pokémon clasificados','Busca y ordena los 966 compañeros mediante una puntuación reproducible de atributos iniciales.','La clasificación usa atributos del código: 35 % PS, 25 % velocidad y 40 % ataque, normalizados por los máximos de la plantilla. No afirma haber probado 966 partidas.','Filtra por el tipo que necesitas, revisa los movimientos disponibles y confirma la evolución antes de crear una build. Para comenzar una partida, consulta también la lista específica de 29 iniciales.'),
  'types':('Tabla de tipos y calculadora de daño de PokéSurvivor','Calcula enfrentamientos simples y dobles con los multiplicadores modificados y el límite de 2,4×.','PokéSurvivor suaviza la tabla habitual: debilidad 1,6×, resistencia 0,6× e inmunidad principal 0,3×. En doble tipo, el producto queda limitado entre 0,3× y 2,4×.','Las filas representan el tipo atacante y las columnas el defensor. El resultado solo es el factor de tipo; no incluye clima, atributo de ataque, defensa ni efectos adicionales.'),
  'legendaries':('Legendarios de PokéSurvivor: grietas y plantilla','Cómo funcionan las grietas y qué legendarios o míticos aparecen en la instantánea de PokéSurvivor.','Las grietas llevan a una arena separada con un encuentro legendario. Vencerlo concede la recompensa indicada, pero no añade automáticamente el compañero normal a la colección.','Entra con una vía de escape, observa el terreno y evita confundir el encuentro de grieta con la elegibilidad del gacha regional. La tabla identifica la plantilla, no un calendario garantizado.'),
  'updates':('Actualizaciones de PokéSurvivor: recargas, cooperativo y Arceus','Cambios verificados de PokéSurvivor hasta el 15 de octubre de 2026.','Este registro resume cambios publicados por el desarrollador y comprobados en la instantánea indicada. No presenta cada línea como una prueba de juego independiente.','Una actualización obligatoria muestra un aviso de diez segundos, termina la partida, guarda las recompensas registradas y recarga. Revisa aquí cambios de cooperativo, recuperación y Judgment of Arceus.'),
  'arceus-judgment':('Guía de Arceus: sobrevive al Juicio de los 30 minutos','Ataques, refuerzos legendarios y logros verificados del Judgment of Arceus de PokéSurvivor.','A los 30:00 la partida pasa a Ruins of Judgment. Arceus es invencible en la versión oficial verificada: el objetivo es esquivar, sobrevivir y derrotar los refuerzos necesarios.','Protege una ruta de movimiento antes del minuto 28, responde primero a las zonas de aviso y concentra el daño en un refuerzo cada vez. Los pilares, rayos, ondas y el contacto obligan a mantener espacio.'),
  'upgrades':('Mejoras de PokéSurvivor: cartas y prioridades','Consulta las mejoras de una partida y decide cuándo priorizar daño, movimiento, defensa o requisitos de evolución.','Las cartas de mejora cambian la partida actual. Algunas estadísticas son además requisitos de evolución, por lo que una elección temprana puede desbloquear la carta dorada más adelante.','Reserva primero los requisitos de tus movimientos principales y evita perseguir una fórmula universal. El espacio, el patrón de ataque y el objetivo de la partida cambian la prioridad correcta.'),
  'gacha-calculator':('Calculadora de gacha y pity de PokéSurvivor','Calcula probabilidades base y comprueba si una cantidad de tiradas alcanza el pity duro de 70.','Introduce las tiradas previstas y tu pity actual. El cálculo muestra probabilidades base independientes y si la ventana alcanza el pity duro; no predice un Pokémon concreto.','Una probabilidad acumulada no garantiza el resultado antes del pity. Usa el cálculo para presupuestar recursos y consulta la Pokédex para saber qué compañeros pertenecen a la reserva regional.'),
  'search':('Buscar en la wiki de PokéSurvivor','Busca guías, Pokémon y movimientos en la wiki de PokéSurvivor.','Encuentra una guía, un compañero o un movimiento.','Prueba con el nombre oficial del Pokémon o del movimiento; también puedes buscar términos como móvil, cooperativo o Arceus.'),
 },
 'it': {}, 'zh-hant': {}
}


# Italian and Traditional Chinese use independent natural-language copy while
# sharing the same verified game facts and components.
_IT = {
 '':'Wiki di PokéSurvivor: classifiche, build e guide|Wiki indipendente con 966 Pokémon, classifiche, build valide, coop, evoluzioni e guida ad Arceus.|Prepara la prossima partita con i dati della versione registrata: scegli il compagno, controlla le evoluzioni e consulta i tipi senza confondere progetti diversi.|Se è la prima partita, parti dalla guida base. Se conosci già i comandi, confronta la rosa completa e verifica il requisito di evoluzione prima di scegliere un potenziamento.',
 'how-to-play':'Come giocare a PokéSurvivor: guida iniziale|Comandi, scelte di livello e percorso di evoluzione per la prima partita.|PokéSurvivor è un survival per browser: ti muovi, raccogli esperienza e scegli un potenziamento a ogni livello. Gli attacchi sono automatici, quindi il posizionamento è decisivo.|Impara prima a mantenere le distanze e raccogliere esperienza senza farti circondare. Porta poi la mossa iniziale al livello massimo, prendi la carta statistica richiesta e cerca la carta evoluzione dorata.',
 'mobile':'PokéSurvivor su Android e iPhone: comandi e soluzioni|Come giocare da telefono, installare la PWA e proteggere il salvataggio.|Da mobile si usa il sito ufficiale nel browser. Sfrutta i comandi touch, evita di cambiare scheda durante una partita e aggiungi il sito alla schermata Home se preferisci un avvio simile a un’app.|Il salvataggio appartiene al browser e al profilo in uso. Prima di cancellare dati, cambiare telefono o usare la navigazione privata, collega l’account quando il gioco lo consente.',
 'builds':'Build di PokéSurvivor: pianificatore di mosse ed evoluzioni|Crea una build valida con compagno iniziale, seconda mossa compatibile e requisiti di evoluzione.|Una buona build parte dalla vera mossa iniziale e aggiunge una mossa compatibile con il tipo del compagno. Il pianificatore non legge né modifica il salvataggio.|Scegli un attacco che sai gestire, conserva le carte statistiche richieste per le evoluzioni e bilancia danno, movimento e resistenza. Valuta poi il percorso nelle tue partite.',
 'download':'Scaricare PokéSurvivor? Web, PWA e APK|Dove giocare, come installare la PWA e cosa verificare prima di usare un APK non ufficiale.|La versione documentata funziona nel browser su pokesurvivor.com. Puoi aggiungerla alla schermata Home come PWA; il gioco ufficiale non richiede un download a pagamento.|Per un APK o porting di terzi, controlla autore, permessi e versione. Un nome simile non garantisce gli stessi contenuti o lo stesso sistema di salvataggio.',
 'co-op':'Coop di PokéSurvivor: stanze, inviti e soluzioni|Come creare una stanza e risolvere i problemi comuni della modalità cooperativa.|Una persona crea la stanza e condivide il codice; l’altra entra usando la stessa versione del gioco. Non condividere credenziali o dati personali.|Se l’invito non funziona, aggiornate entrambi la pagina, controllate la rete e create una nuova stanza. Versioni diverse o sessioni scadute contano più del riutilizzo dello stesso codice.',
 'survivor-vs-burst':'PokéSurvivor e Pokémon Survivor Burst: differenze|Riconosci il progetto corretto prima di seguire una guida.|Sono giochi distinti. Questa wiki documenta il titolo per browser di JPTER78; schermate, APK e meccaniche di Burst non provano che esistano in questa versione.|Controlla indirizzo, sviluppatore e nomi delle modalità. Se Arceus, download o regole non coincidono, usa una guida dedicata al progetto che hai aperto.',
 'about':'Informazioni sulla wiki e metodo editoriale|Come verifichiamo dati, consigli e contenuti multimediali.|Questa è una guida indipendente. Numeri e requisiti provengono da una versione identificata del codice pubblico; i consigli editoriali sono criteri dichiarati, non risultati inventati.|Manteniamo i nomi interni necessari alla verifica, indichiamo la versione controllata e distinguiamo le immagini di gioco dai diagrammi esplicativi.',
 'privacy':'Privacy e strumenti locali|Dati usati dalla wiki, statistiche facoltative e calcoli nel browser.|Ricerca, filtri e calcolatori funzionano nel browser. Non leggono il salvataggio e non chiedono credenziali del gioco.|Le statistiche dipendono dalla tua preferenza e puoi modificarla nel piè di pagina. Non inserire codici stanza, email o dati personali nelle ricerche o nei link condivisi.',
 'pokedex':'Pokédex di PokéSurvivor: statistiche e ottenimento|Cerca 966 compagni per nome o tipo e confronta PS, velocità, attacco e ottenimento.|Il Pokédex raccoglie tutti i 966 compagni della versione registrata. I valori appartengono a PokéSurvivor e non sono le statistiche dei giochi principali.|Cerca per nome o numero e combina il filtro del tipo. La colonna di ottenimento distingue gacha regionale, scelte iniziali e compagni fuori dal pool.',
 'moves':'Mosse di PokéSurvivor: danno, schemi ed evoluzioni|Consulta 64 mosse con danno base, ricarica, schema, livello massimo ed evoluzione.|Valuta una mossa sia per il comportamento sia per i numeri. Danno e ricarica al livello uno non sono un DPS completo: cambiano gittata, durata e frequenza dei colpi.|Scegli uno schema che ti permetta di mantenere una buona posizione. Poi apri l’evoluzione e conserva la carta statistica esatta nella stessa partita.',
 'move-evolutions':'Evoluzioni delle mosse e controllo requisiti|Consulta 59 evoluzioni, livello e carta statistica richiesti.|Porta la mossa al livello massimo, prendi nella stessa partita la statistica indicata e scegli la carta dorata quando compare. I requisiti rendono l’evoluzione disponibile, non automatica.|Se la carta non appare, ricontrolla livello e requisito. Un potenziamento permanente diverso non sostituisce la carta della partita; i buff senza evoluzione non si trasformano.',
 'starters':'Migliori iniziali di PokéSurvivor: tutte le 29 scelte|Confronta mossa iniziale, PS, velocità, attacco e requisito di evoluzione.|Il quiz suggerisce un compagno, ma puoi rifiutarlo. Scegli un’apertura con uno schema d’attacco che sai controllare e verifica la statistica necessaria all’evoluzione.|Compagni dello stesso tipo non iniziano sempre con la stessa mossa. Confronta gittata, mobilità e requisito prima di guardare solo il moltiplicatore d’attacco.',
 'starter-tier-list':'Classifica degli iniziali di PokéSurvivor|Confronto trasparente dei 29 iniziali con statistiche, mosse e requisiti.|Il punteggio combina PS, velocità e attacco per confrontare l’avvio. Non misura vittorie, durata della sopravvivenza o una classifica ufficiale.|Usa la fascia come primo filtro. Schema, gittata, meteo e controllo personale possono rendere migliore una scelta con un punteggio inferiore.',
 'tier-list':'Tier list di PokéSurvivor: 966 Pokémon classificati|Cerca e ordina i 966 compagni con un punteggio riproducibile.|La classifica usa gli attributi del codice: 35% PS, 25% velocità e 40% attacco, normalizzati sui massimi. Non dichiara 966 prove di gioco.|Filtra il tipo, verifica le mosse disponibili e controlla l’evoluzione prima di comporre la build. Per l’avvio usa anche la lista dedicata ai 29 iniziali.',
 'types':'Tabella dei tipi e calcolatore danni di PokéSurvivor|Calcola scontri singoli e doppi con moltiplicatori modificati e limite 2,4×.|PokéSurvivor attenua la tabella: debolezza 1,6×, resistenza 0,6× e immunità principale 0,3×. Per due tipi il prodotto resta tra 0,3× e 2,4×.|Le righe sono i tipi attaccanti, le colonne quelli difensori. Il risultato è solo il fattore tipo e non include meteo, attacco, difesa o effetti aggiuntivi.',
 'legendaries':'Leggendari di PokéSurvivor: varchi e rosa|Come funzionano i varchi e quali leggendari o misteriosi risultano nella versione registrata.|Un varco porta in un’arena separata contro un leggendario. La vittoria dà la ricompensa prevista, ma non aggiunge automaticamente il normale compagno alla collezione.|Entra con una via di fuga e osserva terreno e tipo. Non confondere l’incontro nel varco con l’idoneità al gacha regionale: la tabella è una rosa, non un calendario garantito.',
 'updates':'Aggiornamenti di PokéSurvivor: ricariche, coop e Arceus|Modifiche verificate fino al 15 ottobre 2026.|Il registro riassume le modifiche dello sviluppatore controllate nella versione indicata. Non presenta ogni voce come una prova indipendente in partita.|Un aggiornamento obbligatorio mostra un avviso di dieci secondi, termina la partita, registra le ricompense e ricarica. Qui trovi anche coop, recupero e Judgment of Arceus.',
 'arceus-judgment':'Guida ad Arceus: sopravvivi al Giudizio dei 30 minuti|Attacchi, rinforzi leggendari e obiettivi verificati del Judgment of Arceus.|A 30:00 la partita passa alle Ruins of Judgment. Nella versione ufficiale verificata Arceus è invincibile: devi schivare, sopravvivere e sconfiggere i rinforzi richiesti.|Prepara una via libera prima del minuto 28, reagisci prima agli indicatori di pericolo e concentra i danni su un rinforzo alla volta. Pilastri, raggi, onde d’urto e contatto richiedono spazio.',
 'upgrades':'Potenziamenti di PokéSurvivor: carte e priorità|Scegli quando privilegiare danno, movimento, difesa o requisiti di evoluzione.|Le carte modificano la partita corrente. Alcune statistiche sono anche requisiti di evoluzione, quindi una scelta anticipata può rendere disponibile più avanti la carta dorata.|Assicurati prima i requisiti delle mosse principali e non inseguire una formula universale. Spazio, schema d’attacco e obiettivo cambiano la priorità corretta.',
 'gacha-calculator':'Calcolatore gacha e pity di PokéSurvivor|Calcola probabilità base e verifica il pity rigido a 70 estrazioni.|Inserisci le estrazioni previste e il pity attuale. Il calcolo mostra probabilità base indipendenti e se raggiungi il pity rigido; non predice un Pokémon specifico.|Una probabilità cumulativa non garantisce il risultato prima del pity. Usa il dato per gestire le risorse e il Pokédex per controllare il pool regionale.',
 'search':'Cerca nella wiki di PokéSurvivor|Cerca guide, Pokémon e mosse nella wiki.|Trova una guida, un compagno o una mossa.|Prova il nome ufficiale del Pokémon o della mossa; puoi anche cercare termini come mobile, cooperativa o Arceus.'
}

_ZH = {
 '':'PokéSurvivor 維基：排行、配裝與攻略|獨立 PokéSurvivor 攻略站，收錄 966 隻寶可夢、強度排行、合法配裝、合作模式、進化與阿爾宙斯攻略。|依照已記錄的遊戲版本規劃下一局：挑選開局夥伴、核對進化條件、查詢屬性相剋，也避免把不同同人作品的資訊混在一起。|初次遊玩可先看新手入門；熟悉操作後，再比較完整名單，並在選擇強化卡前確認招式的進化需求。',
 'how-to-play':'PokéSurvivor 新手攻略：玩法與開局流程|從操作、升級選擇到第一次進化，掌握 PokéSurvivor 的基本玩法。|PokéSurvivor 是瀏覽器生存遊戲：移動角色、收集經驗並在升級時選擇強化。攻擊會自動施放，因此走位與安全距離特別重要。|先練習拉開距離並安全收集經驗，再把起始招式升到滿級、取得指定能力卡，最後在出現時選擇金色進化卡。',
 'mobile':'PokéSurvivor Android／iPhone 攻略：操作與疑難排解|手機版操作、加入主畫面與保存進度的注意事項。|手機可直接使用官方網站。以觸控操作時，遊戲中盡量不要切換分頁；若想像 App 一樣啟動，可把 PWA 加入主畫面。|存檔與目前的瀏覽器及使用者設定檔綁定。清除資料、換機或使用無痕模式前，請在遊戲支援時先綁定帳號，並保留重要資訊。',
 'builds':'PokéSurvivor 配裝攻略：招式與進化規劃器|用開局夥伴、相容副招式與進化需求安排合法配裝。|實用配裝應從夥伴真正的起始招式出發，再加入與其屬性相容的副招式。規劃器不會讀取或修改你的遊戲存檔。|先選自己能駕馭的攻擊方式，保留兩個招式所需的能力卡，再在傷害、移動與生存之間取捨，最後用自己的實戰確認手感。',
 'download':'PokéSurvivor 下載方式：網頁版、PWA 與 APK|官方遊玩入口、PWA 安裝方式，以及第三方 APK 的檢查重點。|本站記錄的版本在 pokesurvivor.com 瀏覽器中執行，也能以 PWA 加入主畫面；遊玩官方版本不需要付費下載。|遇到第三方 APK 或移植版時，先確認發布者、權限與版本。名稱相近不代表內容、存檔機制或更新進度相同。',
 'co-op':'PokéSurvivor 合作模式：房間、邀請與排解方法|建立房間、邀請朋友並處理常見連線問題。|由一位玩家建立房間並分享代碼，另一位使用相同遊戲版本加入。不要公開帳號憑證或個人資料。|無法加入時，雙方先重新載入最新版本、檢查網路，再建立新房間。版本不同或連線階段逾時，通常比反覆輸入舊代碼更值得先排查。',
 'survivor-vs-burst':'PokéSurvivor 與 Pokémon Survivor Burst 差異|先辨認遊戲版本，再使用正確攻略。|兩者是不同作品。本站記錄 JPTER78 的瀏覽器版 PokéSurvivor；Burst 的截圖、APK 或機制不能證明此版本也有相同內容。|請核對網址、開發者與模式名稱。若阿爾宙斯、下載方式或規則不同，應查找目前開啟之作品的專用攻略。',
 'about':'關於本站與編輯方法|說明資料、建議與媒體素材的核對方式。|本站是獨立攻略站。數值與條件來自可辨識版本的公開程式碼；編輯建議會清楚標示判斷依據，不會假稱已完成不存在的實測。|為了可追溯性，必要的內部名稱會保留，並標示核對版本；遊戲畫面與說明圖也會明確區分。',
 'privacy':'隱私權與本機工具|說明本站使用的資料、選用分析與瀏覽器內計算。|搜尋、篩選和計算器都在瀏覽器中運作，不會讀取遊戲存檔，也不會要求遊戲帳號密碼。|分析功能依你的偏好啟用，可由頁尾重新調整。請勿在搜尋欄或分享連結中輸入房間代碼、電子郵件或其他個人資料。',
 'pokedex':'PokéSurvivor 寶可夢圖鑑：能力與取得方式|依名稱或屬性搜尋 966 名夥伴，比較 HP、速度、攻擊與取得分類。|本圖鑑收錄記錄版本中的 966 名可用夥伴；這些是 PokéSurvivor 遊戲數值，不等於寶可夢本傳的對戰能力。|可依名稱或編號搜尋並搭配屬性篩選。取得欄會區分地區扭蛋、開局可選與扭蛋池外夥伴。',
 'moves':'PokéSurvivor 招式表：傷害、型態與進化|查詢 64 種招式的基礎傷害、冷卻、攻擊型態、最高等級與進化。|評估招式時要同時看運作方式和數值。等級一的傷害與冷卻不是完整 DPS，因為射程、持續時間和命中頻率都不同。|先挑選能配合自己走位的攻擊型態，再查看對應進化，並在同一局保留正確的能力卡。',
 'move-evolutions':'PokéSurvivor 招式進化與條件檢查器|查詢 59 種招式進化所需等級與能力卡。|把招式升到最高等級，在同一局取得指定能力卡，並於金色卡出現時選取。達成條件只代表可以進化，不會自動完成。|金色卡未出現時，先核對等級與精確條件。其他永久強化不能代替本局能力卡，沒有進化的增益招式也無法轉化。',
 'starters':'PokéSurvivor 開局夥伴：29 種選擇比較|比較 29 名開局夥伴的起始招式、HP、速度、攻擊與進化需求。|性格測驗會推薦夥伴，但你可以拒絕。請優先挑選自己能掌握的攻擊型態，並確認它需要哪張能力卡才能進化。|相同屬性的夥伴不一定擁有相同起始招式；除了攻擊倍率，也要比較射程、機動性與進化條件。',
 'starter-tier-list':'PokéSurvivor 開局夥伴強度排行|以透明能力分數比較 29 名開局夥伴、起始招式與進化需求。|分數以 HP、速度與攻擊比較開局能力，不代表勝率、生存時間，也不是官方排行。|把階級當成第一層篩選即可。招式型態、射程、天氣與操作習慣，都可能讓低分夥伴更適合你。',
 'tier-list':'PokéSurvivor 強度排行：966 隻寶可夢完整名單|以可重現的開局能力分數搜尋及排序 966 名夥伴。|排行使用程式碼中的能力值：HP 35%、速度 25%、攻擊 40%，並以全名單最高值正規化；本站沒有聲稱完成 966 次實測。|先依需要的屬性篩選，再查看可用招式與進化條件後安排配裝。若要選開局夥伴，也請搭配 29 名專屬排行。',
 'types':'PokéSurvivor 屬性相剋表與傷害計算器|計算單屬性、雙屬性相剋，以及 2.4× 上限。|PokéSurvivor 調整了常見倍率：弱點 1.6×、抗性 0.6×、本傳無效關係為 0.3×；雙屬性乘積限制在 0.3× 至 2.4×。|表格列是攻擊屬性、欄是防守屬性。結果只代表屬性倍率，不包含天氣、夥伴攻擊、防禦強化或其他效果。',
 'legendaries':'PokéSurvivor 傳說寶可夢：裂隙與名單|了解裂隙遭遇，以及版本中標記的傳說與幻之寶可夢。|裂隙會把玩家帶到獨立場地挑戰傳說寶可夢。勝利可獲得指定獎勵，但不會自動把一般夥伴加入收藏。|進入前保留退路並觀察地形與屬性。裂隙遭遇和地區扭蛋資格是兩回事；表格是名單，不是保證出現的時間表。',
 'updates':'PokéSurvivor 更新紀錄：重載、合作與阿爾宙斯|已核對至 2026 年 10 月 15 日的開發者更新。|本頁整理開發者公布、並由指定版本核對的變更，不會把每一條更新都描述成獨立實戰測試。|強制更新會先顯示十秒提示，結束本局、儲存已記錄獎勵並重新載入。此處也收錄合作模式、帳號恢復與阿爾宙斯審判相關變動。',
 'arceus-judgment':'阿爾宙斯攻略：撐過 30 分鐘審判|整理 Judgment of Arceus 的攻擊、傳說增援與已核對成就。|30:00 時場景會轉入 Ruins of Judgment。經核對的官方瀏覽器版中，阿爾宙斯無法擊敗；目標是閃避、生存並擊倒成就所需的增援。|28 分鐘前先保留清楚移動路線，優先避開警示區，再集中火力處理單一增援。光柱、光束、衝擊波與接觸傷害都要求玩家留出空間。',
 'upgrades':'PokéSurvivor 強化卡：效果與選擇優先度|判斷何時優先傷害、移動、防禦或進化所需能力。|強化卡只影響目前這一局；部分能力同時是招式進化條件，因此早期選擇會決定後續能否遇到金色進化卡。|先確保主力招式的必要條件，不要套用唯一固定公式。地圖空間、攻擊型態與本局目標不同，正確優先度也會改變。',
 'gacha-calculator':'PokéSurvivor 扭蛋與保底計算器|計算基礎機率，並確認抽數是否涵蓋 70 抽硬保底。|輸入預計抽數與目前保底進度。工具會顯示獨立基礎機率及本次範圍是否碰到硬保底，不會預測特定寶可夢。|累積機率不代表在保底前一定抽中。可用結果安排資源，再到圖鑑確認各夥伴是否屬於目前地區扭蛋池。',
 'search':'搜尋 PokéSurvivor 維基|搜尋本站攻略、寶可夢與招式。|尋找攻略、夥伴或招式。|建議輸入寶可夢或招式的遊戲內正式名稱，也可搜尋手機、合作或阿爾宙斯等主題。'
}

for slug, value in _IT.items(): PAGES['it'][slug] = tuple(value.split('|'))
for slug, value in _ZH.items(): PAGES['zh-hant'][slug] = tuple(value.split('|'))

PAGES['es']['save-recovery'] = ('Recuperar el guardado de PokéSurvivor: lista segura','Pasos seguros para progreso perdido, vinculación con Google, errores 409 y el aviso de protección del progreso.','Detente antes de borrar datos, desinstalar la PWA o cambiar la única copia que todavía muestra tu progreso. Esta guía no lee, sube ni repara guardados.','Conserva intacto cualquier navegador que aún muestre la partida. Anota solo datos no sensibles y usa la cuenta de Google vinculada cuando corresponda; no compartas contraseñas, tokens, correos, códigos de sala ni archivos de guardado.')
PAGES['it']['save-recovery'] = ('Recupero salvataggio PokéSurvivor: procedura sicura','Passaggi sicuri per progressi mancanti, collegamento Google, errori 409 e pausa di protezione.','Fermati prima di cancellare dati, disinstallare la PWA o modificare l’unica copia che mostra ancora i progressi. Questa guida non legge, carica o ripara salvataggi.','Conserva intatto ogni browser che mostra ancora la partita. Annota solo dati non sensibili e usa l’account Google collegato quando applicabile; non condividere password, token, email, codici stanza o file di salvataggio.')
PAGES['zh-hant']['save-recovery'] = ('PokéSurvivor 存檔救援：安全檢查清單','處理進度消失、Google 綁定、409 錯誤與保護進度暫停訊息的安全步驟。','清除資料、移除 PWA 或更動唯一仍顯示進度的副本前，請先停下來。本站不會讀取、上傳或修復存檔。','保留仍能看到進度的瀏覽器與設定檔，只記錄不敏感資訊；已綁定時使用同一 Google 帳號。請勿分享密碼、權杖、電子郵件、房間代碼或存檔檔案。')

# V3 copy: localized around the October 18 mechanics, reviewed 2026-10-19.
PAGES['es'].update({
 'pokedex':('Pokédex de PokéSurvivor: ataque, ataque especial y defensas','Busca 966 compañeros y compara PS, velocidad, Ataque, Ataque Especial, Defensa y Defensa Especial.','La actualización del 18 de octubre separa las cuatro estadísticas de combate. Estos valores pertenecen a PokéSurvivor, no al combate de la saga principal.','Compara primero la categoría del movimiento: un ataque especial usa Ataque Especial y uno físico usa Ataque. Usa ambas defensas para valorar la resistencia.'),
 'moves':('Movimientos de PokéSurvivor: físicos, especiales y mejoras','Consulta 65 movimientos por tipo, patrón, categoría, daño, enfriamiento y evolución.','Los movimientos físicos usan Ataque y los especiales Ataque Especial. Tóxico es especial y Púas físico en este juego; Maquinación es Normal y mejora el Ataque Especial.','No apliques por costumbre la categoría de otros juegos. Comprueba la tabla y combina el movimiento con el mejor lado ofensivo de tu compañero.'),
 'builds':('Builds de PokéSurvivor: planificador físico y especial','Crea una ruta compatible y comprueba qué estadística usa cada movimiento.','Una build válida parte del movimiento inicial real. Danza Espada y Danza Dragón mejoran el Ataque físico; Maquinación mejora el Ataque Especial y pertenece a la reserva Normal compartida.','El requisito de evolución y la estadística de daño son reglas distintas. Conserva los parámetros p y m del enlace compartido al editar una ruta.'),
 'tier-list':('Tier list de PokéSurvivor: 966 perfiles de cuatro dimensiones','Clasificación reproducible por PS, velocidad, mejor lado ofensivo y defensas equilibradas.','Cada perfil promedia cuatro percentiles: PS, velocidad, el mejor valor entre Ataque y Ataque Especial, y la media de ambas defensas. No representa victorias ni pruebas inventadas.','Las bandas tienen población definida: S 10 %, A 20 %, B 30 % y C 40 %. Después revisa la categoría de los movimientos y la evolución.'),
 'starter-tier-list':('Clasificación de los 29 iniciales de PokéSurvivor','Compara percentiles de PS, velocidad, ataque físico/especial y defensas.','El perfil usa cuatro dimensiones del grupo de 29 iniciales. Las bandas por posición evitan grupos vacíos y no pretenden medir victorias.','Comprueba también la categoría del movimiento inicial: una cifra ofensiva alta solo sirve al lado correcto.'),
 'mobile':('PokéSurvivor en móvil: táctil, mando y apuntado manual','Configura controles táctiles o mando y el apuntado manual opcional.','El juego funciona en el navegador móvil. La versión del 18 de octubre admite la mayoría de mandos USB o Bluetooth; esto no significa que exista una versión nativa para Nintendo Switch.','Configura el mando en Ajustes → Controles. Activa Apuntar a mano en Ajustes → Accesibilidad solo si quieres dirigir ataques con ratón o stick derecho.'),
 'updates':('Actualización de PokéSurvivor del 18 de octubre','Ataque físico/especial, mando, guardado y cambios de Arceus verificados.','El changelog oficial lleva fecha 18 de octubre; el commit central corresponde al 19 de octubre a las 05:35 en Pekín. La guía mantiene ambas fechas sin confundirlas.','Revisa las nuevas estadísticas, Maquinación, el guardado cada diez minutos, el botón Guardar y la nueva curva de presión de Arceus.'),
 'arceus-judgment':('Guía de Arceus: cronología de los minutos 30–40','Tope suave de velocidad, veneno, aceleración y daño de contacto verificados.','El Juicio empieza en 30:00 y Arceus sigue siendo invencible. Hacia 35:00 acelera sin parar; desde alrededor de 37:00 aumenta el daño de contacto y hacia 40:00 puede derrotar de un golpe.','El minuto 40 no es un final automático. Mantén una ruta abierta, no dependas solo de velocidad excesiva y considera la menor escala del veneno contra enemigos de muchísima vida.')})
PAGES['it'].update({
 'pokedex':('Pokédex di PokéSurvivor: attacco, attacco speciale e difese','Cerca 966 compagni e confronta PS, velocità, Attacco, Attacco Speciale, Difesa e Difesa Speciale.','L’aggiornamento del 18 ottobre separa le quattro statistiche di combattimento. Sono valori di PokéSurvivor, non della serie principale.','Controlla la categoria della mossa: le mosse speciali usano l’Attacco Speciale, quelle fisiche l’Attacco. Valuta entrambe le difese.'),
 'moves':('Mosse di PokéSurvivor: fisiche, speciali e bonus','Consulta 65 mosse per tipo, schema, categoria, danno, ricarica ed evoluzione.','Le mosse fisiche usano l’Attacco e quelle speciali l’Attacco Speciale. Tossina è speciale e Punte fisica in questo gioco; Congiura è Normale e aumenta l’Attacco Speciale.','Non trasferire automaticamente le categorie di altri giochi. Abbina ogni mossa al lato offensivo migliore del compagno.'),
 'builds':('Build di PokéSurvivor: pianificatore fisico e speciale','Crea un percorso compatibile e verifica la statistica usata da ogni mossa.','Una build valida parte dalla vera mossa iniziale. Danzaspada e Dragodanza aumentano l’Attacco fisico; Congiura aumenta l’Attacco Speciale ed è nel pool Normale condiviso.','Il requisito di evoluzione e la statistica del danno sono regole separate. Mantieni i parametri p e m quando modifichi un link condiviso.'),
 'tier-list':('Tier list di PokéSurvivor: 966 profili in quattro dimensioni','Classifica riproducibile con PS, velocità, lato offensivo migliore e difese bilanciate.','Il profilo media quattro percentili: PS, velocità, il valore migliore tra Attacco e Attacco Speciale e la media delle due difese. Non misura vittorie.','Le fasce hanno dimensioni definite: S 10%, A 20%, B 30% e C 40%. Poi controlla categoria ed evoluzione delle mosse.'),
 'starter-tier-list':('Classifica dei 29 iniziali di PokéSurvivor','Percentili di PS, velocità, attacco fisico/speciale e difese.','Il profilo usa quattro dimensioni dei 29 iniziali. Le fasce per posizione evitano gruppi vuoti e non dichiarano prove di vittoria.','Controlla anche la categoria della mossa iniziale: un valore offensivo alto aiuta solo il lato corretto.'),
 'mobile':('PokéSurvivor mobile: touch, controller e mira manuale','Configura touch o controller e la mira manuale facoltativa.','Il gioco gira nel browser mobile. La versione del 18 ottobre supporta la maggior parte dei controller USB o Bluetooth; non è una versione nativa per Nintendo Switch.','Configura il controller in Impostazioni → Controlli. Attiva Mira manuale in Impostazioni → Accessibilità per usare mouse o levetta destra.'),
 'updates':('Aggiornamento PokéSurvivor del 18 ottobre','Statistiche fisiche/speciali, controller, salvataggio e modifiche ad Arceus.','Il changelog ufficiale è del 18 ottobre; il commit principale corrisponde al 19 ottobre alle 05:35 a Pechino. Le due date indicano eventi diversi.','Verifica nuove statistiche, Congiura, salvataggio automatico ogni dieci minuti, pulsante Salva e nuova pressione di Arceus.'),
 'arceus-judgment':('Guida ad Arceus: cronologia dei minuti 30–40','Limite morbido alla velocità, veleno, accelerazione e danno da contatto verificati.','Il Giudizio inizia a 30:00 e Arceus resta invincibile. Verso 35:00 accelera continuamente, da circa 37:00 cresce il danno da contatto e verso 40:00 può mandarti KO in un colpo.','Il minuto 40 non è una fine automatica. Mantieni libera una via di fuga e non affidarti solo alla velocità oltre il limite morbido.')})
PAGES['zh-hant'].update({
 'pokedex':('PokéSurvivor 圖鑑：攻擊、特攻與雙防','搜尋 966 名夥伴，比較 HP、速度、攻擊、特攻、防禦與特防。','10 月 18 日更新後，攻擊、特攻、防禦與特防已拆分；這些是 PokéSurvivor 的數值。','先查招式分類：物理招式使用攻擊，特殊招式使用特攻；生存能力則要同時看雙防。'),
 'moves':('PokéSurvivor 招式表：物理、特殊與增益','依屬性、型態、分類、傷害、冷卻與進化查詢 65 種招式。','物理招式看攻擊，特殊招式看特攻。本遊戲的劇毒為特殊、撒菱為物理；詭計屬於共用的一般屬性招式，提升特攻。','不要直接套用其他作品的分類；請以表格為準，並將招式配給正確的輸出側。'),
 'builds':('PokéSurvivor 配裝：物理／特殊路線規劃','建立相容路線，並檢查每種招式使用的能力。','合法配裝從真實起始招式開始。劍舞與龍之舞只提升物理攻擊；詭計提升特攻，且屬於共用一般屬性池。','進化需求與傷害縮放是不同規則。編輯分享路線時保留 p 與 m 參數。'),
 'tier-list':('PokéSurvivor 強度排行：966 名夥伴四維評分','以 HP、速度、最佳輸出側與均衡雙防建立可重現排名。','評分平均四個百分位：HP、速度、攻擊／特攻較高者、雙防平均。這不是勝率或虛構實測。','S、A、B、C 分別佔 10%、20%、30%、40%，再搭配招式分類與進化路線判斷。'),
 'starter-tier-list':('PokéSurvivor 29 名開局夥伴排行','比較 HP、速度、物理／特殊輸出與雙防百分位。','評分以 29 名開局夥伴的四維百分位計算，分組依名次切分，不會出現空白階級。','同時檢查起始招式分類；高輸出能力只會強化對應的物理或特殊側。'),
 'mobile':('PokéSurvivor 手機版：觸控、手把與手動瞄準','設定觸控或手把，並按需開啟手動瞄準。','遊戲在手機瀏覽器運作。10 月 18 日版本支援多數 USB 或藍牙手把；這不代表有 Nintendo Switch 原生版。','至「設定 → 控制」設定手把；若要以滑鼠或右類比擇瞄準，再至「設定 → 輔助使用」開啟手動瞄準。'),
 'updates':('PokéSurvivor 10 月 18 日更新','已核對物理／特殊、手把、儲存與阿爾宙斯變更。','官方更新日誌標記 10 月 18 日；核心提交對應北京時間 10 月 19 日 05:35。兩個日期代表不同事件。','重點包括四項戰鬥能力、詭計、10 分鐘自動儲存、儲存按鈕與新的阿爾宙斯壓力曲線。'),
 'arceus-judgment':('阿爾宙斯攻略：30–40 分鐘壓力時間軸','已核對速度軟上限、中毒縮放、加速與接觸傷害。','30:00 開始審判，阿爾宙斯仍無法擊敗。約 35:00 起持續加速，約 37:00 起接觸傷害增加，約 40:00 可能一擊倒下。','40 分鐘不是固定結束點。保留逃生路線，別只依賴超過軟上限的速度，並留意高 HP 敌人的中毒效果會降低。')})


TYPE_NAMES = {
 'es': {'normal':'Normal','fire':'Fuego','water':'Agua','electric':'Eléctrico','grass':'Planta','ice':'Hielo','fighting':'Lucha','poison':'Veneno','ground':'Tierra','flying':'Volador','psychic':'Psíquico','bug':'Bicho','rock':'Roca','ghost':'Fantasma','dragon':'Dragón','dark':'Siniestro','steel':'Acero','fairy':'Hada'},
 'it': {'normal':'Normale','fire':'Fuoco','water':'Acqua','electric':'Elettro','grass':'Erba','ice':'Ghiaccio','fighting':'Lotta','poison':'Veleno','ground':'Terra','flying':'Volante','psychic':'Psico','bug':'Coleottero','rock':'Roccia','ghost':'Spettro','dragon':'Drago','dark':'Buio','steel':'Acciaio','fairy':'Folletto'},
 'zh-hant': {'normal':'一般','fire':'火','water':'水','electric':'電','grass':'草','ice':'冰','fighting':'格鬥','poison':'毒','ground':'地面','flying':'飛行','psychic':'超能力','bug':'蟲','rock':'岩石','ghost':'幽靈','dragon':'龍','dark':'惡','steel':'鋼','fairy':'妖精'}
}

HEADERS = {
 'es': {'No.':'N.º','Pokémon':'Pokémon','Partner':'Compañero','Type':'Tipo','HP':'PS','Speed':'Velocidad','Attack':'Ataque','Sp. Atk':'At. Esp.','Defense':'Defensa','Sp. Def':'Def. Esp.','Category':'Categoría','Buff stat':'Mejora','Profile':'Perfil','Gen':'Gen.','Collection':'Obtención','Move':'Movimiento','Pattern':'Patrón','Base damage':'Daño base','Cooldown':'Enfriamiento','Max level':'Nivel máx.','Evolution':'Evolución','Required level':'Nivel requerido','Required stat card':'Carta requerida','Evolves into':'Evoluciona a','Starting move':'Movimiento inicial','Evolution stat':'Carta de evolución','Band':'Banda','Score':'Puntuación','Attack / defend':'Ataque / defensa'},
 'it': {'No.':'N.','Pokémon':'Pokémon','Partner':'Compagno','Type':'Tipo','HP':'PS','Speed':'Velocità','Attack':'Attacco','Sp. Atk':'Att. Sp.','Defense':'Difesa','Sp. Def':'Dif. Sp.','Category':'Categoria','Buff stat':'Bonus','Profile':'Profilo','Gen':'Gen.','Collection':'Ottenimento','Move':'Mossa','Pattern':'Schema','Base damage':'Danno base','Cooldown':'Ricarica','Max level':'Livello max','Evolution':'Evoluzione','Required level':'Livello richiesto','Required stat card':'Carta richiesta','Evolves into':'Evolve in','Starting move':'Mossa iniziale','Evolution stat':'Carta evoluzione','Band':'Fascia','Score':'Punteggio','Attack / defend':'Attacco / difesa'},
 'zh-hant': {'No.':'編號','Pokémon':'寶可夢','Partner':'夥伴','Type':'屬性','HP':'HP','Speed':'速度','Attack':'攻擊','Sp. Atk':'特攻','Defense':'防禦','Sp. Def':'特防','Category':'分類','Buff stat':'增益能力','Profile':'綜合評分','Gen':'世代','Collection':'取得方式','Move':'招式','Pattern':'型態','Base damage':'基礎傷害','Cooldown':'冷卻','Max level':'最高等級','Evolution':'進化','Required level':'所需等級','Required stat card':'所需能力卡','Evolves into':'進化為','Starting move':'起始招式','Evolution stat':'進化能力','Band':'階級','Score':'分數','Attack / defend':'攻擊／防守'}
}
HEADERS['es']['Attack / Sp. Atk'] = 'Ataque / At. Esp.'
HEADERS['it']['Attack / Sp. Atk'] = 'Attacco / Att. Sp.'
HEADERS['zh-hant']['Attack / Sp. Atk'] = '攻擊／特攻'


JS = {
 'es': {'entries':'{count} de {total} registros','starterPartner':'Compañero inicial','levelRequirement':'Nivel {level} + {requirement} en esta partida; después elige la carta dorada.','loadingEvolution':'Cargando requisitos…','noEvolution':'{move} no tiene evolución en esta versión.','invalidLevel':'Introduce un nivel entero del 1 al {max}.','reachLevel':'alcanza el nivel {level}','takeStat':'toma {stat} en esta partida','eligible':'Puedes evolucionar a {evolution}. Elige la carta dorada cuando aparezca; no sucede automáticamente.','loadFail':'No se pudo cargar el comprobador. Usa la tabla o vuelve a intentarlo.','loadingTypes':'Cargando reglas de tipos…','damage':'{attack} → {defense}: {mult}× de daño','typeFail':'No se pudo cargar la calculadora. Usa la tabla inferior.','searchHint':'Prueba un Pokémon, un movimiento o una consulta como móvil.','searching':'Buscando…','results':'{count} resultados.','noResults':'Sin resultados. Prueba un nombre más corto o usa la navegación.','searchFail':'No se pudo cargar la búsqueda. Vuelve a intentarlo o navega por las guías.','linkCopied':'Enlace copiado','copyLink':'Copiar enlace','gachaInvalid':'Introduce entre 1 y 1000 tiradas y un pity actual entre 0 y 69.','gachaSummary':'Probabilidad base de al menos una rareza 5: {five} %. Probabilidad base de al menos una tirada con opción shiny: {shiny} %.','pityReach':'Esta ventana alcanza el pity duro de 70 en un máximo de {pulls} tiradas.','pityRemain':'El pity duro no está garantizado en esta ventana; faltan {pulls} tiradas.'},
 'it': {'entries':'{count} di {total} voci','starterPartner':'Compagno iniziale','levelRequirement':'Livello {level} + {requirement} in questa partita, poi scegli la carta dorata.','loadingEvolution':'Caricamento requisiti…','noEvolution':'{move} non ha un’evoluzione in questa versione.','invalidLevel':'Inserisci un livello intero da 1 a {max}.','reachLevel':'raggiungi il livello {level}','takeStat':'prendi {stat} in questa partita','eligible':'Puoi evolvere in {evolution}. Scegli la carta dorata quando appare; non avviene automaticamente.','loadFail':'Impossibile caricare il controllo. Usa la tabella o riprova.','loadingTypes':'Caricamento regole dei tipi…','damage':'{attack} → {defense}: danno {mult}×','typeFail':'Impossibile caricare il calcolatore. Usa la tabella qui sotto.','searchHint':'Prova un Pokémon, una mossa o un termine come mobile.','searching':'Ricerca…','results':'{count} risultati.','noResults':'Nessun risultato. Prova un nome più breve o usa la navigazione.','searchFail':'Ricerca non disponibile. Riprova o consulta guide e database.','linkCopied':'Link copiato','copyLink':'Copia link','gachaInvalid':'Inserisci 1–1000 estrazioni e un pity attuale tra 0 e 69.','gachaSummary':'Probabilità base di almeno una rarità 5: {five}%. Probabilità base di almeno un tiro idoneo shiny: {shiny}%.','pityReach':'Questa finestra raggiunge il pity rigido a 70 entro {pulls} estrazioni.','pityRemain':'Il pity rigido non è garantito in questa finestra; mancano {pulls} estrazioni.'},
 'zh-hant': {'entries':'顯示 {count}／{total} 筆','starterPartner':'開局夥伴','levelRequirement':'本局將招式升至 {level} 級並取得 {requirement}，再選擇金色卡。','loadingEvolution':'正在載入進化條件…','noEvolution':'此版本中的 {move} 沒有招式進化。','invalidLevel':'請輸入 1 至 {max} 的整數等級。','reachLevel':'升至 {level} 級','takeStat':'本局取得 {stat}','eligible':'可進化為 {evolution}。出現金色進化卡時仍需手動選擇。','loadFail':'無法載入檢查器，請使用下方表格或重新載入。','loadingTypes':'正在載入屬性規則…','damage':'{attack} → {defense}：{mult}× 傷害','typeFail':'無法載入計算器，請使用下方單屬性表。','searchHint':'可輸入寶可夢、招式，或「手機」等主題。','searching':'搜尋中…','results':'找到 {count} 筆結果。','noResults':'找不到結果，請縮短名稱或使用導覽。','searchFail':'無法載入搜尋，請重試或瀏覽攻略與資料庫。','linkCopied':'連結已複製','copyLink':'複製分享連結','gachaInvalid':'請輸入 1–1000 抽，且目前保底進度須為 0–69。','gachaSummary':'至少一次五星的基礎機率：{five}%；至少一次可出現異色判定的基礎機率：{shiny}%。','pityReach':'本次範圍會在最多 {pulls} 抽內觸發 70 抽硬保底。','pityRemain':'本次範圍不保證觸發硬保底；依目前進度尚差 {pulls} 抽。'}
}

JS['es'].update({'moveEvolution':'{move} → {evolution}: nivel {level} + {requirement}','moveNoEvolution':'{move}: sin evolución en esta versión','buildSummary':'{partner} empieza con {primary}. Ruta secundaria: {secondary}. Reserva compatible: tipos {types} y movimientos Normal.','plannerFail':'No se pudo cargar el planificador. Usa las rutas y la tabla de evoluciones.','copyFail':'El navegador bloqueó la copia; usa la URL de la barra de direcciones.'})
JS['it'].update({'moveEvolution':'{move} → {evolution}: livello {level} + {requirement}','moveNoEvolution':'{move}: nessuna evoluzione in questa versione','buildSummary':'{partner} inizia con {primary}. Percorso secondario: {secondary}. Pool compatibile: tipi {types} e mosse Normale.','plannerFail':'Impossibile caricare il pianificatore. Usa i percorsi e la tabella evoluzioni.','copyFail':'Il browser ha bloccato la copia; usa l’URL nella barra degli indirizzi.'})
JS['zh-hant'].update({'moveEvolution':'{move} → {evolution}：{level} 級 + {requirement}','moveNoEvolution':'{move}：此版本無進化','buildSummary':'{partner} 的起始路線為 {primary}。副招式路線：{secondary}。相容範圍：{types} 屬性與一般屬性招式。','plannerFail':'無法載入規劃器，請使用路線說明與進化表。','copyFail':'瀏覽器封鎖複製；請使用網址列中的連結。'})
JS['es'].update({'savePreserve':'Conserva ese navegador y perfil. No borres los datos ni desinstales la PWA. Vincula la cuenta solo desde el juego oficial si es seguro hacerlo.','saveLinked':'En el dominio oficial, usa Iniciar sesión con Google con el mismo Gmail vinculado. Si falta el progreso, contacta al desarrollador con este informe sin datos privados.','saveGuest':'La recuperación de un invitado no vinculado es incierta. Conserva el navegador y perfil originales y contacta al desarrollador; no confíes en sitios que pidan credenciales o el guardado.','saveUnknown':'La recuperación es incierta. Conserva los datos restantes y contacta al desarrollador antes de hacer cambios destructivos.','reportCopied':'Informe copiado','copyReport':'Copiar informe','reportCopyFail':'El navegador bloqueó la copia. Selecciona el texto y cópialo manualmente.'})
JS['it'].update({'savePreserve':'Conserva quel browser e profilo. Non cancellare i dati e non disinstallare la PWA. Collega l’account solo dal gioco ufficiale se è sicuro farlo.','saveLinked':'Sul dominio ufficiale, usa Accedi con Google con lo stesso Gmail collegato. Se i progressi mancano, contatta lo sviluppatore con questo rapporto non sensibile.','saveGuest':'Il recupero di un ospite non collegato è incerto. Conserva browser e profilo originali e contatta lo sviluppatore; non fidarti di siti che chiedono credenziali o salvataggi.','saveUnknown':'Il recupero è incerto. Conserva i dati rimasti e contatta lo sviluppatore prima di modifiche distruttive.','reportCopied':'Rapporto copiato','copyReport':'Copia rapporto','reportCopyFail':'Il browser ha bloccato la copia. Seleziona il testo e copialo manualmente.'})
JS['zh-hant'].update({'savePreserve':'保留該瀏覽器與設定檔，不要清除網站資料或移除 PWA。只有在安全時，才透過官方遊戲綁定帳號。','saveLinked':'在官方網域使用同一個已綁定 Gmail 登入。進度仍消失時，請以這份不含私密資料的報告聯絡開發者。','saveGuest':'未綁定訪客的救援結果不確定。請保留原瀏覽器與設定檔並聯絡開發者；不要信任要求帳密或上傳存檔的網站。','saveUnknown':'救援結果不確定。進行破壞性變更前，先保留現存瀏覽器資料並以不敏感資訊聯絡開發者。','reportCopied':'報告已複製','copyReport':'複製報告','reportCopyFail':'瀏覽器封鎖複製；請手動選取報告文字。'})
for _locale in ('es','it','zh-hant'): JS[_locale]['typeNames']=TYPE_NAMES[_locale]


def url(locale: str, slug: str) -> str:
    tail = (slug + '/') if slug else ''
    return '/' + tail if locale == 'en' else f'/{locale}/' + tail


HOME_TEXT = {
 'Atk / Sp. Atk':('Atq. / At. Esp.','Att. / Att. Sp.','攻擊／特攻'),
 'tiers, builds & guides.':('clasificaciones, builds y guías.','classifiche, build e guide.','排行、配裝與攻略'),
 'Your independent Pokémon Survivor Wiki for the 966-partner Pokédex, tier lists, legal builds, co-op fixes and Judgment of Arceus.':('Tu wiki independiente de Pokémon Survivor: Pokédex de 966 compañeros, clasificaciones, builds legales, cooperativo y Judgment of Arceus.','La wiki indipendente di Pokémon Survivor con 966 compagni, classifiche, build valide, coop e Judgment of Arceus.','獨立 Pokémon Survivor 攻略站：收錄 966 名夥伴、強度排行、合法配裝、合作模式與阿爾宙斯審判。'),
 'Search Pokémon, moves and guides':('Buscar Pokémon, movimientos y guías','Cerca Pokémon, mosse e guide','搜尋寶可夢、招式與攻略'),
 'Pokémon, moves, or a question…':('Pokémon, movimientos o una pregunta…','Pokémon, mosse o una domanda…','輸入寶可夢、招式或問題…'),
 'Explore the full tier list':('Ver la clasificación completa','Apri la classifica completa','查看完整強度排行'),
 'Survive Arceus':('Sobrevive a Arceus','Sopravvivi ad Arceus','挑戰阿爾宙斯'),
 'Independent guide for JPTER78’s browser game. No game login, download charge or in-game purchase is offered here.':('Guía independiente del juego para navegador de JPTER78. Aquí no se cobra por descargar, iniciar sesión ni comprar dentro del juego.','Guida indipendente al gioco per browser di JPTER78. Qui non vengono offerti accessi, download a pagamento o acquisti nel gioco.','JPTER78 瀏覽器遊戲的獨立攻略站；本站不提供遊戲登入、付費下載或遊戲內購買。'),
 'Your opening move':('Tu movimiento inicial','La tua mossa iniziale','你的起始招式'),
 'All 29 starters':('Los 29 iniciales','Tutti i 29 iniziali','全部 29 名開局夥伴'),
 'Preview a starting partner':('Vista previa de un compañero inicial','Anteprima di un compagno iniziale','預覽開局夥伴'),
 'Fire · Starter partner':('Fuego · Compañero inicial','Fuoco · Compagno iniziale','火 · 開局夥伴'),
 'Movement':('Movimiento','Movimento','移動'),
 'Starting move':('Movimiento inicial','Mossa iniziale','起始招式'),
 'Evolution':('Evolución','Evoluzione','進化'),
 'Level 5 + Power in this run, then choose the golden card.':('Nivel 5 + Power en esta partida; después elige la carta dorada.','Livello 5 + Power in questa partita, poi scegli la carta dorata.','本局升至 5 級並取得 Power，再選擇金色卡。'),
 'Plan this evolution':('Planificar esta evolución','Pianifica questa evoluzione','規劃這次進化'),
 'Preview shows Charmander. Compare every option in the starter guide.':('La vista previa muestra a Charmander. Compara todas las opciones en la guía de iniciales.','L’anteprima mostra Charmander. Confronta ogni scelta nella guida agli iniziali.','預覽目前顯示 Charmander；請至開局夥伴攻略比較全部選項。'),
 'partners':('compañeros','compagni','名夥伴'),
 'definitions':('definiciones','definizioni','種定義'),
 'conditions':('condiciones','condizioni','項條件'),
 'Play the developer’s game':('Jugar al juego del desarrollador','Gioca al titolo dello sviluppatore','前往開發者遊戲'),
 'What’s stopping<br>your next run?':('¿Qué frena<br>tu próxima partida?','Cosa blocca<br>la prossima partita?','下一局卡在<br>哪個環節？'),
 'Choose the problem. Find your next step.':('Elige el problema y encuentra el siguiente paso.','Scegli il problema e trova il passo successivo.','選擇目前問題，找到下一步。'),
 'Explore starter builds':('Ver builds iniciales','Esplora le build iniziali','查看開局配裝'),
 'Survive Judgment of Arceus':('Sobrevive al Judgment of Arceus','Sopravvivi al Judgment of Arceus','撐過阿爾宙斯審判'),
 '30-minute trigger, attacks and achievements.':('Inicio a los 30 minutos, ataques y logros.','Inizio al minuto 30, attacchi e obiettivi.','30 分鐘觸發、攻擊模式與成就。'),
 'Fix co-op and invites':('Soluciona el cooperativo y las invitaciones','Risolvi coop e inviti','排解合作與邀請問題'),
 'Start a room or diagnose common failures.':('Crea una sala o diagnostica los fallos habituales.','Crea una stanza o risolvi i problemi comuni.','建立房間或排查常見錯誤。'),
 'Plan a legal build':('Planifica una build legal','Pianifica una build valida','規劃合法配裝'),
 'Starting moves, upgrades and evolution routes.':('Movimientos iniciales, mejoras y rutas de evolución.','Mosse iniziali, potenziamenti e percorsi evolutivi.','起始招式、強化與進化路線。'),
 'Take the run to mobile':('Juega también en móvil','Porta la partita su mobile','在手機上繼續遊玩'),
 'Touch controls, installation and keeping your save.':('Controles táctiles, instalación y protección del guardado.','Comandi touch, installazione e protezione del salvataggio.','觸控操作、安裝方式與存檔保護。'),
 'Protect or recover progress':('Protege o recupera el progreso','Proteggi o recupera i progressi','保護或救援進度'),
 'Use the safe account and save checklist.':('Usa la lista segura para cuentas y guardados.','Usa la procedura sicura per account e salvataggi.','使用安全帳號與存檔檢查清單。'),
 'See the run.<br>Read the next move.':('Mira la partida.<br>Decide el siguiente paso.','Guarda la partita.<br>Scegli la prossima mossa.','觀看實戰。<br>判斷下一步。'),
 'Real captures from a fresh local guest session. Watch the automatic attack, then follow the guide for your next upgrade.':('Capturas reales de una sesión local nueva. Observa el ataque automático y sigue la guía para elegir la próxima mejora.','Catture reali da una nuova sessione locale. Osserva l’attacco automatico e segui la guida per il prossimo potenziamento.','來自全新本機訪客存檔的實際畫面；先觀察自動攻擊，再依攻略選擇下一張強化卡。'),
 'Learn the controls':('Aprende los controles','Impara i comandi','學習操作'),
 'Meet the partners.<br>Know the numbers.':('Conoce a los compañeros.<br>Entiende los números.','Conosci i compagni.<br>Leggi i valori.','認識夥伴。<br>掌握數值。'),
 'Actual partner stats and type rules from the recorded game snapshot. Find a name, compare an opening, or check a difficult matchup.':('Estadísticas y reglas de tipos de la versión registrada. Busca un nombre, compara una apertura o revisa un enfrentamiento difícil.','Statistiche e regole dei tipi dalla versione registrata. Cerca un nome, confronta un inizio o controlla uno scontro difficile.','資料來自已記錄的遊戲版本；可搜尋名稱、比較開局能力或確認棘手的屬性相剋。'),
 'Open the full Pokédex':('Abrir la Pokédex completa','Apri il Pokédex completo','開啟完整圖鑑'),
 'A sample of the partner reference':('Muestra de la tabla de compañeros','Esempio della tabella compagni','夥伴資料表範例'),
 'Move patterns & base values':('Patrones y valores base','Schemi e valori base delle mosse','招式型態與基礎數值'),
 'Type chart & matchup calculator':('Tabla de tipos y calculadora','Tabella tipi e calcolatore','屬性表與相剋計算器'),
 'Legendary encounters & roster':('Encuentros legendarios y plantilla','Incontri leggendari e rosa','傳說遭遇與名單'),
 'A tier is a starting point.<br>Your build is the plan.':('Una categoría es el comienzo.<br>Tu build es el plan.','La fascia è il punto di partenza.<br>La build è il piano.','排行只是起點。<br>配裝才是計畫。'),
 'Compare all 966 source attributes, then use the dedicated 29-starter list, move patterns and evolution requirements to plan a route.':('Compara los atributos de los 966 compañeros y usa la lista de 29 iniciales, los patrones y los requisitos para planificar la ruta.','Confronta i 966 profili e usa la lista dei 29 iniziali, gli schemi e i requisiti per pianificare il percorso.','比較 966 名夥伴的資料，再搭配 29 名開局排行、招式型態與進化條件安排路線。'),
 'See all 966 ranked':('Ver los 966 clasificados','Vedi tutti i 966 classificati','查看 966 名完整排行'),
 'Compare starters':('Comparar iniciales','Confronta gli iniziali','比較開局夥伴'),
 'Plan a build':('Planificar una build','Pianifica una build','規劃配裝'),
 'Latest verified game update':('Última actualización verificada','Ultimo aggiornamento verificato','最新已核對更新'),
 'Required updates':('Actualizaciones obligatorias','Aggiornamenti obbligatori','強制更新'),
 'A required update ends the current run after a 10-second warning, saves its recorded rewards and reloads the game.':('Una actualización obligatoria avisa durante 10 segundos, termina la partida, guarda las recompensas registradas y recarga el juego.','Un aggiornamento obbligatorio avvisa per 10 secondi, termina la partita, salva le ricompense registrate e ricarica il gioco.','強制更新會先顯示 10 秒提示，結束本局、儲存已記錄獎勵並重新載入遊戲。'),
 'Read the verified changes':('Leer los cambios verificados','Leggi le modifiche verificate','閱讀已核對變更'),
 'Checked against the source.':('Comprobado en el código fuente.','Controllato sul codice sorgente.','已依原始碼核對。'),
 'Reference reviewed 2026-10-18. Source inspection is separate from gameplay testing.':('Referencia revisada el 18-10-2026. Revisar el código no equivale a probar cada situación.','Riferimento verificato il 18/10/2026. L’analisi del codice è distinta dalle prove di gioco.','資料於 2026-10-18 核對；檢查原始碼與實際遊玩測試分開記錄。'),
 'Reference reviewed 2026-10-19. Source inspection is separate from gameplay testing.':('Referencia revisada el 19-10-2026. Revisar el código no equivale a probar cada situación.','Riferimento verificato il 19/10/2026. L’analisi del codice è distinta dalle prove di gioco.','資料於 2026-10-19 核對；檢查原始碼與實際遊玩測試分開記錄。'),
 'Our sources & method':('Fuentes y método','Fonti e metodo','資料來源與方法'),
 'Different game, similar name?':('¿Otro juego con un nombre parecido?','Un altro gioco con un nome simile?','名稱相近但不是同一款？'),
 'Pokémon Survivor Burst is a separate project. Identify your game before using a build or download guide.':('Pokémon Survivor Burst es otro proyecto. Identifica tu juego antes de seguir una build o una guía de descarga.','Pokémon Survivor Burst è un progetto diverso. Identifica il gioco prima di usare una build o una guida al download.','Pokémon Survivor Burst 是另一個專案；使用配裝或下載攻略前，請先確認目前遊戲。'),
 'Compare the games':('Comparar los juegos','Confronta i giochi','比較兩款遊戲')
}

_LOCALE_INDEX={'es':0,'it':1,'zh-hant':2}


def localize_home(body: str, locale: str) -> str:
    for source, targets in HOME_TEXT.items(): body=body.replace(source,targets[_LOCALE_INDEX[locale]])
    return localize_component(body,locale)


def localize_home_media(body: str, locale: str) -> str:
    media_text={
      'Original concept art · AI-assisted.':('Arte conceptual original · asistido por IA.','Concept art originale · assistita dall’IA.','原創概念圖 · AI 輔助。'),
      'A compass-bearing forest guardian beside a turquoise rift. Original AI-assisted concept illustration.':('Un guardián del bosque con brújula junto a una grieta turquesa. Ilustración conceptual original asistida por IA.','Un guardiano della foresta con bussola accanto a un varco turchese. Illustrazione originale assistita dall’IA.','帶著羅盤的森林守護者站在青綠裂隙旁；原創 AI 輔助概念圖。'),
      'Credits & scope':('Créditos y alcance','Crediti e ambito','素材說明'),
      'A first look at the battlefield':('Primer vistazo al campo de batalla','Primo sguardo al campo di battaglia','初次進入戰場'),
      'Your browser cannot play this video.':('Tu navegador no puede reproducir este vídeo.','Il browser non può riprodurre questo video.','你的瀏覽器無法播放此影片。'),
      'Open the WebM recording':('Abrir la grabación WebM','Apri la registrazione WebM','開啟 WebM 錄影'),
      'or read the steps below.':('o lee los pasos siguientes.','oppure leggi i passaggi qui sotto.','或閱讀下方步驟。'),
      'The video could not load. Read the transcript below or':('No se pudo cargar el vídeo. Lee la transcripción o','Impossibile caricare il video. Leggi la trascrizione o','影片無法載入，請閱讀逐步說明或'),
      'open the recording':('abre la grabación','apri la registrazione','開啟錄影'),
      'Read the video steps':('Leer los pasos del vídeo','Leggi i passaggi del video','閱讀影片步驟'),
      'Ember fires automatically while the partner moves.':('Ember se dispara automáticamente mientras el compañero se mueve.','Ember parte automaticamente mentre il compagno si muove.','夥伴移動時，Ember 會自動發射。'),
      'Keep space around the partner and approach dropped experience.':('Mantén espacio alrededor del compañero y acércate a la experiencia caída.','Mantieni spazio attorno al compagno e avvicinati all’esperienza caduta.','保持夥伴周圍的空間，再靠近掉落的經驗。'),
      'Upgrade offers and outcomes vary between runs.':('Las mejoras y los resultados cambian entre partidas.','Potenziamenti e risultati cambiano tra le partite.','每局出現的強化與結果都可能不同。'),
      'Game capture.':('Captura del juego.','Cattura di gioco.','遊戲實拍。'),
      'Ember attacks automatically while the partner moves.':('Ember ataca automáticamente mientras el compañero se mueve.','Ember attacca automaticamente mentre il compagno si muove.','夥伴移動時，Ember 會自動攻擊。'),
      'Capture & credits':('Captura y créditos','Cattura e crediti','錄影與來源')
    }
    for source,targets in media_text.items():body=body.replace(source,targets[_LOCALE_INDEX[locale]])
    body=body.replace('Silent recording with English captions.','')
    return body


def _component(body: str, marker: str) -> str:
    pattern = rf'(<(?:section class="data-section"|div class="tool[^"]*")[^>]*{marker}.*?(?:</section>|</noscript></div>))'
    found = re.search(pattern, body, re.S)
    return found.group(1) if found else ''


def _all_tables(body: str) -> str:
    return ''.join(re.findall(r'<section class="data-section".*?</section>', body, re.S))


def localize_component(value: str, locale: str) -> str:
    if not value: return value
    ui = UI[locale]
    value = value.replace('Find in this table', ui['table_search']).replace('Name, move or stat…', ui['table_placeholder'])
    value = value.replace('All types', ui['all_types']).replace('>Reset<', f'>{ui["reset"]}<')
    value = value.replace('No matches. Try another name or reset the filters.', ui['no_matches'])
    value = value.replace('Reference table', ui['reference_table'])
    for source, target in HEADERS[locale].items():
        value = value.replace(f'>{source}<', f'>{target}<').replace(f'>{source}<svg', f'>{target}<svg')
    for source, target in TYPE_NAMES[locale].items():
        value = re.sub(rf'>(?:{source.title()})</(?:span|option)>', lambda m: '>'+target+m.group(0)[m.group(0).rfind('</'):], value)
    replacements = {
      'Check your next evolution': {'es':'Comprueba tu próxima evolución','it':'Controlla la prossima evoluzione','zh-hant':'檢查下一個進化'},
      'Select what you have in this run. This checker does not access your game save.': {'es':'Indica lo que tienes en esta partida. No se accede al guardado.','it':'Indica ciò che hai in questa partita. Il salvataggio non viene letto.','zh-hant':'選擇本局已取得的項目；工具不會讀取存檔。'},
      'Current level': {'es':'Nivel actual','it':'Livello attuale','zh-hant':'目前等級'},
      'I have taken the required stat card in this run': {'es':'He tomado la carta requerida en esta partida','it':'Ho preso la carta richiesta in questa partita','zh-hant':'本局已取得所需能力卡'},
      'Check a type matchup': {'es':'Comprueba un enfrentamiento de tipos','it':'Controlla uno scontro tra tipi','zh-hant':'計算屬性相剋'},
      'Attacking type': {'es':'Tipo atacante','it':'Tipo attaccante','zh-hant':'攻擊屬性'},
      'Defending type': {'es':'Tipo defensor','it':'Tipo difensore','zh-hant':'防守屬性'},
      'Second defending type': {'es':'Segundo tipo defensor','it':'Secondo tipo difensore','zh-hant':'第二防守屬性'},
      '>None<': {'es':'>Ninguno<','it':'>Nessuno<','zh-hant':'>無<'},
      'Build route planner': {'es':'Planificador de build','it':'Pianificatore della build','zh-hant':'配裝路線規劃器'},
      'Starter': {'es':'Inicial','it':'Iniziale','zh-hant':'開局夥伴'},
      'Secondary move': {'es':'Movimiento secundario','it':'Mossa secondaria','zh-hant':'副招式'},
      'Copy share link': {'es':'Copiar enlace','it':'Copia link','zh-hant':'複製分享連結'},
      'Choose a starter and a compatible secondary move. The planner keeps the official starting move fixed and checks the evolution cards for both moves.': {'es':'Elige un inicial y un movimiento secundario compatible. Se conserva el movimiento inicial oficial y se comprueban ambas evoluciones.','it':'Scegli un iniziale e una mossa secondaria compatibile. La mossa iniziale ufficiale resta fissa e vengono controllate entrambe le evoluzioni.','zh-hant':'選擇開局夥伴與相容的副招式；工具會固定官方起始招式，並檢查兩者的進化條件。'},
      'Loading build data…': {'es':'Cargando datos de la build…','it':'Caricamento dati della build…','zh-hant':'正在載入配裝資料…'},
      'Check every evolution': {'es':'Consultar todas las evoluciones','it':'Controlla tutte le evoluzioni','zh-hant':'查看所有進化'},
      'The planner needs JavaScript. Use the four starter routes and evolution table below.': {'es':'El planificador necesita JavaScript. También puedes usar las rutas y la tabla.','it':'Il pianificatore richiede JavaScript. Puoi usare anche i percorsi e la tabella.','zh-hant':'規劃器需要 JavaScript；你仍可使用路線說明與進化表。'},
      'Build a privacy-safe recovery report': {'es':'Crea un informe de recuperación sin datos privados','it':'Crea un rapporto di recupero senza dati privati','zh-hant':'建立不含私密資料的救援報告'},
      'Choose only non-sensitive facts. This tool runs in your browser and does not inspect or upload a save.': {'es':'Elige solo datos no sensibles. La herramienta funciona en tu navegador y no revisa ni sube el guardado.','it':'Scegli solo dati non sensibili. Lo strumento funziona nel browser e non legge né carica il salvataggio.','zh-hant':'只選擇不敏感資訊；工具在瀏覽器中執行，不會檢查或上傳存檔。'},
      'Where the game was used': {'es':'Dónde se usó el juego','it':'Dove è stato usato il gioco','zh-hant':'遊戲使用位置'},
      'Official pokesurvivor.com': {'es':'pokesurvivor.com oficial','it':'pokesurvivor.com ufficiale','zh-hant':'官方 pokesurvivor.com'},
      'Installed PWA from the official site': {'es':'PWA instalada desde el sitio oficial','it':'PWA installata dal sito ufficiale','zh-hant':'從官方網站安裝的 PWA'},
      'Another address or unknown': {'es':'Otra dirección o desconocida','it':'Altro indirizzo o non noto','zh-hant':'其他網址或不確定'},
      'Account state': {'es':'Estado de la cuenta','it':'Stato dell’account','zh-hant':'帳號狀態'},
      'Linked to Gmail': {'es':'Vinculada a Gmail','it':'Collegato a Gmail','zh-hant':'已綁定 Gmail'},
      'Username/password; linkage unknown': {'es':'Usuario/contraseña; vínculo desconocido','it':'Nome utente/password; collegamento non noto','zh-hant':'帳號密碼；不確定是否綁定'},
      'Guest or unlinked': {'es':'Invitado o sin vincular','it':'Ospite o non collegato','zh-hant':'訪客或未綁定'},
      'Unknown': {'es':'No lo sé','it':'Non noto','zh-hant':'不確定'},
      'Surviving copy': {'es':'Copia que conserva el progreso','it':'Copia che conserva i progressi','zh-hant':'仍存有進度的副本'},
      'One browser/profile still shows progress': {'es':'Un navegador o perfil aún muestra el progreso','it':'Un browser o profilo mostra ancora i progressi','zh-hant':'某個瀏覽器／設定檔仍顯示進度'},
      'No copy shows progress': {'es':'Ninguna copia muestra el progreso','it':'Nessuna copia mostra i progressi','zh-hant':'沒有副本顯示進度'},
      'Visible symptom': {'es':'Síntoma visible','it':'Sintomo visibile','zh-hant':'畫面上的症狀'},
      'Progress or account appears missing': {'es':'Falta el progreso o la cuenta','it':'Progressi o account mancanti','zh-hant':'進度或帳號消失'},
      'Paused to protect your progress': {'es':'Pausado para proteger tu progreso','it':'In pausa per proteggere i progressi','zh-hant':'已暫停以保護進度'},
      '409 response while setting a name': {'es':'Respuesta 409 al elegir un nombre','it':'Risposta 409 durante la scelta del nome','zh-hant':'設定名稱時出現 409'},
      'Other or unknown': {'es':'Otro o desconocido','it':'Altro o non noto','zh-hant':'其他或不確定'},
      'Show safest next step': {'es':'Mostrar el siguiente paso más seguro','it':'Mostra il passo successivo più sicuro','zh-hant':'顯示最安全的下一步'},
      'Select what you know, then run the checklist.': {'es':'Selecciona lo que sabes y ejecuta la lista.','it':'Seleziona ciò che sai e avvia la procedura.','zh-hant':'選擇已知情況，再執行檢查。'},
      'Non-sensitive report': {'es':'Informe sin datos sensibles','it':'Rapporto senza dati sensibili','zh-hant':'不含敏感資訊的報告'},
      'Copy report': {'es':'Copiar informe','it':'Copia rapporto','zh-hant':'複製報告'},
      'JavaScript is required for the decision helper. Use the safety table above without entering private information.': {'es':'El asistente necesita JavaScript. Usa la tabla sin introducir datos privados.','it':'L’assistente richiede JavaScript. Usa la tabella senza inserire dati privati.','zh-hant':'判斷工具需要 JavaScript；也可直接使用上方表格，請勿輸入私密資料。'},
      'Enable JavaScript for the checker, or use the complete table below.': {'es':'Activa JavaScript para usar el comprobador o consulta la tabla completa.','it':'Attiva JavaScript per il controllo oppure usa la tabella completa.','zh-hant':'啟用 JavaScript 可使用檢查器，或直接查閱完整表格。'},
      'Enable JavaScript for dual-type calculations. The single-type chart remains available below.': {'es':'Activa JavaScript para calcular tipos dobles; la tabla simple sigue disponible.','it':'Attiva JavaScript per i calcoli con doppio tipo; la tabella singola resta disponibile.','zh-hant':'啟用 JavaScript 可計算雙屬性；下方仍提供單屬性表。'},
      'No evolution': {'es':'Sin evolución','it':'Nessuna evoluzione','zh-hant':'無進化'},
      'Starter / gacha': {'es':'Inicial / gacha','it':'Iniziale / gacha','zh-hant':'開局／扭蛋'},
      'Outside gacha pool': {'es':'Fuera del gacha','it':'Fuori dal gacha','zh-hant':'扭蛋池外'},
      '>Gacha<': {'es':'>Gacha<','it':'>Gacha<','zh-hant':'>扭蛋<'},
      'Current pity': {'es':'Pity actual','it':'Pity attuale','zh-hant':'目前保底進度'},
      'Gacha probability calculator': {'es':'Calculadora de probabilidad del gacha','it':'Calcolatore probabilità gacha','zh-hant':'扭蛋機率計算器'},
      'Enter future pulls and your current banner pity. Each regional banner tracks its own pity.': {'es':'Indica las tiradas previstas y el pity del banner. Cada región lleva su propio contador.','it':'Inserisci le estrazioni previste e il pity del banner. Ogni regione ha un contatore separato.','zh-hant':'輸入預計抽數與目前卡池保底；各地區卡池會分開計算。'},
      'Future pulls': {'es':'Tiradas previstas','it':'Estrazioni previste','zh-hant':'預計抽數'},
      'Base five-star rate is 1.5%, shiny chance is 1%, and pity guarantees a five-star at 70 pulls.': {'es':'La tasa base de rareza 5 es 1,5 %, la de shiny es 1 % y el pity garantiza rareza 5 en 70 tiradas.','it':'La probabilità base di rarità 5 è 1,5%, quella shiny è 1% e il pity garantisce rarità 5 a 70 estrazioni.','zh-hant':'五星基礎機率為 1.5%，異色機率為 1%，70 抽觸發五星硬保底。'},
    }
    for source, targets in replacements.items(): value = value.replace(source, targets[locale])
    patterns = {
      'es': {'Projectile':'Proyectil','Dash':'Desplazamiento','Aura':'Aura','Beam':'Rayo','Boomerang':'Bumerán','Buff':'Mejora','Chain':'Cadena','Cone':'Cono','Melee':'Cuerpo a cuerpo','Meteor':'Meteoro','Mine':'Mina','Nova':'Explosión','Orbit':'Órbita','Trail':'Rastro','Turret':'Torreta'},
      'it': {'Projectile':'Proiettile','Dash':'Scatto','Aura':'Aura','Beam':'Raggio','Boomerang':'Boomerang','Buff':'Bonus','Chain':'Catena','Cone':'Cono','Melee':'Corpo a corpo','Meteor':'Meteora','Mine':'Mina','Nova':'Esplosione','Orbit':'Orbita','Trail':'Scia','Turret':'Torretta'},
      'zh-hant': {'Projectile':'投射物','Dash':'衝刺','Aura':'光環','Beam':'光束','Boomerang':'迴旋','Buff':'增益','Chain':'連鎖','Cone':'錐形','Melee':'近戰','Meteor':'隕石','Mine':'地雷','Nova':'範圍爆發','Orbit':'環繞','Trail':'軌跡','Turret':'砲塔'}
    }
    for source, target in patterns[locale].items(): value = value.replace(f'>{source}<', f'>{target}<')
    value = re.sub(r'href="/(?!assets/|llms|index\.md)', f'href="/{locale}/', value)
    return value


def make_pages(base_pages: dict, locale: str) -> dict:
    pages = {}
    h = html.escape
    for slug, source in base_pages.items():
        title, description, lead, guidance = PAGES[locale][slug]
        body = f'<p class="lead">{h(lead)}</p>'
        if slug == 'search':
            body += f'<form action="{url(locale,"search")}" class="search-page"><label for="search-query">{UI[locale]["search"]}</label><div><input id="search-query" type="search" name="q" maxlength="100" placeholder="{h(guidance)}"><button class="button" type="submit">{UI[locale]["search"]}</button></div></form><p id="search-status" role="status" aria-live="polite"></p><ul id="search-results" class="search-results"></ul><noscript><p>JavaScript required.</p></noscript>'
        elif slug == '':
            body = localize_home(source['body'],locale)
        else:
            heading = {'es':'Cómo usar esta guía','it':'Come usare questa guida','zh-hant':'本頁使用方式'}[locale]
            body += f'<section class="article-section" id="uso"><h2>{heading}</h2><p>{h(guidance)}</p></section>'
            tool = _component(source['body'], 'data-(?:evolution|matchup|gacha|build-planner|save-diagnostic)')
            tables = _all_tables(source['body'])
            if tool: body += localize_component(tool, locale)
            if tables: body += localize_component(tables, locale)
        item = deepcopy(source)
        item.update(title=title, description=description, body=body)
        if slug == '': item['preserve_media_layout']=True
        pages[slug] = item
    return pages
