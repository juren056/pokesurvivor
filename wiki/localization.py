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
 'tier-list':('寶可夢倖存者強度排行：966 名角色與配招參考','比較 966 名角色，再依取得狀態、物理／特殊方向、操作距離、合法招式與進化路線選角。','這是 966 名完整角色的資料比較，不是 29 名免費開局榜，也不是 400 金幣起始招式清單。評分來自能力值百分位，不是勝率或虛構實測。','先按已持有角色、免費開局、物理或特殊輸出與操作距離縮小範圍，再查合法招式與進化。完整榜、初始榜與起始招式各自回答不同問題。'),
 'starter-tier-list':('PokéSurvivor 29 名開局夥伴排行','比較 HP、速度、物理／特殊輸出與雙防百分位。','評分以 29 名開局夥伴的四維百分位計算，分組依名次切分，不會出現空白階級。','同時檢查起始招式分類；高輸出能力只會強化對應的物理或特殊側。'),
 'mobile':('PokéSurvivor 手機版：觸控、手把與手動瞄準','設定觸控或手把，並按需開啟手動瞄準。','遊戲在手機瀏覽器運作。10 月 18 日版本支援多數 USB 或藍牙手把；這不代表有 Nintendo Switch 原生版。','至「設定 → 控制」設定手把；若要以滑鼠或右類比擇瞄準，再至「設定 → 輔助使用」開啟手動瞄準。'),
 'updates':('PokéSurvivor 10 月 18 日更新','已核對物理／特殊、手把、儲存與阿爾宙斯變更。','官方更新日誌標記 10 月 18 日；核心提交對應北京時間 10 月 19 日 05:35。兩個日期代表不同事件。','重點包括四項戰鬥能力、詭計、10 分鐘自動儲存、儲存按鈕與新的阿爾宙斯壓力曲線。'),
 'arceus-judgment':('阿爾宙斯攻略：30–40 分鐘壓力時間軸','已核對速度軟上限、中毒縮放、加速與接觸傷害。','30:00 開始審判，阿爾宙斯仍無法擊敗。約 35:00 起持續加速，約 37:00 起接觸傷害增加，約 40:00 可能一擊倒下。','40 分鐘不是固定結束點。保留逃生路線，別只依賴超過軟上限的速度，並留意高 HP 敌人的中毒效果會降低。')})

# V4 copy: localized around the locked October 19 source (103 moves / 97 evolutions).
PAGES['es'].update({
 'moves':('Movimientos y evoluciones de PokéSurvivor: los 103','Consulta los 103 movimientos, sus patrones, categoría física o especial y 97 evoluciones.','La referencia del 19 de octubre reúne 103 movimientos, incluidas 38 incorporaciones, y 97 evoluciones. El patrón de ataque y la categoría de daño son datos distintos.','Busca por nombre, tipo, categoría o patrón. Los valores base no son una clasificación de DPS; confirma también la carta necesaria para evolucionar.'),
 'move-evolutions':('Evoluciones de PokéSurvivor: requisitos y carta dorada','Consulta 97 recetas de evolución, nivel máximo y carta de estadística necesaria.','Aquí evoluciona el movimiento equipado, no la especie del compañero. Alcanza el nivel máximo, toma la carta indicada en la misma partida y elige la carta dorada cuando aparezca.','Cumplir los requisitos solo habilita la oferta. Si no aparece, revisa el nivel, la carta exacta y si el movimiento ya evolucionó.'),
 'builds':('Builds de PokéSurvivor: movimiento inicial y rutas','Planifica el movimiento por defecto, la mejora Movimiento inicial, Repertorio y las evoluciones.','Movimiento inicial cuesta 400 monedas una vez por compañero y excluye mejoras de tipo buff; Repertorio cuesta 1.500 y añade un segundo movimiento. El movimiento por defecto siempre puede restaurarse.','El 20 % solo se aplica a un movimiento de daño del mismo tipo que un compañero de tipo único. Un movimiento fuera de tipo puede ser válido sin recibir el bonus.'),
 'upgrades':('Mejoras de PokéSurvivor: Movimiento inicial, costes y límites','Compara la mejora de 400 monedas, Repertorio de 1.500 y los costes exactos.','Movimiento inicial se compra una vez por compañero y permite elegir gratis después. Repertorio es otra mejora y sirve para comenzar con dos movimientos.','La lista inicial excluye buffs como Maquinación y Danza Espada, pero conserva el ataque por defecto incluso si no coincide con el tipo.'),
 'updates':('Actualización de PokéSurvivor del 19 de octubre','103 movimientos, 97 evoluciones, Movimiento inicial, bonus monotipo y guardado.','La versión registrada añade 38 movimientos y ocho patrones, además de Movimiento inicial. Los Pokémon de tipo único obtienen 20 % solo con ataques de daño de su tipo.','El código actual programa los cambios pendientes a los 30 minutos; la nota de 10 minutos pertenece al 18 de octubre. Espera o pendiente no significa subida completada.'),
 'save-recovery':('Recuperar el guardado de PokéSurvivor: estados seguros','Distingue copia local, subida pendiente, sincronización, confirmación en la nube y carga en el segundo dispositivo.','Usar la misma cuenta no demuestra que ambos dispositivos hayan cargado el mismo guardado. La revisión del 21 de octubre añade control de versiones para reducir el riesgo de que una copia antigua sustituya otra más reciente.','Conserva el dispositivo que mantiene el progreso. Pulsa Guardar, espera la confirmación visible y abre después el segundo dispositivo; no borres datos ni subas a ciegas una copia antigua.')})
PAGES['it'].update({
 'moves':('Mosse ed evoluzioni di PokéSurvivor: tutte le 103','Consulta 103 mosse, schemi, categoria fisica o speciale e 97 evoluzioni.','Il riferimento del 19 ottobre contiene 103 mosse, comprese 38 aggiunte, e 97 evoluzioni. Schema d’attacco e categoria di danno restano campi distinti.','Cerca per nome, tipo, categoria o schema. I valori base non sono una classifica DPS; controlla anche la carta richiesta per l’evoluzione.'),
 'move-evolutions':('Evoluzioni delle mosse: 97 ricette e requisiti','Controlla livello massimo, carta statistica e carta dorata per 97 evoluzioni.','Qui evolve la mossa equipaggiata, non la specie del compagno. Porta la mossa al massimo, prendi la carta richiesta nella stessa partita e scegli la carta dorata.','Avere i requisiti rende l’offerta possibile, non automatica. Se manca, ricontrolla livello, carta e stato della mossa.'),
 'builds':('Build di PokéSurvivor: mossa iniziale e percorsi','Pianifica mossa predefinita, upgrade Mossa iniziale, Repertorio ed evoluzioni.','Mossa iniziale costa 400 monete una volta per compagno ed esclude i buff; Repertorio costa 1.500 e aggiunge una seconda mossa. La mossa predefinita resta sempre selezionabile.','Il 20% vale solo per una mossa dannosa dello stesso tipo di un compagno monotipo. Una mossa predefinita fuori tipo può essere valida senza bonus.'),
 'upgrades':('Potenziamenti: Mossa iniziale, costi e limiti','Confronta Mossa iniziale da 400 monete, Repertorio da 1.500 e i costi esatti.','Mossa iniziale si compra una volta per compagno; in seguito la scelta è gratuita. Repertorio è distinto e permette di iniziare con due mosse.','La scelta iniziale esclude buff come Congiura e Danzaspada, ma conserva la mossa predefinita anche se fuori tipo.'),
 'updates':('Aggiornamento PokéSurvivor del 19 ottobre','103 mosse, 97 evoluzioni, Mossa iniziale, bonus monotipo e salvataggio.','La versione registrata aggiunge 38 mosse e otto schemi, oltre a Mossa iniziale. Il bonus del 20% richiede un compagno monotipo e una mossa dannosa dello stesso tipo.','Il codice attuale pianifica le modifiche in sospeso dopo 30 minuti; la nota dei 10 minuti appartiene al 18 ottobre. Attesa o pending non significa upload completato.'),
 'save-recovery':('Recupero salvataggio: stati e procedura sicura','Distingui copia locale, upload richiesto, sincronizzazione, conferma cloud e caricamento sul secondo dispositivo.','Lo stesso account non dimostra che entrambi i dispositivi abbiano caricato lo stesso salvataggio. La revisione del 21 ottobre aggiunge il controllo delle revisioni contro le copie vecchie.','Conserva il dispositivo con i progressi. Premi Salva, attendi la conferma visibile e solo dopo apri il secondo dispositivo; non cancellare i dati e non caricare alla cieca una copia vecchia.')})
PAGES['zh-hant'].update({
 'moves':('PokéSurvivor 103 種招式與進化總表','查詢 103 種招式、攻擊型態、物理／特殊分類及 97 條進化。','10 月 19 日資料包含 103 種招式，其中新增 38 種，並有 97 條招式進化。攻擊型態與傷害分類是不同欄位。','可依名稱、屬性、分類或型態搜尋。基礎數值不是 DPS 排行；規劃前還要核對同局所需能力卡。'),
 'move-evolutions':('PokéSurvivor 招式進化表：97 組條件與金色卡','查詢 97 組招式進化的最高等級、能力卡與金色卡條件。','此處進化的是裝備中的招式，不是夥伴物種。將招式升滿、本局取得指定能力卡，並在金色卡出現時選取。','達成條件只代表有資格進入卡池，不會自動進化；未出現時請核對等級、能力卡與是否已進化。'),
 'builds':('PokéSurvivor 配裝：起始招式與升級路線','規劃預設起手、400 金幣起始招式、1,500 金幣招式庫與進化路線。','「起始招式」每名夥伴一次花費 400 金幣，且不能選增益招式；「招式庫」是 1,500 金幣的另一項升級，會增加第二招。預設招式永遠可切回。','20% 加成只適用於單屬性夥伴使用同屬性的傷害招式。異屬性的預設招式仍可合法選擇，但不會獲得該加成。'),
 'upgrades':('PokéSurvivor 升級：起始招式、費用與上限','比較 400 金幣起始招式、1,500 金幣招式庫及完整升級費用。','「起始招式」每名夥伴購買一次，之後可免費切換；「招式庫」則是開局攜帶兩招的另一項升級。','起始選單會排除詭計、劍舞等增益招式，但即使預設招式不同屬性，也會保留讓玩家切回。'),
 'updates':('PokéSurvivor 10 月 19 日更新','103 種招式、97 條進化、起始招式、單屬性加成與存檔節奏。','本次版本新增 38 種招式與八種攻擊型態，並加入起始招式。單屬性夥伴只在使用同屬性傷害招式時獲得 20% 加成。','目前程式會在第一筆未同步變更後 30 分鐘排程上傳；10 分鐘為 10 月 18 日舊說明。等待或待同步不代表雲端已完成。'),
 'save-recovery':('PokéSurvivor 存檔救援：同步狀態與安全步驟','分辨本機副本、要求上傳、同步中、雲端完成，以及第二台裝置已載入。','使用同一個 Google 帳戶，不代表兩台裝置已載入同一份雲端資料。10 月 21 日版本加入 revision 衝突保護，降低舊裝置覆蓋較新雲端資料的風險。','先保留仍有完整進度的裝置；按下儲存並等到畫面明確顯示雲端成功，再開啟第二台裝置。不要清除資料，也不要盲目上傳較舊副本。')})

# V5 copy: October 20 source review, co-op evidence and platform intent.
PAGES['es'].update({
 'download':('Descargar PokéSurvivor: Android, iPhone y PC','Abre el juego oficial, instala la PWA y distingue una web oficial de un APK o port no verificado.','PokéSurvivor se juega directamente en pokesurvivor.com desde Android, iPhone, iPad o PC. La PWA añade esa misma web a la pantalla de inicio; esta guía no ofrece un APK oficial inexistente.','Abre primero la web oficial. En Android usa Instalar aplicación o Añadir a pantalla de inicio; en iPhone/iPad usa Safari → Compartir → Añadir a pantalla de inicio. Si una web incrustada muestra el aviso oficial, sal de ese marco y abre pokesurvivor.com.'),
 'co-op':('PokéSurvivor no conecta: Conectando y Reconectando','Distingue amistad, invitación, conexión con el anfitrión y partida; consulta informes entre redes sin arriesgar el guardado.','Una sala puede mostrar a los jugadores antes de completar la conexión con el anfitrión. Separa cuatro fases: amistad, invitación, conexión y partida. Los informes #233–235 son experiencias de jugadores, no un apagón confirmado.','Abre el juego oficial, comprueba versiones y cuentas, acepta una invitación nueva y mantén activo al anfitrión. No borres datos ni desactives el cortafuegos. Las notas oficiales del 21 de octubre ya publican una ruta de retransmisión TURN; esta Wiki no ha probado todas las cuentas, redes ni desconexiones durante la partida.'),
 'how-to-play':('Cómo jugar a PokéSurvivor: controles, idioma y mejoras','Aprende controles, cambio manual de movimiento, Movimiento inicial y el menú de idioma.','Los ataques son automáticos, pero aprender un movimiento ya no lo activa por sí solo. Cambia con 1–4 o Q/E, o toca la ranura en móvil. El idioma del juego está en Ajustes → Gráficos → Idioma.','Movimiento inicial cambia la apertura; Repertorio añade una segunda. El selector de idioma de esta Wiki no cambia el idioma del juego.'),
 'mobile':('PokéSurvivor en Android y iPhone: controles, PWA e idioma','Configura táctil, mando, mira manual, PWA e idioma sin perder el guardado.','Usa Ajustes → Controles para botones y mando, Accesibilidad para Mira manual y Gráficos → Idioma para el idioma del juego.','Aprender una nueva habilidad no la activa automáticamente: toca la ranura deseada. No borres datos del sitio como paso rutinario.'),
 'updates':('Actualización de PokéSurvivor del 21 de octubre: guardado y retransmisión','Control de revisiones del guardado, ruta de retransmisión por servidor, Guardar manual y correcciones verificadas.','La revisión del 21 de octubre protege frente a copias antiguas entre dispositivos y publica una ruta de retransmisión cuando falla la conexión directa.','Distingue código publicado, despliegue y reproducción: no garantiza recuperar pérdidas anteriores ni resolver todas las desconexiones.')})
PAGES['it'].update({
 'co-op':('PokéSurvivor co-op: connessione e riconnessione','Distingui amicizia, invito, collegamento all’host e partita; consulta le segnalazioni senza rischiare il salvataggio.','La stanza può mostrare i giocatori prima che il collegamento all’host sia pronto. Le issue #233–235 sono segnalazioni, non prova di un disservizio globale.','Apri il sito ufficiale, verifica versioni e account, accetta un nuovo invito e mantieni attivo l’host. Le note ufficiali del 21 ottobre descrivono ora un percorso relay TURN; questa Wiki non ha provato ogni account, rete o disconnessione durante la partita.'),
 'how-to-play':('Come giocare a PokéSurvivor: comandi, lingua e potenziamenti','Comandi, cambio manuale della mossa, Mossa iniziale e menu della lingua.','Imparare una mossa non la rende più automaticamente attiva. Cambia con 1–4 o Q/E, oppure tocca lo slot. La lingua del gioco è in Impostazioni → Grafica → Lingua.','Mossa iniziale cambia l’apertura; Repertorio aggiunge una seconda mossa. La lingua della Wiki è separata.'),
 'mobile':('PokéSurvivor su Android e iPhone: comandi, PWA e lingua','Configura touch, controller, mira manuale, PWA e lingua senza rischiare il salvataggio.','Usa Impostazioni → Controlli per i pulsanti, Accessibilità per Mira manuale e Grafica → Lingua per la lingua del gioco.','Una nuova mossa non si attiva automaticamente: tocca lo slot desiderato. Non cancellare i dati del sito come prova ordinaria.'),
 'updates':('Aggiornamento PokéSurvivor del 21 ottobre: salvataggi e relay','Controllo delle revisioni, percorso relay tramite server, Salva manuale e correzioni verificate.','La revisione del 21 ottobre protegge dalle copie vecchie tra dispositivi e pubblica un percorso relay quando la connessione diretta fallisce.','Distingui codice pubblicato, distribuzione e riproduzione: non garantisce il recupero di perdite precedenti né risolve ogni disconnessione.')})
PAGES['zh-hant'].update({
 'co-op':('PokéSurvivor 連線失敗：一直連線／重新連線怎麼辦','分辨好友、房間邀請、與房主連線及對局四階段，安全整理跨網路回報。','房間裡看得到玩家，不代表已與房主建立連線。#233–235 是玩家回報，不能當成全體停服或已確認的 NAT 原因。','直接開啟官方遊戲、核對版本與帳號、接受新邀請並讓房主保持前台。不要清除資料或關閉防火牆；10 月 21 日官方紀錄已公布 TURN 中繼路徑；本站尚未測遍所有帳號、網路及對局中斷情境。'),
 'how-to-play':('PokéSurvivor 新手攻略：操作、語言與升級','學會手動切招、起始招式，以及遊戲語言設定。','學會新招式後不會自動切換；桌面可用 1–4 或 Q/E，手機則點選招式欄。遊戲語言位於「設定 → 圖形 → 語言」。','起始招式決定開局，招式庫則增加第二招。Wiki 語言選單與遊戲語言是兩個不同設定。'),
 'mobile':('PokéSurvivor 手機版：觸控、PWA、手把與語言','在 Android、iPhone 或 iPad 設定觸控、手把、手動瞄準、PWA 與語言。','「設定 → 控制」調整按鈕；「輔助使用」開啟手動瞄準；「圖形 → 語言」更改遊戲語言。','新學到的招式不會自動啟用，請點選需要的招式欄；不要把清除網站資料當成一般排障步驟。'),
 'starter-tier-list':('PokéSurvivor 開局夥伴強度排行：29 名完整比較','用遊戲內中文名稱、英文別名、起始招式與透明能力分數比較 29 名夥伴。','排行比較免費開局夥伴的 HP、速度、輸出與雙防；起始招式升級是另外的 400 金幣解鎖，不代表新增夥伴。','可用中文或英文名搜尋。先依操作距離與招式型態選擇，再核對進化能力卡；分數不是勝率。'),
 'updates':('PokéSurvivor 10 月 21 日更新：存檔版本與伺服器中繼','存檔 revision 衝突保護、伺服器中繼路徑、手動儲存與已核對修正。','10 月 21 日版本降低舊裝置副本覆蓋較新雲端資料的風險，並公布直接連線失敗時的伺服器中繼路徑。','請區分已公布程式、正式部署與本站實測；它不保證找回過去遺失內容，也不代表所有中途斷線都已解決。')})


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

JS['es'].update({'moveEvolution':'{move} → {evolution}: nivel {level} + {requirement}','moveNoEvolution':'{move}: sin evolución en esta versión','buildSummary':'{partner}. Apertura por defecto: {defaultMove}. {unlock}: {primary}. Segundo movimiento de Repertorio: {secondary}. El factor del 20 % solo corresponde a movimientos de daño del mismo tipo en un compañero monotipo.','plannerFail':'No se pudo cargar el planificador. Usa las rutas y la tabla de evoluciones.','copyFail':'El navegador bloqueó la copia; usa la URL de la barra de direcciones.'})
JS['it'].update({'moveEvolution':'{move} → {evolution}: livello {level} + {requirement}','moveNoEvolution':'{move}: nessuna evoluzione in questa versione','buildSummary':'{partner}. Apertura predefinita: {defaultMove}. {unlock}: {primary}. Seconda mossa di Repertorio: {secondary}. Il fattore del 20% vale solo per mosse dannose dello stesso tipo di un compagno monotipo.','plannerFail':'Impossibile caricare il pianificatore. Usa i percorsi e la tabella evoluzioni.','copyFail':'Il browser ha bloccato la copia; usa l’URL nella barra degli indirizzi.'})
JS['zh-hant'].update({'moveEvolution':'{move} → {evolution}：{level} 級 + {requirement}','moveNoEvolution':'{move}：此版本無進化','buildSummary':'{partner}。預設起手：{defaultMove}。{unlock}：{primary}。招式庫第二招：{secondary}。20% 因子只適用於單屬性夥伴的同屬性傷害招式。','plannerFail':'無法載入規劃器，請使用路線說明與進化表。','copyFail':'瀏覽器封鎖複製；請使用網址列中的連結。'})
JS['es'].update({'savePreserveMismatch':'Conserva el dispositivo original y su perfil. Guardado local, pendiente, sincronización, éxito en la nube y carga en el segundo dispositivo son estados distintos. No borres datos ni subas una copia antigua mientras investigas.','savePreserve':'Conserva ese navegador y perfil. No borres los datos ni desinstales la PWA. Vincula la cuenta solo desde el juego oficial si es seguro hacerlo.','saveLinked':'En el dominio oficial, usa Iniciar sesión con Google con el mismo Gmail vinculado. Si falta el progreso, contacta al desarrollador con este informe sin datos privados.','saveGuest':'La recuperación de un invitado no vinculado es incierta. Conserva el navegador y perfil originales y contacta al desarrollador; no confíes en sitios que pidan credenciales o el guardado.','saveUnknown':'La recuperación es incierta. Conserva los datos restantes y contacta al desarrollador antes de hacer cambios destructivos.','reportCopied':'Informe copiado','copyReport':'Copiar informe','reportCopyFail':'El navegador bloqueó la copia. Selecciona el texto y cópialo manualmente.'})
JS['it'].update({'savePreserveMismatch':'Conserva il dispositivo originale e il suo profilo. Copia locale, attesa, sincronizzazione, conferma cloud e caricamento sul secondo dispositivo sono stati distinti. Non cancellare dati e non caricare una copia vecchia durante la verifica.','savePreserve':'Conserva quel browser e profilo. Non cancellare i dati e non disinstallare la PWA. Collega l’account solo dal gioco ufficiale se è sicuro farlo.','saveLinked':'Sul dominio ufficiale, usa Accedi con Google con lo stesso Gmail collegato. Se i progressi mancano, contatta lo sviluppatore con questo rapporto non sensibile.','saveGuest':'Il recupero di un ospite non collegato è incerto. Conserva browser e profilo originali e contatta lo sviluppatore; non fidarti di siti che chiedono credenziali o salvataggi.','saveUnknown':'Il recupero è incerto. Conserva i dati rimasti e contatta lo sviluppatore prima di modifiche distruttive.','reportCopied':'Rapporto copiato','copyReport':'Copia rapporto','reportCopyFail':'Il browser ha bloccato la copia. Seleziona il testo e copialo manualmente.'})
JS['zh-hant'].update({'savePreserveMismatch':'保留原裝置及其瀏覽器設定檔。本機已保存、等待上傳、同步中、雲端成功與第二台已載入是不同狀態。排查時不要清除資料，也不要上傳較舊副本。','savePreserve':'保留該瀏覽器與設定檔，不要清除網站資料或移除 PWA。只有在安全時，才透過官方遊戲綁定帳號。','saveLinked':'在官方網域使用同一個已綁定 Gmail 登入。進度仍消失時，請以這份不含私密資料的報告聯絡開發者。','saveGuest':'未綁定訪客的救援結果不確定。請保留原瀏覽器與設定檔並聯絡開發者；不要信任要求帳密或上傳存檔的網站。','saveUnknown':'救援結果不確定。進行破壞性變更前，先保留現存瀏覽器資料並以不敏感資訊聯絡開發者。','reportCopied':'報告已複製','copyReport':'複製報告','reportCopyFail':'瀏覽器封鎖複製；請手動選取報告文字。'})
for _locale in ('es','it','zh-hant'): JS[_locale]['typeNames']=TYPE_NAMES[_locale]
JS['es'].update({'startingUnlocked':'Movimiento inicial desbloqueado','startingLocked':'Movimiento inicial no comprado'})
JS['it'].update({'startingUnlocked':'Mossa iniziale sbloccata','startingLocked':'Mossa iniziale non acquistata'})
JS['zh-hant'].update({'startingUnlocked':'已解鎖起始招式','startingLocked':'尚未購買起始招式'})
JS['es'].update({'coopOfficial':'Abre pokesurvivor.com directamente. El juego bloquea el uso en iframes de terceros; esta Wiki no ofrece proxy ni recupera cuentas.','coopInvite':'Comprueba las cuentas, la amistad aceptada y una invitación nueva a la sala actual.','coopConnecting':'Aparecer en la sala no demuestra que la conexión con el anfitrión esté lista. Comprueba la versión y mantén activo al anfitrión.','coopDifferent':'Un jugador informó de éxito en la misma red y fallo entre redes. Regístralo sin diagnosticar tu NAT. El paquete TURN revisado no está desplegado ni conectado al juego.','coopSame':'La misma red no descarta otras causas. Registra el resultado sin reiniciar cuentas ni borrar datos.','coopBoss':'Es un problema durante la partida. El changelog del 19 de octubre describe una corrección para un jefe demasiado lejano; comprueba la versión y si se repite.','coopMove':'Anota movimiento, nivel, evolución, compañero, modo y versión. #232 es un informe, no prueba de que todo esté roto.','coopReport':'Anota mensaje, rol, navegador/dispositivo y hora aproximada. Oculta nombres, IP y datos privados.','coopReportTitle':'Lista co-op de PokéSurvivor (sin credenciales, guardados ni datos WebRTC completos)','checklistCopied':'Lista copiada','copyChecklist':'Copiar lista','checklistCopyFail':'El navegador bloqueó la copia. Selecciona el texto y cópialo manualmente.'})
JS['it'].update({'coopOfficial':'Apri direttamente pokesurvivor.com. Il gioco blocca gli iframe di terzi; la Wiki non offre proxy e non recupera account.','coopInvite':'Verifica account, amicizia accettata e un nuovo invito alla stanza corrente.','coopConnecting':'Essere nella stanza non prova che la connessione con l’host sia pronta. Verifica la versione e mantieni attivo l’host.','coopDifferent':'Un utente segnala successo sulla stessa rete e problemi tra reti. Registralo senza diagnosticare il NAT. Il TURN verificato non è distribuito né collegato al gioco.','coopSame':'La stessa rete non esclude altre cause. Registra il risultato senza reimpostare account o cancellare dati.','coopBoss':'È un problema durante la partita. Il changelog del 19 ottobre descrive una correzione per un boss troppo lontano; verifica versione e persistenza.','coopMove':'Annota mossa, livello, evoluzione, compagno, modalità e versione. #232 è una segnalazione, non la prova che tutto sia rotto.','coopReport':'Annota messaggio, ruolo, browser/dispositivo e ora approssimativa. Nascondi nomi, IP e dati privati.','coopReportTitle':'Lista co-op PokéSurvivor (senza credenziali, salvataggi o dati WebRTC completi)','checklistCopied':'Elenco copiato','copyChecklist':'Copia elenco','checklistCopyFail':'Il browser ha bloccato la copia. Seleziona il testo e copialo manualmente.'})
JS['zh-hant'].update({'coopOfficial':'直接開啟 pokesurvivor.com。遊戲會阻擋第三方 iframe；本站不提供代理，也不能恢復帳號。','coopInvite':'確認雙方帳號、已接受好友關係，以及目前房間的新邀請。','coopConnecting':'出現在房間中不代表已與房主建立連線；先核對版本並讓房主保持前台。','coopDifferent':'有玩家回報同網成功、跨網失敗；請記錄比較，不要據此診斷 NAT。10 月 21 日官方紀錄已公布 TURN 中繼路徑；本站尚未測遍所有帳號、網路及對局中斷情境。','coopSame':'同一網路仍可能有其他原因。記錄結果，不要重設帳號或刪除資料。','coopBoss':'這是對局內問題。10 月 19 日更新日誌描述 Boss 生成過遠的修正；請核對版本並記錄是否重現。','coopMove':'記錄招式、等級、進化、夥伴、模式與版本。#232 是玩家回報，不代表所有招式都壞了。','coopReport':'記錄錯誤文字、房主或加入者、瀏覽器／裝置及大約時間；移除暱稱、IP 與私密資料。','coopReportTitle':'PokéSurvivor 合作檢查清單（不含帳密、存檔或完整 WebRTC 資料）','checklistCopied':'清單已複製','copyChecklist':'複製檢查清單','checklistCopyFail':'瀏覽器封鎖複製；請手動選取清單文字。'})

JS['es'].update({'coopDifferent':'La versión actual prefiere una conexión directa y puede usar el piloto TURN para cuentas autorizadas. Sin credenciales, continúa solo con STUN; esto no garantiza disponibilidad universal.','masterCount':'{done} de {total} completadas · {shown} visibles','masterMemory':'El almacenamiento no está disponible. Los cambios solo duran hasta cerrar esta página.','masterMemoryShort':'solo memoria temporal','masterInvalidStored':'La lista guardada no era válida. Se abrió una lista temporal vacía.','masterLoadFail':'No se pudo cargar la lista. Usa la tabla estática inferior.','masterTooLarge':'Importación rechazada: el archivo es demasiado grande.','masterUnknown':'Importado con {count} ID desconocidos conservados para revisión.','masterImported':'Lista importada.','masterInvalid':'Importación rechazada: elige un JSON válido de Move Master.','masterResetConfirm':'¿Restablecer todos los movimientos completados de esta lista del navegador?','masterReset':'Lista restablecida.'})
JS['it'].update({'coopDifferent':'La versione attuale preferisce una connessione diretta e può usare il pilota TURN per gli account autorizzati. Senza credenziali continua solo con STUN; non è una garanzia di disponibilità universale.','masterCount':'{done} di {total} completate · {shown} visibili','masterMemory':'Lo spazio locale non è disponibile. Le modifiche durano solo fino alla chiusura della pagina.','masterMemoryShort':'solo memoria temporanea','masterInvalidStored':'La lista salvata non era valida. È stata aperta una lista temporanea vuota.','masterLoadFail':'Impossibile caricare la lista. Usa la tabella statica sotto.','masterTooLarge':'Importazione rifiutata: file troppo grande.','masterUnknown':'Importazione completata con {count} ID sconosciuti conservati per verifica.','masterImported':'Lista importata.','masterInvalid':'Importazione rifiutata: scegli un JSON Move Master valido.','masterResetConfirm':'Azzerare tutte le mosse completate in questa lista del browser?','masterReset':'Lista azzerata.'})
JS['zh-hant'].update({'coopDifferent':'目前版本優先使用直接連線；獲授權帳號可使用 TURN 試行服務。沒有憑證時只使用 STUN，這不代表服務全面可用。','masterCount':'已完成 {done}／{total} · 顯示 {shown} 項','masterMemory':'無法使用瀏覽器儲存空間；變更只保留到關閉本頁。','masterMemoryShort':'僅暫存於記憶體','masterInvalidStored':'已儲存的清單無效，已開啟暫時空白清單。','masterLoadFail':'無法載入清單，請使用下方靜態表格。','masterTooLarge':'匯入遭拒：檔案過大。','masterUnknown':'已匯入，另保留 {count} 個未知 ID 供檢查。','masterImported':'清單已匯入。','masterInvalid':'匯入遭拒：請選擇有效的 Move Master JSON。','masterResetConfirm':'要重設此瀏覽器清單中的所有完成項目嗎？','masterReset':'清單已重設。'})


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
 '38 new moves + Starting Move':('38 movimientos nuevos + Movimiento inicial','38 nuove mosse + Mossa iniziale','38 種新招式＋起始招式'),
 'The recorded update expands the reference to 103 moves and 97 evolutions, adds the 400-coin Starting Move upgrade and gives matching damaging moves a 20% bonus for single-type partners.':('La actualización registrada amplía la referencia a 103 movimientos y 97 evoluciones, añade Movimiento inicial por 400 monedas y aplica un 20 % a los ataques de daño del mismo tipo en compañeros monotipo.','L’aggiornamento registrato porta la guida a 103 mosse e 97 evoluzioni, aggiunge Mossa iniziale da 400 monete e applica un 20% alle mosse dannose dello stesso tipo per i compagni monotipo.','已記錄版本擴充至 103 種招式與 97 條進化，加入 400 金幣起始招式；單屬性夥伴使用同屬性傷害招式時獲得 20% 加成。'),
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

HOME_TEXT.update({
 'Latest verified source review':('Última revisión de fuente','Ultima verifica della fonte','最新原始碼核對'),
 'Languages, co-op evidence & official-site access':('Idiomas, evidencias co-op y acceso oficial','Lingue, prove co-op e accesso ufficiale','語言、合作證據與官方入口'),
 'The October 19 release remains at 103 moves and 97 evolutions. The latest review adds the game-language path, separates connection reports from the boss-spawn fix, and records the official-site iframe rule.':('La versión del 19 de octubre mantiene 103 movimientos y 97 evoluciones. La revisión añade la ruta del idioma, separa los informes de conexión de la corrección del jefe y registra la regla de iframe.','La versione del 19 ottobre resta a 103 mosse e 97 evoluzioni. La verifica aggiunge il percorso della lingua, separa le segnalazioni di connessione dalla correzione del boss e registra la regola iframe.','10 月 19 日版本仍為 103 種招式與 97 條進化；最新核對補上遊戲語言路徑、區分連線回報與 Boss 生成修正，並記錄官方網站 iframe 規則。'),
 'Reference reviewed 2026-10-20. Source inspection is separate from gameplay testing.':('Referencia revisada el 20-10-2026. Revisar el código no equivale a probar cada situación.','Riferimento verificato il 20/10/2026. L’analisi del codice è distinta dalle prove di gioco.','資料於 2026-10-20 核對；檢查原始碼與實際遊玩測試分開記錄。')
})
HOME_TEXT.update({
 'Save revisions & server relay':('Revisiones de guardado y retransmisión','Revisioni del salvataggio e relay','存檔版本與伺服器中繼'),
 'The October 21 source adds revision conflict protection for cross-device saves and publishes a server-relay path while preserving direct connections.':('El código del 21 de octubre protege los guardados entre dispositivos con revisiones y publica una ruta de retransmisión sin dejar de priorizar la conexión directa.','Il codice del 21 ottobre protegge i salvataggi tra dispositivi con revisioni e pubblica un percorso relay continuando a preferire la connessione diretta.','10 月 21 日原始碼加入跨裝置存檔版本衝突保護，並在保留直接連線優先的同時公布伺服器中繼路徑。')
})
HOME_TEXT.update({
 'Manual Save, friend invites & TURN pilot':('Guardado manual, invitaciones y piloto TURN','Salvataggio manuale, inviti e pilota TURN','手動儲存、好友邀請與 TURN 試行'),
 'The current source uses explicit cloud Save, removes the friend Online prerequisite and integrates an authorized TURN pilot while preserving direct connections.':('El código actual usa Guardar para subir a la nube, elimina el requisito En línea para invitar e integra un piloto TURN autorizado manteniendo la conexión directa.','Il codice attuale usa Salva per il cloud, rimuove il requisito Online per gli inviti e integra un pilota TURN autorizzato mantenendo la connessione diretta.','目前原始碼改用明確的雲端「儲存」、移除好友邀請的上線前提，並在保留直接連線的同時整合授權 TURN 試行。'),
 'Reference reviewed 2026-10-21. Source inspection is separate from gameplay testing.':('Referencia revisada el 21-10-2026. Revisar el código no equivale a probar cada situación.','Riferimento verificato il 21/10/2026. L’analisi del codice è distinta dalle prove di gioco.','資料於 2026-10-21 核對；檢查原始碼與實際遊玩測試分開記錄。')
})

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
      'Starting move & build planner': {'es':'Movimiento inicial y planificador de build','it':'Mossa iniziale e pianificatore build','zh-hant':'起始招式與配裝規劃器'},
      'Partner': {'es':'Compañero','it':'Compagno','zh-hant':'夥伴'},
      'Starting Move purchased for this partner': {'es':'Movimiento inicial comprado para este compañero','it':'Mossa iniziale acquistata per questo compagno','zh-hant':'此夥伴已購買起始招式'},
      'Selected starting move': {'es':'Movimiento inicial elegido','it':'Mossa iniziale scelta','zh-hant':'已選起始招式'},
      'Second move (Repertoire)': {'es':'Segundo movimiento (Repertorio)','it':'Seconda mossa (Repertorio)','zh-hant':'第二招（招式庫）'},
      'Copy share link': {'es':'Copiar enlace','it':'Copia link','zh-hant':'複製分享連結'},
      'Model the partner’s default opening, the optional 400-coin Starting Move unlock, and the separate second move from Repertoire. This local tool never reads or changes a game account.': {'es':'Modela la apertura por defecto, la mejora opcional Movimiento inicial de 400 monedas y el segundo movimiento separado de Repertorio. La herramienta no lee ni cambia la cuenta.','it':'Modella l’apertura predefinita, lo sblocco facoltativo Mossa iniziale da 400 monete e la seconda mossa separata di Repertorio. Lo strumento non legge né modifica l’account.','zh-hant':'規劃預設起手、400 金幣起始招式解鎖，以及招式庫提供的第二招；本機工具不會讀取或變更遊戲帳號。'},
      'Loading build data…': {'es':'Cargando datos de la build…','it':'Caricamento dati della build…','zh-hant':'正在載入配裝資料…'},
      'Check every evolution': {'es':'Consultar todas las evoluciones','it':'Controlla tutte le evoluzioni','zh-hant':'查看所有進化'},
      'The planner needs JavaScript. Use the route notes and evolution table below.': {'es':'El planificador necesita JavaScript. También puedes usar las notas de ruta y la tabla.','it':'Il pianificatore richiede JavaScript. Puoi usare le note e la tabella evoluzioni.','zh-hant':'規劃器需要 JavaScript；仍可使用路線說明與進化表。'},
      'Build a privacy-safe recovery report': {'es':'Crea un informe de recuperación sin datos privados','it':'Crea un rapporto di recupero senza dati privati','zh-hant':'建立不含私密資料的救援報告'},
      'Choose only non-sensitive facts. This tool runs in your browser and does not inspect or upload a save.': {'es':'Elige solo datos no sensibles. La herramienta funciona en tu navegador y no revisa ni sube el guardado.','it':'Scegli solo dati non sensibili. Lo strumento funziona nel browser e non legge né carica il salvataggio.','zh-hant':'只選擇不敏感資訊；工具在瀏覽器中執行，不會檢查或上傳存檔。'},
      'Where the game was used': {'es':'Dónde se usó el juego','it':'Dove è stato usato il gioco','zh-hant':'遊戲使用位置'},
      'Device handoff': {'es':'Cambio de dispositivo','it':'Passaggio tra dispositivi','zh-hant':'裝置切換情境'},
      'iPad Safari → PC Chrome': {'es':'iPad Safari → PC Chrome','it':'iPad Safari → PC Chrome','zh-hant':'iPad Safari → PC Chrome'},
      'Android → PC': {'es':'Android → PC','it':'Android → PC','zh-hant':'Android → PC'},
      '>Other devices<': {'es':'>Otros dispositivos<','it':'>Altri dispositivi<','zh-hant':'>其他裝置<'},
      'Official pokesurvivor.com': {'es':'pokesurvivor.com oficial','it':'pokesurvivor.com ufficiale','zh-hant':'官方 pokesurvivor.com'},
      'Installed PWA from the official site': {'es':'PWA instalada desde el sitio oficial','it':'PWA installata dal sito ufficiale','zh-hant':'從官方網站安裝的 PWA'},
      'Another address or unknown': {'es':'Otra dirección o desconocida','it':'Altro indirizzo o non noto','zh-hant':'其他網址或不確定'},
      'Account state': {'es':'Estado de la cuenta','it':'Stato dell’account','zh-hant':'帳號狀態'},
      'Linked to Gmail': {'es':'Vinculada a Gmail','it':'Collegato a Gmail','zh-hant':'已綁定 Gmail'},
      'Google or linked account': {'es':'Google o cuenta vinculada','it':'Google o account collegato','zh-hant':'Google 或已綁定帳號'},
      'Other account type': {'es':'Otro tipo de cuenta','it':'Altro tipo di account','zh-hant':'其他帳號類型'},
      'Username/password; linkage unknown': {'es':'Usuario/contraseña; vínculo desconocido','it':'Nome utente/password; collegamento non noto','zh-hant':'帳號密碼；不確定是否綁定'},
      'Guest or unlinked': {'es':'Invitado o sin vincular','it':'Ospite o non collegato','zh-hant':'訪客或未綁定'},
      'Unknown': {'es':'No lo sé','it':'Non noto','zh-hant':'不確定'},
      'Surviving copy': {'es':'Copia que conserva el progreso','it':'Copia che conserva i progressi','zh-hant':'仍存有進度的副本'},
      'Original device still has complete progress': {'es':'El dispositivo original conserva todo el progreso','it':'Il dispositivo originale conserva tutti i progressi','zh-hant':'原裝置仍有完整進度'},
      '>Yes<': {'es':'>Sí<','it':'>Sì<','zh-hant':'>是<'},
      '>No<': {'es':'>No<','it':'>No<','zh-hant':'>否<'},
      'Original device save state': {'es':'Estado de guardado en el dispositivo original','it':'Stato del salvataggio sul dispositivo originale','zh-hant':'原裝置儲存狀態'},
      '>Saved locally<': {'es':'>Guardado localmente<','it':'>Salvato localmente<','zh-hant':'>本機已保存<'},
      '>Pending upload<': {'es':'>Subida pendiente<','it':'>Upload in attesa<','zh-hant':'>等待上傳<'},
      '>Syncing<': {'es':'>Sincronizando<','it':'>Sincronizzazione<','zh-hant':'>正在同步<'},
      '>Cloud save successful<': {'es':'>Guardado en la nube completado<','it':'>Salvataggio cloud completato<','zh-hant':'>雲端儲存成功<'},
      '>Offline<': {'es':'>Sin conexión<','it':'>Offline<','zh-hant':'>離線<'},
      'Second device shows the same collection': {'es':'El segundo dispositivo muestra la misma colección','it':'Il secondo dispositivo mostra la stessa collezione','zh-hant':'第二台裝置顯示相同收藏'},
      'Difference appeared': {'es':'La diferencia apareció','it':'La differenza è comparsa','zh-hant':'差異出現時間'},
      '>Before pressing Save<': {'es':'>Antes de pulsar Guardar<','it':'>Prima di premere Salva<','zh-hant':'>按下儲存之前<'},
      '>After pressing Save<': {'es':'>Después de pulsar Guardar<','it':'>Dopo aver premuto Salva<','zh-hant':'>按下儲存之後<'},
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
      'Build a privacy-safe co-op checklist': {'es':'Crea una lista co-op sin datos privados','it':'Crea una lista co-op senza dati privati','zh-hant':'建立不含私密資料的合作檢查清單'},
      'Choose only non-sensitive categories. This tool does not inspect your network, contact the game server or read an account.': {'es':'Elige solo categorías no sensibles. La herramienta no inspecciona tu red, no contacta al servidor y no lee cuentas.','it':'Scegli solo categorie non sensibili. Lo strumento non ispeziona la rete, non contatta il server e non legge account.','zh-hant':'只選擇不敏感的分類；工具不會檢查網路、不會連線遊戲伺服器，也不會讀取帳號。'},
      'Where the game is open': {'es':'Dónde está abierto el juego','it':'Dove è aperto il gioco','zh-hant':'遊戲從哪裡開啟'},
      'Official game opened directly': {'es':'Juego oficial abierto directamente','it':'Gioco ufficiale aperto direttamente','zh-hant':'直接開啟官方遊戲'},
      'Inside another site or copied version': {'es':'Dentro de otra web o copia','it':'Dentro un altro sito o una copia','zh-hant':'其他網站內嵌或複製版本'},
      'Not sure': {'es':'No lo sé','it':'Non so','zh-hant':'不確定'},
      'Stage that failed': {'es':'Fase que falla','it':'Fase del problema','zh-hant':'失敗的階段'},
      'Friend or invitation is missing': {'es':'Falta el amigo o la invitación','it':'Manca l’amico o l’invito','zh-hant':'沒有好友或邀請'},
      'Already playing: boss missing after a rift': {'es':'Partida iniciada: falta el jefe tras una grieta','it':'Partita iniziata: boss assente dopo un rift','zh-hant':'已在對局：裂縫後找不到 Boss'},
      'A move behaves unexpectedly': {'es':'Un movimiento se comporta de forma inesperada','it':'Una mossa si comporta in modo inatteso','zh-hant':'招式表現異常'},
      'Network comparison': {'es':'Comparación de redes','it':'Confronto reti','zh-hant':'網路對照'},
      'Not checked / not sure': {'es':'No comprobado / no lo sé','it':'Non verificato / non so','zh-hant':'未測試／不確定'},
      'Players are on the same network': {'es':'Los jugadores están en la misma red','it':'I giocatori sono sulla stessa rete','zh-hant':'玩家在同一網路'},
      'Players are on different networks': {'es':'Los jugadores están en redes diferentes','it':'I giocatori sono su reti diverse','zh-hant':'玩家在不同網路'},
      'Show safe checks': {'es':'Ver pasos seguros','it':'Mostra controlli sicuri','zh-hant':'查看安全步驟'},
      'Select the failed stage, then run the checklist.': {'es':'Elige la fase y ejecuta la lista.','it':'Scegli la fase ed esegui la lista.','zh-hant':'選擇失敗階段，再執行清單。'},
      'Non-sensitive checklist': {'es':'Lista sin datos sensibles','it':'Lista non sensibile','zh-hant':'不敏感檢查清單'},
      'Copy checklist': {'es':'Copiar lista','it':'Copia elenco','zh-hant':'複製檢查清單'},
      'Use the four-stage table below: friendship, room invitation, peer connection and running game. Open the official site directly, keep the host active, preserve site data and report only non-sensitive facts.': {'es':'Usa las cuatro fases: amistad, invitación, conexión y partida. Abre la web oficial, mantén activo al anfitrión, conserva los datos y comunica solo hechos no sensibles.','it':'Usa le quattro fasi: amicizia, invito, connessione e partita. Apri il sito ufficiale, mantieni attivo l’host, conserva i dati e comunica solo fatti non sensibili.','zh-hant':'依好友、房間邀請、網路連線及對局四階段檢查；直接開啟官方網站、讓房主保持前台、保留網站資料，且只回報不敏感資訊。'},
      'Move Master checklist': {'es':'Lista Move Master','it':'Lista Move Master','zh-hant':'Move Master 招式清單'},
      'Track the 97 move evolutions completed in this browser. This is a Wiki checklist, not a game save, cloud record or official achievement.': {'es':'Marca las 97 evoluciones completadas en este navegador. Es una lista de la Wiki, no un guardado, registro en la nube ni logro oficial.','it':'Segna le 97 evoluzioni completate in questo browser. È una lista della Wiki, non un salvataggio, registro cloud o obiettivo ufficiale.','zh-hant':'在此瀏覽器記錄 97 條已完成的招式進化；這是本站清單，不是遊戲存檔、雲端紀錄或官方成就。'},
      'Search moves': {'es':'Buscar movimientos','it':'Cerca mosse','zh-hant':'搜尋招式'},
      'Move or evolution': {'es':'Movimiento o evolución','it':'Mossa o evoluzione','zh-hant':'招式或進化'},
      '>Show<': {'es':'>Mostrar<','it':'>Mostra<','zh-hant':'>顯示<'},
      '>All recipes<': {'es':'>Todas las recetas<','it':'>Tutte le ricette<','zh-hant':'>全部配方<'},
      '>Incomplete<': {'es':'>Incompletas<','it':'>Incomplete<','zh-hant':'>未完成<'},
      '>Completed<': {'es':'>Completadas<','it':'>Completate<','zh-hant':'>已完成<'},
      'Loading checklist…': {'es':'Cargando lista…','it':'Caricamento lista…','zh-hant':'正在載入清單…'},
      '>Export JSON<': {'es':'>Exportar JSON<','it':'>Esporta JSON<','zh-hant':'>匯出 JSON<'},
      '>Import JSON<': {'es':'>Importar JSON<','it':'>Importa JSON<','zh-hant':'>匯入 JSON<'},
      '>Reset checklist<': {'es':'>Restablecer lista<','it':'>Azzera lista<','zh-hant':'>重設清單<'},
      'JavaScript is needed for the checklist. The complete static table remains below.': {'es':'La lista necesita JavaScript. La tabla estática completa sigue disponible abajo.','it':'La lista richiede JavaScript. La tabella statica completa resta disponibile sotto.','zh-hant':'清單需要 JavaScript；下方仍提供完整靜態表格。'},
      '>Option<': {'es':'>Opción<','it':'>Opzione<','zh-hant':'>方式<'},
      '>What it means<': {'es':'>Qué significa<','it':'>Cosa significa<','zh-hant':'>代表意義<'},
      '>Where to start<': {'es':'>Dónde empezar<','it':'>Da dove iniziare<','zh-hant':'>從哪裡開始<'},
      '>Browser game<': {'es':'>Juego en navegador<','it':'>Gioco nel browser<','zh-hant':'>瀏覽器遊戲<'},
      '>Play on desktop or mobile without a separate installer<': {'es':'>Juega en ordenador o móvil sin instalador separado<','it':'>Gioca su computer o mobile senza un installer separato<','zh-hant':'>免安裝即可在電腦或手機遊玩<'},
      '>Home-screen app / PWA<': {'es':'>Aplicación de inicio / PWA<','it':'>App schermata Home / PWA<','zh-hant':'>主畫面應用程式／PWA<'},
      '>A browser installation using the project’s manifest and cache<': {'es':'>Instalación del navegador que usa el manifiesto y la caché del proyecto<','it':'>Installazione del browser basata su manifest e cache del progetto<','zh-hant':'>使用專案 manifest 與快取的瀏覽器安裝<'},
      '>Your browser’s install or home-screen menu<': {'es':'>Menú Instalar o Añadir a inicio del navegador<','it':'>Menu Installa o Aggiungi alla schermata Home del browser<','zh-hant':'>瀏覽器的安裝或加入主畫面選單<'},
      '>Local source copy<': {'es':'>Copia local del código<','it':'>Copia locale del sorgente<','zh-hant':'>本機原始碼副本<'},
      '>Developer files; a separate origin and setup from the live game<': {'es':'>Archivos para desarrollo; origen y configuración distintos del juego público<','it':'>File per sviluppatori; origine e configurazione separate dal gioco pubblico<','zh-hant':'>開發用檔案；與正式遊戲使用不同來源與設定<'},
      '>The upstream GitHub repository<': {'es':'>Repositorio original de GitHub<','it':'>Repository GitHub originale<','zh-hant':'>上游 GitHub 儲存庫<'},
      '>APK or native port<': {'es':'>APK o adaptación nativa<','it':'>APK o port nativo<','zh-hant':'>APK 或原生移植版<'},
      '>A separate package whose author, version and compatibility need checking<': {'es':'>Paquete separado cuyo autor, versión y compatibilidad deben comprobarse<','it':'>Pacchetto separato: verifica autore, versione e compatibilità<','zh-hant':'>獨立套件，需核對作者、版本與相容性<'},
      '>Follow a specific developer announcement; no package is hosted here<': {'es':'>Sigue un anuncio concreto del desarrollador; aquí no se aloja ningún paquete<','it':'>Segui un annuncio specifico dello sviluppatore; qui non ospitiamo pacchetti<','zh-hant':'>依開發者明確公告操作；本站不代管套件<'},
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


LOCALIZED_DETAILS = {
 'es': {
  'save-recovery':'<section class="article-section"><h2>¿El guardado no se sincroniza entre iPad y PC?</h2><p>Usar la misma cuenta de Google no confirma que ambos dispositivos hayan cargado el mismo guardado. Conserva intacto el dispositivo que todavía mantiene el progreso. «Guardado en este navegador», «pendiente», «sincronizando», «guardado en la nube» y «cargado en el segundo dispositivo» son estados distintos.</p><p>La revisión oficial del 21 de octubre incorpora control de versiones. Si una copia antigua entra en conflicto con una revisión más nueva, el cliente puede leer la nube, combinar y volver a intentarlo. Es un cambio publicado; no garantiza recuperar progreso perdido ni autoriza a jugar en dos dispositivos a la vez.</p></section>',
  'co-op':'<section class="article-section"><h2>Fallos de conexión, retransmisión y desconexiones</h2><p>Las notas del 21 de octubre describen una ruta por servidor cuando la conexión directa falla. Una sala que nunca conecta y una partida que se desconecta después de empezar son síntomas distintos. La función publicada no demuestra que esta Wiki haya probado todas las cuentas y redes.</p></section>',
  'moves':'<section class="article-section"><h2>Del compañero a una ruta guardada</h2><ol><li>Elige un compañero que tengas o compara los 29 iniciales.</li><li>Comprueba movimientos legales y si usan Ataque o Ataque Especial.</li><li>Confirma la carta exacta de evolución.</li><li>Crea la build, compártela y espera el estado de guardado en la nube antes de cambiar de dispositivo.</li></ol></section>',
  'builds':'<section class="article-section"><h2>Del compañero a una ruta guardada</h2><ol><li>Elige un compañero que tengas o compara los 29 iniciales.</li><li>Comprueba movimientos legales y su estadística ofensiva.</li><li>Confirma la evolución antes de gastar cartas.</li><li>Comparte la ruta y espera la confirmación del guardado en la nube antes de cambiar de dispositivo.</li></ol></section>'
 },
 'it': {
  'save-recovery':'<section class="article-section"><h2>Il salvataggio cloud non si sincronizza tra iPad e PC?</h2><p>Usare lo stesso account Google non dimostra che entrambi i dispositivi abbiano caricato lo stesso salvataggio. Conserva il dispositivo che contiene ancora i progressi. Copia locale, upload in attesa, sincronizzazione, conferma nel cloud e caricamento sul secondo dispositivo sono stati distinti.</p><p>La revisione ufficiale del 21 ottobre aggiunge il controllo delle revisioni: in caso di conflitto il client può leggere il cloud, unire e riprovare. Non garantisce il recupero di progressi già persi e non rende sicuro giocare contemporaneamente su due dispositivi.</p></section>',
  'co-op':'<section class="article-section"><h2>Errori di connessione, relay e disconnessioni</h2><p>Le note del 21 ottobre descrivono un percorso tramite server quando la connessione diretta fallisce. Una stanza che non si connette e una partita che cade dopo l’avvio sono sintomi distinti. La funzione pubblicata non prova che questa Wiki abbia testato ogni account e rete.</p></section>'
 },
 'zh-hant': {
  'save-recovery':'<section class="article-section"><h2>iPad 與 PC 的 PokéSurvivor 雲端存檔沒有同步？</h2><p>使用同一個 Google 帳戶，不代表兩台裝置已載入同一份雲端資料。先保留仍有進度的裝置，分清「本機已保存」「等待上傳」「正在同步」「雲端已完成」及「另一台已載入」。排查時不要清除網站資料，也不要用較舊副本覆蓋仍保留的進度。</p><p>10 月 21 日官方加入存檔版本檢查；發生 revision 衝突時，程式可讀取雲端、合併再重試。這是已公布的程式改動，不代表本站能還原帳號，也不保證既有遺失內容會自動恢復。</p></section>',
  'co-op':'<section class="article-section"><h2>連線失敗、伺服器中繼與對局中斷</h2><p>10 月 21 日官方紀錄已描述無法直接連線時改走伺服器中繼的路徑。房間從未連上與對局開始後中斷是不同症狀；已公布功能不等於本站測遍所有帳號及網路。</p></section>',
  'tier-list':'<section class="article-section"><h2>先決定你在選哪一種角色</h2><p>本頁比較 966 名完整角色，不是 29 名免費開局榜，也不是 400 金幣起始招式列表。先按已持有角色、免費開局、物理或特殊輸出與操作距離縮小範圍，再查看合法招式及進化條件。高評分只代表資料屬性較高，不等於本站實測勝率或清怪效率。</p><p><a href="/zh-hant/starter-tier-list/">比較 29 名免費開局夥伴</a> · <a href="/zh-hant/moves/">查合法招式</a> · <a href="/zh-hant/move-evolutions/">查進化條件</a></p></section>'
 }
}


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
            body += LOCALIZED_DETAILS.get(locale,{}).get(slug,'')
            tool = _component(source['body'], 'data-(?:evolution|matchup|gacha|build-planner|save-diagnostic|coop-diagnostic)')
            tables = _all_tables(source['body'])
            if tool: body += localize_component(tool, locale)
            if slug == 'move-evolutions':
                tracker = _component(source['body'], 'data-move-master')
                if tracker: body += localize_component(tracker, locale)
            if tables: body += localize_component(tables, locale)
        item = deepcopy(source)
        item.update(title=title, description=description, body=body)
        if slug == '': item['preserve_media_layout']=True
        pages[slug] = item
    return pages
