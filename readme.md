# 🦾 RPA Process Recorder & Code Generator (V2)

> Ferramenta para gravação de eventos de periféricos (mouse e teclado), revisão visual de etapas e geração automática de scripts executáveis em Python (`pyautogui`).

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-FF6F00?style=for-the-badge)
![Pynput](https://img.shields.io/badge/Pynput-Event_Hooking-blue?style=for-the-badge)
![JSON](https://img.shields.io/badge/Schema-JSON_State-000000?style=for-the-badge)

---

## 🎯 Visão Geral do Projeto

O **Process Recorder & Code Generator** foi desenvolvido para acelerar a esteira de criação de robôs RPA. Em vez de mapear manualmente coordenadas de tela, pausas e sequências de teclas, o usuário simplesmente executa o processo real no computador enquanto o sistema intercepta os eventos em segundo plano.

Na versão **V2**, o projeto introduz uma **camada de revisão e refinamento**, permitindo calibrar coordenadas, tempos de espera e comandos antes de compilar o arquivo final em Python.

---

## ⚙️ Arquitetura do Pipeline

```text
[ Ações do Usuário ] 
       │
       ▼ (Event Hooking via pynput)
[ Captura & Serialização ] ──► Gera `fluxo_gravado.json` (com metadados e prints)
       │
       ▼
[ Interface de Revisão V2 ] ──► Ajuste de delays, coordenadas, duplicar/remover etapas
       │
       ▼ (Code Generation Engine)
[ Script Python Final ] ──────► Automação autônoma pronta em `pyautogui`
```
---

## ✨ Funcionalidades Principais

### ⏺️ 1. Motor de Gravação
* **Mouse Tracking:** Captura cliques (esquerdo/direito), movimentações e consolidação inteligente de scrolls consecutivos.
* **Keylogging Estruturado:** Gravação de digitação de texto com tratamento dinâmico de `Backspace` para salvar apenas a string corrigida.
* **Teclas Especiais:** Detecção de teclas de controle (`Enter`, `Tab`, `Esc`, setas direcionais, atalhos).
* **Context Awareness:** Captura de tempo decorrido entre etapas (*delays* reais), janela ativa no sistema operacional e *screenshots* de referência.

### 🛠️ 2. Módulo de Revisão e Calibração (V2)
* **Ajuste Fino de Ações:** Edição manual de coordenadas `(X, Y)`, alteração do texto digitado e intensidade da rolagem (*scroll*).
* **Controle de Fluxo:** Desativação temporária ou exclusão de etapas desnecessárias sem perder o restante da gravação.
* **Manipulação de Etapas:** Duplicação rápida de blocos de passos repetitivos.
* **Ajuste de Latência:** Modificação dos tempos de pausa (*sleep/delay*) para otimizar a velocidade de execução.

### 🐍 3. Geração de Código
* Compilação das etapas aprovadas em um script `.py` limpo, formatado e documentado utilizando `pyautogui` e tratamento de exceções.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Captura de Eventos (Hooks globais):** `pynput`
* **Mecanismo de Automação Gerado:** `pyautogui`
* **Armazenamento de Estado:** `json`
* **Manipulação de Telas & Imagens:** `pillow`

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
Certifique-se de ter o Python 3 instalado no sistema.

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/pwdro2brb/treinador-de-robos.git](https://github.com/pwdro2brb/treinador-de-robos.git)
   cd treinador-de-robos
