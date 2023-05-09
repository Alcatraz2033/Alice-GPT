## Bienvenido a Alice-GPT

<p align="center">
	<img src="https://i.imgur.com/k8JJmHK.png" width="80%" height="80%" align="">
</p>

##

<h3><p align="center">Advertencia</p></h3>

Es importante tener en cuenta que los asistentes virtuales son herramientas útiles y prácticas, pero también pueden ser objeto de mal uso. Algunas personas pueden usarlos para acosar, intimidar o engañar a otros, mientras que otras pueden depender demasiado de ellos y descuidar habilidades importantes, como la comunicación interpersonal. Es importante recordar que los asistentes virtuales no son seres humanos y tienen limitaciones en su capacidad para entender el contexto y las emociones humanas. Por lo tanto, es esencial utilizar los asistentes virtuales de manera responsable y ética, respetando los límites y la privacidad de los demás.

##

## Alice-GPT ASISTENTE VIRTUAL
Alice es un asistente virtual que utiliza la API de Chat-GPT para ofrecer respuestas precisas y relevantes a las preguntas de los usuarios. Gracias a la potencia de la tecnología GPT, Alice puede analizar el contexto y el tono de la conversación para brindar una experiencia de usuario personalizada y satisfactoria. Ya sea que los usuarios necesiten ayuda con una tarea cotidiana, información sobre un tema específico o simplemente una conversación amigable, Alice está siempre lista para ayudar. Además, la API de Chat-GPT permite que Alice aprenda y se adapte continuamente a las necesidades y preferencias de los usuarios, brindando una experiencia de asistencia virtual cada vez más eficiente y efectiva.
<p align="center">
	<img src="https://i.imgur.com/Um78TkC.png" width="80%" height="80%" align="">
</p>
Alice solo está disponible actualmente en plataformas Linux.

# Habla con Alice
La palabra de activación es **Alice** seguido de lo que quieres preguntar. Por ejemplo:
* **Alice** quién es el presidente de Ecuador?
* Parece que va a llover, **Alice** cual es el pronóstico del clima en Ecuador?
* **Salir** (Esta palabra cierra la ejecución del programa.)

# Instalación
## Añade la API de CHAT-GPT a Alice.
<p align="center">
	<img src="https://i.imgur.com/eiQY7Qt.png" width="100%" height="100%" align="">
</p>

Entra a [CHAT-GPT API.](https://platform.openai.com/docs/guides/chat) Inicia secio o create una cuenta nueva. 

<p align="center">
	<img src="https://i.imgur.com/vmb7sUz.png" width="100%" height="100%" align="">
</p>

Clic en tu perfil y selecciona **View API Keys**.

<p align="center">
	<img src="https://i.imgur.com/JL2skX6.png" width="100%" height="100%" align="">
</p>
<p align="center">
	<img src="https://i.imgur.com/XBsIRM9.png" width="100%" height="100%" align="">
</p>

Crea una nueva **API Key** y cópiala.


<p align="center">
	<img src="https://i.imgur.com/givgVbh.png" width="100%" height="100%" align="">
</p>

Pégala dentro de **config.py**.

## Instalación Dependencias
### Clonar Repositorio
```markdown
git clone https://github.com/Alcatraz2033/Alice-GPT.git
cd Alice-GPT
```
### Instalar librerias Python
```markdown
pip install openai
pip install SpeechRecognition
pip install gtts
```
### Ejecución
```markdown
python3 chat_gpt.py 2>/dev/null
```
Al iniciar el programa se suele mostraer algo de ruido referente a la activación del micrófono. Para no ver estos errores, reedireccionamos todos los errores al **/dev/null**.
