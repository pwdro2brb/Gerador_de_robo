# 🦾 Treinador de Robôs RPA (V2.2)

> Gravador de processos, revisor visual e gerador automático de automações Python com suporte a coordenadas adaptativas.

https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/PyAutoGUI-Automation-FF6F00?style=for-the-badge
https://img.shields.io/badge/Pynput-Event_Hooking-blue?style=for-the-badge
https://img.shields.io/badge/Schema-JSON_State-000000?style=for-the-badge

---

# 🎯 Visão Geral do Projeto

O **Treinador de Robôs RPA** foi desenvolvido para acelerar a criação de automações desktop através da gravação de processos executados pelo usuário.

Em vez de mapear coordenadas, teclas e tempos manualmente, o usuário simplesmente executa o processo normalmente enquanto o sistema registra cada interação.

Após a gravação, um módulo de revisão permite editar, reorganizar, validar e testar as etapas antes da geração automática do script Python final.

Na versão **V2.2**, o projeto introduz:

- Execução individual de etapas.
- Execução parcial do fluxo.
- Preview visual das capturas de tela.
- Estatísticas da gravação.
- Metadados do ambiente.
- Coordenadas adaptativas para diferentes resoluções.

---

# ⚙️ Arquitetura do Pipeline

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
        ├── Delays
        ├── Screenshots
        ├── Janela Ativa
        └── Metadados do Ambiente
        │
        ▼
[ Interface de Revisão ]
        │
        ├── Edição
        ├── Duplicação
        ├── Exclusão
        ├── Reordenação
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

# ✨ Funcionalidades Principais

## ⏺️ 1. Motor de Gravação

### Mouse Tracking

- Captura de cliques esquerdo, direito e central.
- Registro de coordenadas da ação.
- Consolidação inteligente de eventos de scroll.

### Keylogging Estruturado

- Captura de texto digitado.
- Tratamento automático de Backspace.
- Armazenamento apenas do texto resultante.

### Teclas Especiais

Suporte para:

- Enter
- Tab
- Esc
- Delete
- Setas direcionais
- Home
- End
- Page Up
- Page Down

### Context Awareness

Captura automática de:

- Delay entre etapas
- Janela ativa
- Timestamp
- Screenshot da ação

### Metadados do Ambiente

Registro automático de:

- Resolução da tela
- Escala DPI
- Sistema operacional

### Coordenadas Adaptativas

Além das coordenadas absolutas:

```json
{
  "x": 1558,
  "y": 175
}
```

também são registradas coordenadas percentuais:

```json
{
  "x_percent": 0.811458,
  "y_percent": 0.162037
}
```

Permitindo maior compatibilidade em resoluções diferentes.

---

## 🛠️ 2. Módulo de Revisão

O revisor permite alterar a gravação antes da geração do script final.

### Edição

- Coordenadas X/Y
- Delay
- Texto digitado
- Intensidade de scroll
- Status da etapa

### Organização

- Duplicar etapas
- Excluir etapas
- Mover para cima
- Mover para baixo

### Execução

- Executar etapa individual
- Executar a partir da etapa selecionada

### Visualização

- Preview de screenshots
- Descrição da etapa
- Resumo da gravação

### Estatísticas

Exibição automática de:

- Total de ações
- Quantidade de cliques
- Quantidade de textos
- Quantidade de teclas
- Quantidade de scrolls
- Tempo estimado da execução

---

## 🐍 3. Geração Automática de Código

O sistema converte automaticamente o fluxo aprovado em um script Python executável.

Características:

- Código limpo e organizado.
- Compatibilidade com PyAutoGUI.
- Delays preservados.
- Suporte a teclas especiais.
- Suporte a atalhos.
- Compatível com gravações antigas.
- Suporte a coordenadas adaptativas.

Exemplo gerado:

```python
x, y = coordenada_adaptada(
    0.811458,
    0.162037
)

pyautogui.click(
    x,
    y,
    button="left"
)
```

---

# 🆕 Novidades da Versão V2.2

## ✅ Revisor Aprimorado

- Duplicação de etapas.
- Execução individual.
- Execução parcial.
- Preview visual das ações.
- Estatísticas em tempo real.

## ✅ Adaptação Automática de Resolução

O sistema agora registra:

- Resolução do monitor.
- Escala DPI.
- Coordenadas absolutas.
- Coordenadas percentuais.

Durante a execução, os cliques podem ser recalculados dinamicamente para posições equivalentes em telas diferentes.

---

# 📂 Estrutura de Saída

Após a gravação:

```text
robos_treinados/
└── meu_processo/
    ├── meu_processo.json
    ├── meu_processo_revisado.json
    ├── meu_processo.py
    ├── meu_processo_revisado.py
    └── prints/
        ├── click_001.png
        ├── tecla_002.png
        └── ...
```

### Arquivos Gerados

| Arquivo | Finalidade |
|----------|------------|
| processo.json | Fluxo original gravado |
| processo_revisado.json | Fluxo após edição |
| processo.py | Script gerado automaticamente |
| processo_revisado.py | Script final revisado |
| prints/ | Evidências visuais das etapas |

---

# 🛠️ Tecnologias Utilizadas

- Python 3.10+
- tkinter
- pynput
- pyautogui
- pillow
- pygetwindow
- json
- ctypes
- platform

---

# 🚧 Roadmap

## ✅ V2.0

- Gravação de mouse
- Gravação de teclado
- Captura de screenshots
- Exportação JSON
- Geração automática de código

## ✅ V2.1

- Duplicação de etapas
- Execução individual
- Execução parcial
- Preview de screenshots
- Estatísticas da gravação

## ✅ V2.2

- Metadados do ambiente
- Coordenadas percentuais
- Coordenadas adaptativas
- Compatibilidade entre resoluções

## ⏳ V3

- Captura de elementos visuais
- Localização por imagem
- Fallback entre imagem e coordenadas
- Espera inteligente baseada em elementos da tela

## 🔮 V4

- Fluxograma automático
- Detecção de padrões repetidos
- Sugestões automáticas de otimização
- Estruturas de repetição

---

# 🚀 Como Executar o Projeto

## Pré-requisitos

- Python 3.10+
- Windows

## Clone o repositório

```bash
git clone https://github.com/pwdro2brb/treinador-de-robos.git

cd treinador-de-robos
```

## Instale as dependências

```bash
pip install pyautogui
pip install pynput
pip install pillow
pip install pygetwindow
```

## Executar

```bash
python treinador_robos.py
```

## Encerrar gravação

Durante a gravação:

```text
Pressione F12
```

para finalizar e abrir o revisor de etapas.

---

# 📄 Licença

Projeto desenvolvido para estudos e automação de processos RPA utilizando Python.