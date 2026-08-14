import time
import pyautogui


def executar_robo_treinado():
    print('Iniciando robô treinado...')
    time.sleep(2)

    time.sleep(1.559)
    pyautogui.click(1592, 167, button='left')

    time.sleep(0.632)
    pyautogui.click(1297, 171, button='left')

    time.sleep(5.129)
    pyautogui.press('enter')

    time.sleep(2.159)
    pyautogui.click(1288, 760, button='left')

    time.sleep(1.744)
    pyautogui.click(1609, 159, button='left')

    time.sleep(0.536)
    pyautogui.click(1385, 175, button='left')

    time.sleep(4.136)
    pyautogui.press('enter')

    time.sleep(1.823)
    pyautogui.click(1596, 173, button='left')

    time.sleep(0.632)
    pyautogui.click(1263, 167, button='left')

    time.sleep(0.368)
    pyautogui.press('backspace')

    time.sleep(0.4)
    pyautogui.press('enter')

    print('Robô treinado finalizado.')


if __name__ == '__main__':
    executar_robo_treinado()