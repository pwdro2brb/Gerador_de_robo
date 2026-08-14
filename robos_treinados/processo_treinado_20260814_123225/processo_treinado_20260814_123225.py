import time
import pyautogui


def executar_robo_treinado():
    print('Iniciando robô treinado...')
    time.sleep(2)

    time.sleep(1.4)
    pyautogui.click(591, 167, button='left')

    time.sleep(5.126)
    pyautogui.moveTo(1198, 455)
    pyautogui.scroll(-470)

    time.sleep(0.899)
    pyautogui.click(472, 570, button='left')

    time.sleep(1.864)
    pyautogui.click(511, 615, button='left')

    time.sleep(92.112)
    pyautogui.click(713, 322, button='left')

    time.sleep(2.224)
    pyautogui.click(537, 764, button='left')

    time.sleep(2.24)
    pyautogui.click(703, 844, button='left')

    time.sleep(2.684)
    pyautogui.moveTo(705, 850)
    pyautogui.scroll(-90)

    time.sleep(1.124)
    pyautogui.click(400, 598, button='left')

    print('Robô treinado finalizado.')


if __name__ == '__main__':
    executar_robo_treinado()