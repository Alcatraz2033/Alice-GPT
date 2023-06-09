import openai, config, os, signal
from elevenlabs import generate, play
import speech_recognition as sr

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[39m'

alice = f"""{CYAN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣠⠤⡤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣶⠞⠋⢡⠀⠀⠀⢠⡀⠀⠉⠙⠲⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⢞⣉⡴⢁⡾⠁⠀⠀⢸⡆⠀⠀⠀⠉⠳⣦⡀⠀⠈⠋⠳⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡴⢟⡿⠋⠈⠀⣼⠁⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠀⠙⢶⣄⠀⠀⠀⠙⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⠟⢄⡞⠀⠀⠀⢨⡏⠀⠀⠀⠀⠀⠈⢷⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠂⠈⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⠿⢀⡞⠀⠀⠀⠀⢻⡇⠀⠀⠀⣀⣀⢀⡈⣇⠀⠀⠀⠀⠀⠀⠀⠀⠳⡄⠀⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⠟⠀⣾⠀⠀⠀⠐⠲⣼⡇⢀⠀⣾⡏⢹⣷⡀⢹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠹⡆⠀⠀⠀⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣾⠀⢸⠇⠀⢀⣀⣀⣠⠿⠿⠾⠷⢾⡇⢸⡟⠋⠛⠋⠉⠉⠙⠓⠒⠲⠶⠦⣼⢽⡄⠀⠀⠘⣇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣼⠋⠀⣿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠠⢿⡀⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣿⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠈⡷⢄⠀⢸⣇⠀⠀⠀⠀⠀⠀⠀
⠀⢸⠁⠸⢹⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣶⠀⢹⡀⠀⠈⣿⠀⠀⠀⠀⠀⠀⠀
⠀⣼⠀⠀⣿⣽⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⣿⢦⡜⢷⠄⠀⣿⡄⠀⠀⠀⠀⠀⠀
⢀⡏⠀⠀⣿⢺⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡿⠀⠀⠀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀
⢸⡇⠀⠀⣿⢼⡇{RED}⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀{CYAN}⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀
⣾⣿⠀⡀⢹⣼⡇{RED}⠀⠀⠀⠀⠀⣿⣿⠆⠀⠀⠐⠒⠒⠒⠀⠀⢼⣿⡷{CYAN}⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀
⣿⣿⣄⢣⠸⣿⡇{RED}⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁{CYAN}⠀⠀⠀⠀⠀⠀⡇⠀⠈⢳⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀
⣿⡇⣏⡄⣧⢺⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢸⠀⠀⣸⡇⠀⠀⠀⠀⠀⠀
⣿⣿⣿⡃⠈⠈⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢰⠀⢸⠀⠀⣾⡇⠀⠀⠀⠀⠀⠀
⢹⣧⢻⡆⠀⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢸⠀⢸⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀
⢸⣿⢸⡇⢠⣀⠻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⡿⠀⢸⠀⠀⢺⣷⠀⠀⠀⠀⠀⠀
⠈⣿⣆⡇⠀⢹⠀⡇{MAGENTA}ALICE⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀GPT{CYAN}⣧⡇⠀⢸⠀⠀⢸⢸⠀⠀⠀⠀⠀⠀
⠀⠸⣿⣧⠀⣾⡟⡷⢤⣤⣤⠴⣶⣶⣶⠶⣶⣶⣖⣲⠒⢒⣒⣶⣶⣷⣾⠒⣶⢲⠒⠲⣿⠇⠀⢸⠀⠄⣾⢸⠀⠀⠀⠀⠀⠀
⠀⠀⠹⣿⡄⢸⡇⢹⡄⠀⢹⠀⢸⡀⢾⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡿⢻⠀⣿⢸⡄⠀⡞⠀⠀⢸⢀⡄⣿⢺⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠙⣿⠀⡇⠐⣇⠀⢸⠀⠈⣇⢸⣇⣬⣿⣿⣹⣿⣿⣿⣿⠟⠀⢸⣤⣏⢸⠆⢠⡇⠀⠀⢸⠀⠁⢯⢸⣷⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⡆⣧⠀⠹⡄⠘⡇⠀⣿⣿⣿⣿⡟⢿⣿⣿⠿⠟⠁⠀⠀⠸⣿⣿⣿⣀⣾⠀⠀⠀⠸⠀⠀⠸⡖⢹⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢻⠀⣿⠀⠀⢧⢠⣧⣼⣿⣿⣿⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢹⣿⢹⣿⣶⣶⣤⣀⡀⠀⠀⢻⠘⡇⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠀⣹⣠⣴⣾⣾⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡿⣸⣿⣿⣿⣿⣿⣿⣿⣶⣾⣤⣷⠀⠀⠀⠀
⠀⠀⣀⣠⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⢀⣀⣀⣤⣄⣀⠀⠀⣾⣿⣷⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣽⣿⣿⣷⣤⡀
⣴⣿⣿⣿⣷⣶⣤⣤⣌⣙⣛⡻⠿⣿⣿⣿⣿⣿⡟⢛⣋⣉⣁⣈⡛⡿⣾⣿⣿⣿⣿⠟⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
            {MAGENTA}By: Alcatraz2033{RESET}
"""

def ctrl_c(sig, frame):
    print(f"\n[{RED}!{RESET}] {RED}SALIENDO...{RESET}")
    exit(1)
signal.signal(signal.SIGINT, ctrl_c)

def chat_gpt(query):
    openai.api_key = config.api_key
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content":query}])
        texto = response.choices[0].message.content
        #print(f"Respuesta: {texto}")
        text2voice(texto)
    except Exception as e:
        print(e)


def voice2text():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        ##print("Hable ahora:")
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language='es-ES')
        # print(f"Dijiste: {texto}")
        return texto
    except sr.UnknownValueError:
        text2voice("No te entiendo")
        return ''
    except sr.RequestError as e:
        text2voice(f"Error al conectarse con la API de Google: {e}")
        exit(1)

def text2voice(texto):
    audio = generate(
        text=texto,
        voice="Bella",
        model='eleven_multilingual_v1'
    )
    play(audio)

if '__main__' == __name__:
    print(alice)
    print(f"[{GREEN}+{RESET}] {GREEN}Habla con Alice{RESET}")
    while True:
        respuesta = voice2text()
        if respuesta == "salir":
            text2voice("Hasta pronto")
            exit(1)
        elif "Alice" in respuesta:
            posicion = respuesta.find("Alice") + 6
            nueva_respuesta = respuesta[posicion:]
            chat_gpt(nueva_respuesta)

