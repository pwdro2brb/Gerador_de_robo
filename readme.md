# Treinador de Robôs MRV - V2

O Treinador de Robôs é uma ferramenta experimental integrada ao Hub Central MRV para gravar ações do usuário, revisar etapas e gerar um script Python base para automatizar processos repetitivos.

A versão V2 adiciona um revisor de etapas, permitindo corrigir ações gravadas antes de gerar o script final.

---

## Objetivo

Permitir que usuários gravem processos simples feitos no computador e transformem essas ações em um script automatizado usando `pyautogui`.

O robô registra ações como:

- cliques do mouse;
- textos digitados;
- teclas especiais;
- rolagem do mouse;
- tempo entre ações;
- janela ativa;
- prints durante a gravação.

Depois da gravação, o usuário pode revisar as etapas antes de gerar o código final.

---

## Funcionalidades da V2

- Gravação de cliques do mouse.
- Gravação de textos digitados.
- Tratamento básico de `Backspace`, salvando o texto final corrigido.
- Gravação de teclas como `Enter`, `Tab`, `Esc`, setas e outras.
- Gravação de scroll do mouse.
- Consolidação de scrolls consecutivos.
- Captura de prints durante a gravação.
- Geração de arquivo `.json` com as etapas gravadas.
- Geração de script `.py` com `pyautogui`.
- Tela de revisão das etapas.
- Edição de texto digitado.
- Edição de delay.
- Edição de coordenadas X/Y.
- Edição manual da intensidade do scroll.
- Exclusão de etapas.
- Duplicação de etapas.
- Ativação/desativação de etapas.
- Geração de script revisado.

---

## Dependências

Instale as bibliotecas necessárias:

```bash
pip install pynput pyautogui