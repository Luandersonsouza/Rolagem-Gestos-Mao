import cv2
import mediapipe as mp
import pyautogui
#import time

class HandGestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.hand_landmarks = None
        self.scroll_speed = 50
        self.scrolling = False

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

    def perform_scroll(self, gesture):
        if gesture == "scroll_up":
            pyautogui.scroll(self.scroll_speed)
        elif gesture == "scroll_down":
            pyautogui.scroll(-self.scroll_speed)

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
                #self.mp_drawing.draw_landmarks(frame, self.hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                if not self.scrolling:
                    self.scrolling = True
                    print("Mão detectada -  Iniciando rolagem!")

            else:
                if self.scrolling:
                    self.scrolling = False
                    print("Mão não detectada - Parando rolagem!")

            if self.scrolling:
                hand_position = self.get_hand_position()
                if hand_position and len(hand_position) >= 5:
                    average_y = sum([hand_position[i][1] for i in range(2, 5)]) / 3
                    buffer_threshold = 10

                    if average_y < (self.screen_height // 2 - buffer_threshold):
                        self.perform_scroll("scroll_up")
                        print("Rolando para Cima!")
                    elif average_y > (self.screen_height // 2 + buffer_threshold):
                        self.perform_scroll("scroll_down")
                        print("Rolando para Baixo!")
            cv2.imshow("Hand Gesture Control", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # Pressione 'Esc' para sair
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    gesture_controller = HandGestureController()
    gesture_controller.run()
