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


TYPE_NAMES = {
 'es': {'normal':'Normal','fire':'Fuego','water':'Agua','electric':'Eléctrico','grass':'Planta','ice':'Hielo','fighting':'Lucha','poison':'Veneno','ground':'Tierra','flying':'Volador','psychic':'Psíquico','bug':'Bicho','rock':'Roca','ghost':'Fantasma','dragon':'Dragón','dark':'Siniestro','steel':'Acero','fairy':'Hada'},
 'it': {'normal':'Normale','fire':'Fuoco','water':'Acqua','electric':'Elettro','grass':'Erba','ice':'Ghiaccio','fighting':'Lotta','poison':'Veleno','ground':'Terra','flying':'Volante','psychic':'Psico','bug':'Coleottero','rock':'Roccia','ghost':'Spettro','dragon':'Drago','dark':'Buio','steel':'Acciaio','fairy':'Folletto'},
 'zh-hant': {'normal':'一般','fire':'火','water':'水','electric':'電','grass':'草','ice':'冰','fighting':'格鬥','poison':'毒','ground':'地面','flying':'飛行','psychic':'超能力','bug':'蟲','rock':'岩石','ghost':'幽靈','dragon':'龍','dark':'惡','steel':'鋼','fairy':'妖精'}
}

HEADERS = {
 'es': {'No.':'N.º','Pokémon':'Pokémon','Partner':'Compañero','Type':'Tipo','HP':'PS','Speed':'Velocidad','Attack':'Ataque','Gen':'Gen.','Collection':'Obtención','Move':'Movimiento','Pattern':'Patrón','Base damage':'Daño base','Cooldown':'Enfriamiento','Max level':'Nivel máx.','Evolution':'Evolución','Required level':'Nivel requerido','Required stat card':'Carta requerida','Evolves into':'Evoluciona a','Starting move':'Movimiento inicial','Evolution stat':'Carta de evolución','Band':'Banda','Score':'Puntuación','Attack / defend':'Ataque / defensa'},
 'it': {'No.':'N.','Pokémon':'Pokémon','Partner':'Compagno','Type':'Tipo','HP':'PS','Speed':'Velocità','Attack':'Attacco','Gen':'Gen.','Collection':'Ottenimento','Move':'Mossa','Pattern':'Schema','Base damage':'Danno base','Cooldown':'Ricarica','Max level':'Livello max','Evolution':'Evoluzione','Required level':'Livello richiesto','Required stat card':'Carta richiesta','Evolves into':'Evolve in','Starting move':'Mossa iniziale','Evolution stat':'Carta evoluzione','Band':'Fascia','Score':'Punteggio','Attack / defend':'Attacco / difesa'},
 'zh-hant': {'No.':'編號','Pokémon':'寶可夢','Partner':'夥伴','Type':'屬性','HP':'HP','Speed':'速度','Attack':'攻擊','Gen':'世代','Collection':'取得方式','Move':'招式','Pattern':'型態','Base damage':'基礎傷害','Cooldown':'冷卻','Max level':'最高等級','Evolution':'進化','Required level':'所需等級','Required stat card':'所需能力卡','Evolves into':'進化為','Starting move':'起始招式','Evolution stat':'進化能力','Band':'階級','Score':'分數','Attack / defend':'攻擊／防守'}
}


JS = {
 'es': {'entries':'{count} de {total} registros','starterPartner':'Compañero inicial','levelRequirement':'Nivel {level} + {requirement} en esta partida; después elige la carta dorada.','loadingEvolution':'Cargando requisitos…','noEvolution':'{move} no tiene evolución en esta versión.','invalidLevel':'Introduce un nivel entero del 1 al {max}.','reachLevel':'alcanza el nivel {level}','takeStat':'toma {stat} en esta partida','eligible':'Puedes evolucionar a {evolution}. Elige la carta dorada cuando aparezca; no sucede automáticamente.','loadFail':'No se pudo cargar el comprobador. Usa la tabla o vuelve a intentarlo.','loadingTypes':'Cargando reglas de tipos…','damage':'{attack} → {defense}: {mult}× de daño','typeFail':'No se pudo cargar la calculadora. Usa la tabla inferior.','searchHint':'Prueba un Pokémon, un movimiento o una consulta como móvil.','searching':'Buscando…','results':'{count} resultados.','noResults':'Sin resultados. Prueba un nombre más corto o usa la navegación.','searchFail':'No se pudo cargar la búsqueda. Vuelve a intentarlo o navega por las guías.','linkCopied':'Enlace copiado','copyLink':'Copiar enlace','gachaInvalid':'Introduce entre 1 y 1000 tiradas y un pity actual entre 0 y 69.','gachaSummary':'Probabilidad base de al menos una rareza 5: {five} %. Probabilidad base de al menos una tirada con opción shiny: {shiny} %.','pityReach':'Esta ventana alcanza el pity duro de 70 en un máximo de {pulls} tiradas.','pityRemain':'El pity duro no está garantizado en esta ventana; faltan {pulls} tiradas.'},
 'it': {'entries':'{count} di {total} voci','starterPartner':'Compagno iniziale','levelRequirement':'Livello {level} + {requirement} in questa partita, poi scegli la carta dorata.','loadingEvolution':'Caricamento requisiti…','noEvolution':'{move} non ha un’evoluzione in questa versione.','invalidLevel':'Inserisci un livello intero da 1 a {max}.','reachLevel':'raggiungi il livello {level}','takeStat':'prendi {stat} in questa partita','eligible':'Puoi evolvere in {evolution}. Scegli la carta dorata quando appare; non avviene automaticamente.','loadFail':'Impossibile caricare il controllo. Usa la tabella o riprova.','loadingTypes':'Caricamento regole dei tipi…','damage':'{attack} → {defense}: danno {mult}×','typeFail':'Impossibile caricare il calcolatore. Usa la tabella qui sotto.','searchHint':'Prova un Pokémon, una mossa o un termine come mobile.','searching':'Ricerca…','results':'{count} risultati.','noResults':'Nessun risultato. Prova un nome più breve o usa la navigazione.','searchFail':'Ricerca non disponibile. Riprova o consulta guide e database.','linkCopied':'Link copiato','copyLink':'Copia link','gachaInvalid':'Inserisci 1–1000 estrazioni e un pity attuale tra 0 e 69.','gachaSummary':'Probabilità base di almeno una rarità 5: {five}%. Probabilità base di almeno un tiro idoneo shiny: {shiny}%.','pityReach':'Questa finestra raggiunge il pity rigido a 70 entro {pulls} estrazioni.','pityRemain':'Il pity rigido non è garantito in questa finestra; mancano {pulls} estrazioni.'},
 'zh-hant': {'entries':'顯示 {count}／{total} 筆','starterPartner':'開局夥伴','levelRequirement':'本局將招式升至 {level} 級並取得 {requirement}，再選擇金色卡。','loadingEvolution':'正在載入進化條件…','noEvolution':'此版本中的 {move} 沒有招式進化。','invalidLevel':'請輸入 1 至 {max} 的整數等級。','reachLevel':'升至 {level} 級','takeStat':'本局取得 {stat}','eligible':'可進化為 {evolution}。出現金色進化卡時仍需手動選擇。','loadFail':'無法載入檢查器，請使用下方表格或重新載入。','loadingTypes':'正在載入屬性規則…','damage':'{attack} → {defense}：{mult}× 傷害','typeFail':'無法載入計算器，請使用下方單屬性表。','searchHint':'可輸入寶可夢、招式，或「手機」等主題。','searching':'搜尋中…','results':'找到 {count} 筆結果。','noResults':'找不到結果，請縮短名稱或使用導覽。','searchFail':'無法載入搜尋，請重試或瀏覽攻略與資料庫。','linkCopied':'連結已複製','copyLink':'複製分享連結','gachaInvalid':'請輸入 1–1000 抽，且目前保底進度須為 0–69。','gachaSummary':'至少一次五星的基礎機率：{five}%；至少一次可出現異色判定的基礎機率：{shiny}%。','pityReach':'本次範圍會在最多 {pulls} 抽內觸發 70 抽硬保底。','pityRemain':'本次範圍不保證觸發硬保底；依目前進度尚差 {pulls} 抽。'}
}

JS['es'].update({'moveEvolution':'{move} → {evolution}: nivel {level} + {requirement}','moveNoEvolution':'{move}: sin evolución en esta versión','buildSummary':'{partner} empieza con {primary}. Ruta secundaria: {secondary}. Reserva compatible: tipos {types} y movimientos Normal.','plannerFail':'No se pudo cargar el planificador. Usa las rutas y la tabla de evoluciones.','copyFail':'El navegador bloqueó la copia; usa la URL de la barra de direcciones.'})
JS['it'].update({'moveEvolution':'{move} → {evolution}: livello {level} + {requirement}','moveNoEvolution':'{move}: nessuna evoluzione in questa versione','buildSummary':'{partner} inizia con {primary}. Percorso secondario: {secondary}. Pool compatibile: tipi {types} e mosse Normale.','plannerFail':'Impossibile caricare il pianificatore. Usa i percorsi e la tabella evoluzioni.','copyFail':'Il browser ha bloccato la copia; usa l’URL nella barra degli indirizzi.'})
JS['zh-hant'].update({'moveEvolution':'{move} → {evolution}：{level} 級 + {requirement}','moveNoEvolution':'{move}：此版本無進化','buildSummary':'{partner} 的起始路線為 {primary}。副招式路線：{secondary}。相容範圍：{types} 屬性與一般屬性招式。','plannerFail':'無法載入規劃器，請使用路線說明與進化表。','copyFail':'瀏覽器封鎖複製；請使用網址列中的連結。'})


def url(locale: str, slug: str) -> str:
    tail = (slug + '/') if slug else ''
    return '/' + tail if locale == 'en' else f'/{locale}/' + tail


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
            cards = ''.join(f'<a class="route" href="{url(locale,s)}"><span><strong>{h(PAGES[locale][s][0])}</strong><span>{h(PAGES[locale][s][2])}</span></span></a>' for s in ('how-to-play','tier-list','builds','arceus-judgment'))
            body = f'<section class="opening"><div class="hero"><div class="hero-copy"><h1>{h(title)}</h1><p class="lead">{h(lead)}</p><form class="hero-search" action="{url(locale,"search")}" role="search"><label class="sr-only" for="home-search">{UI[locale]["search"]}</label><input id="home-search" name="q" type="search" maxlength="100" placeholder="{UI[locale]["search"]}…"><button type="submit">→</button></form><div class="actions"><a class="button" href="{url(locale,"tier-list")}">{UI[locale]["tier"]}</a><a class="button secondary" href="{url(locale,"arceus-judgment")}">{UI[locale]["arceus"]}</a></div></div><div class="route-list">{cards}</div></div></section><div class="home-content"><section class="home-section"><div class="section-heading"><h2>{UI[locale]["start"]}</h2><p>{h(guidance)}</p></div></section>{localize_component(_all_tables(source["body"]),locale)}</div>'
        else:
            heading = {'es':'Cómo usar esta guía','it':'Come usare questa guida','zh-hant':'本頁使用方式'}[locale]
            body += f'<section class="article-section" id="uso"><h2>{heading}</h2><p>{h(guidance)}</p></section>'
            tool = _component(source['body'], 'data-(?:evolution|matchup|gacha|build-planner)')
            tables = _all_tables(source['body'])
            if tool: body += localize_component(tool, locale)
            if tables: body += localize_component(tables, locale)
        item = deepcopy(source)
        item.update(title=title, description=description, body=body)
        pages[slug] = item
    return pages
