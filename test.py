from playsound import playsound

def play_sound(count):
    pygame.init()
    sound = pygame.mixer.Sound("alarm.wav")
    for i in range(count):
        sound.play(count - 1)

playsound("alarm.wav")