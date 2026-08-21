    # 🦾 RPA Process Recorder & Code Generator (V2.2)

    > Ferramenta para gravação de eventos de periféricos (mouse e teclado), revisão visual de etapas e geração automática de scripts executáveis em Python (`pyautogui`).

    ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
    ![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-FF6F00?style=for-the-badge)
    ![Pynput](https://img.shields.io/badge/Pynput-Event_Hooking-blue?style=for-the-badge)
    ![JSON](https://img.shields.io/badge/Schema-JSON_State-000000?style=for-the-badge)

    ---

       ## 🎯 Visão Geral do Projeto

    O **Process Recorder & Code Generator** é uma ferramenta para captura, revisão e geração automática de automações em Python utilizando `pyautogui`.

    O usuário simplesmente executa um processo real enquanto o sistema registra cliques, teclas, textos digitados, rolagens e contexto da execução.

    A versão **V2.2** introduz recursos avançados de revisão, execução parcial do fluxo e adaptação automática de coordenadas para diferentes resoluções de tela, aumentando significativamente a portabilidade das automações geradas.

    ---

    ## ⚙️ Arquitetura do Pipeline

    ```text
    [ Ações do Usuário ]
            │
            ▼
    (Event Hooking via pynput)
            │
            ▼
    [ Captura & Serialização ]
            │
            ├── Coordenadas Absolutas
            ├── Coordenadas Percentuais
            ├── Screenshots
            └── Metadados do Ambiente
            │
            ▼
    [ Interface de Revisão ]
            │
            ├── Edição
            ├── Duplicação
            ├── Execução Individual
            ├── Execução Parcial
            └── Preview das Capturas
            │
            ▼
    [ Code Generator ]
            │
            ├── Python
            ├── PyAutoGUI
            └── Coordenadas Adaptativas
            │
            ▼
    [ Robô Final ]
    ```
    ---

    ## ✨ Funcionalidades Principais

    ### ⏺️ 1. Motor de Gravação
    * **Mouse Tracking:** Captura cliques (esquerdo/direito), movimentações e consolidação inteligente de scrolls consecutivos.
    * **Keylogging Estruturado:** Gravação de digitação de texto com tratamento dinâmico de `Backspace` para salvar apenas a string corrigida.
    * **Teclas Especiais:** Detecção de teclas de controle (`Enter`, `Tab`, `Esc`, setas direcionais, atalhos).
    * **Context Awareness:** Captura de tempo decorrido entre etapas (*delays* reais), janela ativa no sistema operacional e *screenshots* de referência.
    * **Metadados do Ambiente:** Registro automático de resolução da tela, escala DPI e sistema operacional.
    * **Coordenadas Adaptativas:** Armazenamento de coordenadas absolutas e percentuais para compatibilidade entre diferentes resoluções.

    ### 🛠️ 2. Módulo de Revisão e Calibração

    * Ajuste de coordenadas `(X,Y)`.
    * Alteração de textos digitados.
    * Alteração de intensidade de scroll.
    * Modificação de delays.
    * Ativação e desativação de etapas.
    * Exclusão de ações desnecessárias.
    * Duplicação rápida de etapas.
    * Reordenação de etapas.
    * Execução individual da etapa selecionada.
    * Execução do fluxo a partir do ponto selecionado.
    * Visualização de screenshots capturados durante a gravação.
    * Estatísticas automáticas da sessão.

    ### 🐍 3. Geração de Código

    * Compilação automática para Python.
    * Geração de scripts utilizando `pyautogui`.
    * Compatibilidade com gravações antigas.
    * Adaptação automática de coordenadas entre diferentes resoluções de tela.
    * Geração de código limpo e legível.

    ---

    ## 🆕 Novidades da Versão V2.2

    ### ✅ Revisor Aprimorado

    - Duplicação de etapas.
    - Execução individual.
    - Execução a partir do ponto selecionado.
    - Preview visual das ações capturadas.
    - Estatísticas em tempo real.

    ### ✅ Adaptação Automática de Resolução

    O sistema passa a registrar:

    - Resolução do monitor.
    - Escala DPI.
    - Coordenadas absolutas.
    - Coordenadas percentuais.

    Na geração do script, os cliques podem ser recalculados dinamicamente, permitindo maior compatibilidade entre máquinas com resoluções diferentes.

    Exemplo:

    ```json
    {
    "x": 1558,
    "y": 175,
    "x_percent": 0.811458,
    "y_percent": 0.162037
    }

    ---

    ## 🛠️ Tecnologias Utilizadas

    * **Linguagem:** Python 3.10+
    * **Captura de Eventos (Hooks globais):** `pynput`
    * **Mecanismo de Automação Gerado:** `pyautogui`
    * **Armazenamento de Estado:** `json`
    * **Manipulação de Telas & Imagens:** `pillow`

    ---


    ## 🚧 Roadmap

    ### V2.2 ✅
    - Execução de etapas individuais
    - Execução parcial do fluxo
    - Preview de screenshots
    - Estatísticas da gravação
    - Coordenadas adaptativas
    - Metadados do ambiente

    ### V3 ⏳
    - Captura de elementos visuais
    - Localização por imagem
    - Fallback entre imagem e coordenadas
    - Espera inteligente por elementos da tela

    ### V4 🔮
    - Fluxograma automático
    - Detecção de padrões repetidos
    - Sugestões de otimização do processo

    ---

    ## 🚀 Como Executar o Projeto Localmente

    ### Pré-requisitos
    Certifique-se de ter o Python 3 instalado no sistema.

    1. **Clone o repositório:**
    ```bash
    git clone [https://github.com/pwdro2brb/treinador-de-robos.git](https://github.com/pwdro2brb/treinador-de-robos.git)
    cd treinador-de-robos
