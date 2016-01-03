from constants import *

class Features:

    # initialise features
    def __init__(self, config_provider):

        text_to_speech = None
        if (config_provider.browser or config_provider.hand_gesture or
            config_provider.play_your_cards_right or config_provider.happy_colour or
            config_provider.optical_character_recognition):
            from shared import TextToSpeech
            text_to_speech = TextToSpeech()

        speech_to_text = None
        if config_provider.browser or config_provider.play_your_cards_right:
            from shared import SpeechToText
            speech_to_text = SpeechToText()

        self.browser = None
        if config_provider.browser:
            from browser import Browser
            self.browser = Browser(text_to_speech, speech_to_text)

        self.hand_gesture = None
        if config_provider.hand_gesture:
            from handgesture import HandGesture
            self.hand_gesture = HandGesture(text_to_speech)

        self.play_your_cards_right = None
        if config_provider.play_your_cards_right:
            from playyourcardsright import PlayYourCardsRight
            self.play_your_cards_right = PlayYourCardsRight(text_to_speech, speech_to_text)

        self.happy_colour = None
        if config_provider.happy_colour:
            from happycolour import HappyColour
            self.happy_colour = HappyColour(text_to_speech)

        self.optical_character_recognition = None
        if config_provider.optical_character_recognition:
            from opticalcharacterrecognition import OpticalCharacterRecognition
            self.optical_character_recognition = OpticalCharacterRecognition(text_to_speech)

        self.television = None
        if config_provider.television:
            from television import Television
            self.television = Television()

    # indicate whether a feature is speaking
    def is_speaking(self):
        return ((self.browser and self.browser.is_speaking) or
                (self.hand_gesture and self.hand_gesture.is_speaking) or
                (self.play_your_cards_right and self.play_your_cards_right.is_speaking) or
                (self.happy_colour and self.happy_colour.is_speaking) or
                (self.optical_character_recognition and self.optical_character_recognition.is_speaking))

    # provide emotion from a feature
    def get_emotion(self):
        if self.hand_gesture: 
            return self.hand_gesture.emotion
        elif self.happy_colour: 
            return self.happy_colour.emotion
        else:
            return None

    # update background image from a feature
    def update_background_image(self, image):
        if self.television and self.television.background_image.size > 0: 
            return self.television.background_image
        else:
            return image

    # handle features
    def handle(self, rocky_robot, sporty_robot, image):
        self._handle_browser(rocky_robot, sporty_robot)
        self._handle_hand_gesture(rocky_robot, sporty_robot, image)
        self._handle_play_your_cards_right(sporty_robot)
        self._handle_happy_colour(rocky_robot, image)
        self._handle_optical_character_recognition(rocky_robot, sporty_robot, image)
        self._handle_television(rocky_robot, sporty_robot, image)

    # handle browser
    def _handle_browser(self, rocky_robot, sporty_robot):
        if not self.browser: return

        if rocky_robot.is_facing:
            self.browser.start(ROCK)
        elif sporty_robot.is_facing:
            self.browser.start(SPORT)
        else:
            self.browser.stop()

    # handle hand gesture
    def _handle_hand_gesture(self, rocky_robot, sporty_robot, image):
        if not self.hand_gesture: return

        if rocky_robot.is_facing or sporty_robot.is_facing:
            self.hand_gesture.start(image)
        else:
            self.hand_gesture.stop()

    # handle play your cards right
    def _handle_play_your_cards_right(self, sporty_robot):
        if not self.play_your_cards_right: return

        if sporty_robot.is_facing:
            self.play_your_cards_right.start()
        else:
            self.play_your_cards_right.stop()

    # handle happy colour
    def _handle_happy_colour(self, rocky_robot, image):
        if not self.happy_colour: return

        if rocky_robot.is_facing:
            self.happy_colour.start(image)
        else:
            self.happy_colour.stop()

    # handle optical character recognition
    def _handle_optical_character_recognition(self, rocky_robot, sporty_robot, image):
        if not self.optical_character_recognition: return

        if rocky_robot.is_facing or sporty_robot.is_facing:
            self.optical_character_recognition.start(image)
        else:
            self.optical_character_recognition.stop()

    # handle television
    def _handle_television(self, rocky_robot, sporty_robot, image):
        if not self.television: return

        if rocky_robot.is_rendered or sporty_robot.is_rendered:
            self.television.start(image)
        else:
            self.television.stop()