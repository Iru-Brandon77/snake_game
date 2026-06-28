<h1>Juego de la Serpiente</h1>

El software se desarrollo con Python con pygame, organizada en capas (arquitectura tipo clean architecture: domain, application, persistence, presentation).
<h1>Version de Python: </h1>
<li>Python 3.10.6</li>
<h1>Funcionalidades principales:</h1>
<li>Movimiento y crecimiento de la serpiente con detección de colisiones (consigo misma, con los bordes del tablero y con obstáculos).
Obstáculos generados aleatoriamente en cada partida, dejando una zona segura alrededor del punto de inicio.
<li>Sistema de comida con múltiples tipos (normal, dorada y "mala"), manejado mediante un diccionario de propiedades (FOOD_TYPES): cada tipo tiene su propio color, puntaje, efecto de crecimiento y si es temporal o no. Pueden aparecer varias comidas en pantalla a la vez</li>
<li>Puntaje y récord persistente: el high score se guarda en un archivo highscore.json y se recupera automáticamente al iniciar el juego.
<li>Audio generado por código: música de fondo y sonido de "muerte" creados con numpy, sin depender de archivos .mp3 o .wav.
<li>Feedback visual animado: al comer una comida aparece un texto flotante (+10, -10, etc.) que sube y se desvanece, dando retroalimentación inmediata del puntaje ganado o perdido.
<h3>El juego pueden descargarlo en los <a href="https://github.com/Iru-Brandon77/snake_game/releases">Releases</a></h3>
