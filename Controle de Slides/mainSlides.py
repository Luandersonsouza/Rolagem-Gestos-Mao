import cv2
import mediapipe as mp
import pyautogui

class HandGestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.hand_landmarks = None
        self.scrolling = False
        self.slide_advance_threshold = 200  # Ajuste conforme necessário

    def detect_hand_landmarks(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            self.hand_landmarks = results.multi_hand_landmarks[0]
            return True
        else:
            self.hand_landmarks = None
            return False

    def get_hand_position(self):
        if self.hand_landmarks:
            return [(lm.x * self.screen_width, lm.y * self.screen_height) for lm in self.hand_landmarks.landmark]
        else:
            return []

    def perform_slide_action(self, gesture):
        if gesture == "slide_forward":
            pyautogui.press("right")  # Pressiona a seta para a direita (avança slide)
        elif gesture == "slide_backward":
            pyautogui.press("left")  # Pressiona a seta para a esquerda (retrocede slide)

    def run(self):
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Erro ao capturar o frame.")
                break

            frame = cv2.flip(frame, 1)
            hand_detected = self.detect_hand_landmarks(frame)

            if hand_detected:
                self.mp_drawing.draw_landmarks(frame, self.hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                if not self.scrolling:
                    self.scrolling = True
                    print("Iniciando controle de slides!")

            else:
                if self.scrolling:
                    self.scrolling = False
                    print("Parando controle de slides!")

            if self.scrolling:
                hand_position = self.get_hand_position()
                if hand_position and len(hand_position) >= 5:
                    hand_x = hand_position[8][0]  # Posição x do dedo indicador

                    if hand_x > self.screen_width - self.slide_advance_threshold:
                        self.perform_slide_action("slide_forward")
                        print("Avançando slide!")

                    elif hand_x < self.slide_advance_threshold:
                        self.perform_slide_action("slide_backward")
                        print("Retrocedendo slide!")

            cv2.imshow("Hand Gesture Control", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # Pressione 'Esc' para sair
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    gesture_controller = HandGestureController()
    gesture_controller.run()