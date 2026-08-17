import os
import json
import time
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path

import pyautogui
from pynput import mouse, keyboard

try:
    import pygetwindow as gw
except Exception:
    gw = None


class TreinadorRobos:
    def __init__(self, pasta_saida=None, capturar_prints=True):
        self.pasta_saida = Path(pasta_saida or "robos_treinados")
        self.pasta_saida.mkdir(parents=True, exist_ok=True)

        self.capturar_prints = capturar_prints
        self.pasta_prints = None

        self.acoes = []
        self.gravando = False
        self.tempo_ultima_acao = None
        self.buffer_texto = ""

        self.mouse_listener = None
        self.keyboard_listener = None

        self.nome_processo = None
        self.pasta_processo = None
        self.arquivo_json = None
        self.arquivo_json_revisado = None
        self.arquivo_py = None
        self.arquivo_py_revisado = None

    # ==========================================================
    # CONTROLE PRINCIPAL
    # ==========================================================
    def iniciar_gravacao(self, nome_processo=None):
        if self.gravando:
            print("Já existe uma gravação em andamento.")
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.nome_processo = nome_processo or f"processo_treinado_{timestamp}"

        self.pasta_processo = self.pasta_saida / self.nome_processo
        self.pasta_processo.mkdir(parents=True, exist_ok=True)

        self.arquivo_json = self.pasta_processo / f"{self.nome_processo}.json"
        self.arquivo_json_revisado = self.pasta_processo / f"{self.nome_processo}_revisado.json"
        self.arquivo_py = self.pasta_processo / f"{self.nome_processo}.py"
        self.arquivo_py_revisado = self.pasta_processo / f"{self.nome_processo}_revisado.py"

        if self.capturar_prints:
            self.pasta_prints = self.pasta_processo / "prints"
            self.pasta_prints.mkdir(parents=True, exist_ok=True)

        self.acoes = []
        self.buffer_texto = ""
        self.tempo_ultima_acao = time.time()
        self.gravando = True

        print("=" * 70)
        print("TREINADOR DE ROBÔS V2 INICIADO")
        print("Faça o processo normalmente.")
        print("Pressione F12 para parar a gravação.")
        print("Evite digitar senhas enquanto a gravação estiver ativa.")
        print("=" * 70)

        self._registrar_acao({
            "tipo": "inicio",
            "janela": self._janela_ativa(),
            "mensagem": "Início da gravação"
        })

        self.mouse_listener = mouse.Listener(
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )

        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press
        )

        self.mouse_listener.start()
        self.keyboard_listener.start()

        self.keyboard_listener.join()

    def parar_gravacao(self):
        if not self.gravando:
            return

        self._flush_texto()

        self._registrar_acao({
            "tipo": "fim",
            "janela": self._janela_ativa(),
            "mensagem": "Fim da gravação"
        })

        self.gravando = False

        try:
            if self.mouse_listener:
                self.mouse_listener.stop()
        except Exception:
            pass

        try:
            if self.keyboard_listener:
                self.keyboard_listener.stop()
        except Exception:
            pass

        self.acoes = self._consolidar_scrolls(self.acoes)

        self.salvar_json(self.arquivo_json, self.acoes)
        self.gerar_script_py(self.arquivo_py, self.acoes)

        print("=" * 70)
        print("GRAVAÇÃO FINALIZADA")
        print(f"JSON salvo em: {self.arquivo_json}")
        print(f"Script base gerado em: {self.arquivo_py}")
        print("Abrindo revisor de etapas...")
        print("=" * 70)

        self.abrir_revisor()

    # ==========================================================
    # CAPTURA DE EVENTOS
    # ==========================================================
    def _on_click(self, x, y, button, pressed):
        if not self.gravando:
            return

        if not pressed:
            return

        self._flush_texto()

        nome_botao = str(button).replace("Button.", "")

        acao = {
            "tipo": "click",
            "x": int(x),
            "y": int(y),
            "botao": nome_botao,
            "janela": self._janela_ativa()
        }

        self._registrar_acao(acao)
        print(f"Click gravado: {nome_botao} em X={x}, Y={y}")

    def _on_scroll(self, x, y, dx, dy):
        if not self.gravando:
            return

        self._flush_texto()

        acao = {
            "tipo": "scroll",
            "x": int(x),
            "y": int(y),
            "dx": int(dx),
            "dy": int(dy),
            "scroll_amount": int(dy) * 10,
            "janela": self._janela_ativa()
        }

        self._registrar_acao(acao)

        direcao = "cima" if dy > 0 else "baixo"
        print(f"Scroll gravado para {direcao}: dy={dy} em X={x}, Y={y}")

    def _on_key_press(self, key):
        if not self.gravando:
            return

        if key == keyboard.Key.f12:
            print("F12 detectado. Encerrando gravação...")
            self.parar_gravacao()
            return False

        if key == keyboard.Key.backspace:
            if self.buffer_texto:
                self.buffer_texto = self.buffer_texto[:-1]
                print("Backspace aplicado ao texto em memória.")
            else:
                self._registrar_acao({
                    "tipo": "tecla",
                    "tecla": "backspace",
                    "janela": self._janela_ativa()
                })
                print("Tecla gravada: backspace")
            return

        if key == keyboard.Key.space:
            self.buffer_texto += " "
            return

        if isinstance(key, keyboard.Key):
            self._flush_texto()

            nome_tecla = self._normalizar_tecla_especial(key)

            if nome_tecla:
                self._registrar_acao({
                    "tipo": "tecla",
                    "tecla": nome_tecla,
                    "janela": self._janela_ativa()
                })
                print(f"Tecla gravada: {nome_tecla}")

            return

        try:
            char = key.char
        except Exception:
            char = None

        if char:
            self.buffer_texto += char

    # ==========================================================
    # REGISTRO
    # ==========================================================
    def _registrar_acao(self, acao):
        agora = time.time()
        delay = round(agora - self.tempo_ultima_acao, 3) if self.tempo_ultima_acao else 0
        self.tempo_ultima_acao = agora

        acao["delay"] = delay
        acao["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        acao["ativo"] = True

        if self.capturar_prints and acao["tipo"] not in ["texto"]:
            caminho_print = self._capturar_print(acao["tipo"])
            if caminho_print:
                acao["print"] = str(caminho_print)

        self.acoes.append(acao)

    def _flush_texto(self):
        if not self.buffer_texto:
            return

        texto = self.buffer_texto
        self.buffer_texto = ""

        self._registrar_acao({
            "tipo": "texto",
            "valor": texto,
            "janela": self._janela_ativa()
        })

        print(f"Texto gravado: {texto}")

    def _capturar_print(self, tipo_acao):
        try:
            timestamp = datetime.datetime.now().strftime("%H%M%S_%f")
            caminho = self.pasta_prints / f"{tipo_acao}_{timestamp}.png"
            img = pyautogui.screenshot()
            img.save(caminho)
            return caminho
        except Exception:
            return None

    def _janela_ativa(self):
        if not gw:
            return ""

        try:
            janela = gw.getActiveWindow()
            if janela:
                return janela.title or ""
        except Exception:
            pass

        return ""

    def _normalizar_tecla_especial(self, key):
        mapa = {
            keyboard.Key.enter: "enter",
            keyboard.Key.tab: "tab",
            keyboard.Key.esc: "esc",
            keyboard.Key.delete: "delete",
            keyboard.Key.up: "up",
            keyboard.Key.down: "down",
            keyboard.Key.left: "left",
            keyboard.Key.right: "right",
            keyboard.Key.home: "home",
            keyboard.Key.end: "end",
            keyboard.Key.page_up: "pageup",
            keyboard.Key.page_down: "pagedown",
        }

        return mapa.get(key)

    # ==========================================================
    # TRATAMENTO DE AÇÕES
    # ==========================================================
    def _consolidar_scrolls(self, acoes):
        novas_acoes = []
        scroll_acumulado = None

        for acao in acoes:
            if acao.get("tipo") == "scroll":
                if scroll_acumulado is None:
                    scroll_acumulado = acao.copy()
                else:
                    scroll_acumulado["dy"] += int(acao.get("dy", 0))
                    scroll_acumulado["dx"] += int(acao.get("dx", 0))
                    scroll_acumulado["scroll_amount"] += int(acao.get("scroll_amount", 0))
                    scroll_acumulado["delay"] += float(acao.get("delay", 0))
                    scroll_acumulado["x"] = acao.get("x", scroll_acumulado.get("x"))
                    scroll_acumulado["y"] = acao.get("y", scroll_acumulado.get("y"))
            else:
                if scroll_acumulado:
                    novas_acoes.append(scroll_acumulado)
                    scroll_acumulado = None

                novas_acoes.append(acao)

        if scroll_acumulado:
            novas_acoes.append(scroll_acumulado)

        return novas_acoes

    # ==========================================================
    # JSON E SCRIPT
    # ==========================================================
    def salvar_json(self, caminho_json, acoes):
        dados = {
            "nome_processo": self.nome_processo,
            "data_gravacao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "observacao": "Processo gravado pelo Treinador de Robôs MRV.",
            "acoes": acoes
        }

        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def gerar_script_py(self, caminho_py, acoes):
        linhas = []

        linhas.append("import time")
        linhas.append("import pyautogui")
        linhas.append("")
        linhas.append("")
        linhas.append("def executar_robo_treinado():")
        linhas.append("    print('Iniciando robô treinado...')")
        linhas.append("    time.sleep(2)")
        linhas.append("")

        for acao in acoes:
            if not acao.get("ativo", True):
                continue

            tipo = acao.get("tipo")
            delay = float(acao.get("delay", 0) or 0)

            if tipo in ["inicio", "fim"]:
                continue

            if delay > 0:
                linhas.append(f"    time.sleep({round(delay, 3)})")

            if tipo == "click":
                x = int(acao.get("x", 0))
                y = int(acao.get("y", 0))
                botao = acao.get("botao", "left")

                if botao not in ["left", "right", "middle"]:
                    botao = "left"

                linhas.append(f"    pyautogui.click({x}, {y}, button='{botao}')")

            elif tipo == "texto":
                valor = acao.get("valor", "")
                linhas.append(f"    pyautogui.write({repr(valor)}, interval=0.02)")

            elif tipo == "tecla":
                tecla = acao.get("tecla")

                if tecla:
                    tecla = str(tecla).strip().lower()

                    if "+" in tecla:
                        partes = [p.strip() for p in tecla.split("+") if p.strip()]
                        partes_repr = ", ".join(repr(p) for p in partes)
                        linhas.append(f"    pyautogui.hotkey({partes_repr})")
                    else:
                        linhas.append(f"    pyautogui.press('{tecla}')")

            elif tipo == "espera":
                segundos = float(acao.get("segundos", 1) or 1)
                linhas.append(f"    time.sleep({round(segundos, 3)})")

            elif tipo == "scroll":
                x = int(acao.get("x", 0))
                y = int(acao.get("y", 0))
                quantidade = int(acao.get("scroll_amount", 0))

                if quantidade != 0:
                    linhas.append(f"    pyautogui.moveTo({x}, {y})")
                    linhas.append(f"    pyautogui.scroll({quantidade})")

            linhas.append("")

        linhas.append("    print('Robô treinado finalizado.')")
        linhas.append("")
        linhas.append("")
        linhas.append("if __name__ == '__main__':")
        linhas.append("    executar_robo_treinado()")

        with open(caminho_py, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))

    # ==========================================================
    # REVISOR DE ETAPAS
    # ==========================================================
    def abrir_revisor(self):
        app = RevisorTreinamento(
            treinador=self,
            arquivo_json=self.arquivo_json,
            arquivo_json_revisado=self.arquivo_json_revisado,
            arquivo_py_revisado=self.arquivo_py_revisado
        )
        app.executar()


class RevisorTreinamento:
    def __init__(self, treinador, arquivo_json, arquivo_json_revisado, arquivo_py_revisado):
        self.treinador = treinador
        self.arquivo_json = Path(arquivo_json)
        self.arquivo_json_revisado = Path(arquivo_json_revisado)
        self.arquivo_py_revisado = Path(arquivo_py_revisado)

        self.dados = self._carregar_json()
        self.acoes = self.dados.get("acoes", [])

        self.root = None
        self.lista = None

        self.var_tipo = None
        self.var_descricao = None
        self.var_delay = None
        self.var_texto = None
        self.var_x = None
        self.var_y = None
        self.var_scroll = None
        self.var_ativo = None

        self.indice_atual = None

    def executar(self):
        self.root = tk.Tk()
        self.root.title("Revisor de Etapas - Treinador de Robôs")
        self.root.geometry("980x620")
        self.root.minsize(900, 560)

        self._montar_interface()
        self._atualizar_lista()

        self.root.mainloop()

    def _carregar_json(self):
        with open(self.arquivo_json, "r", encoding="utf-8") as f:
            return json.load(f)

    def _montar_interface(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(1, weight=1)

        titulo = tk.Label(
            self.root,
            text="Revisor de Etapas do Treinador de Robôs",
            font=("Segoe UI", 16, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(12, 6))

        frame_lista = tk.Frame(self.root)
        frame_lista.grid(row=1, column=0, sticky="nsew", padx=(14, 7), pady=8)
        frame_lista.grid_rowconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(0, weight=1)

        self.lista = tk.Listbox(frame_lista, font=("Consolas", 10), activestyle="none")
        self.lista.grid(row=0, column=0, sticky="nsew")

        scroll_lista = tk.Scrollbar(frame_lista, orient="vertical", command=self.lista.yview)
        scroll_lista.grid(row=0, column=1, sticky="ns")
        self.lista.configure(yscrollcommand=scroll_lista.set)

        self.lista.bind("<<ListboxSelect>>", self._ao_selecionar)

        frame_editor = tk.LabelFrame(
            self.root,
            text="Editar etapa selecionada",
            font=("Segoe UI", 10, "bold")
        )
        frame_editor.grid(row=1, column=1, sticky="nsew", padx=(7, 14), pady=8)
        frame_editor.grid_columnconfigure(1, weight=1)

        self.var_tipo = tk.StringVar()
        self.var_descricao = tk.StringVar()
        self.var_delay = tk.StringVar()
        self.var_texto = tk.StringVar()
        self.var_x = tk.StringVar()
        self.var_y = tk.StringVar()
        self.var_scroll = tk.StringVar()
        self.var_ativo = tk.BooleanVar(value=True)

        linha = 0

        self._campo_readonly(frame_editor, "Tipo:", self.var_tipo, linha)
        linha += 1

        self._campo_normal(frame_editor, "Descrição:", self.var_descricao, linha)
        linha += 1

        self._campo_normal(frame_editor, "Delay:", self.var_delay, linha)
        linha += 1

        self._campo_normal(frame_editor, "Texto digitado:", self.var_texto, linha)
        linha += 1

        self._campo_normal(frame_editor, "X:", self.var_x, linha)
        linha += 1

        self._campo_normal(frame_editor, "Y:", self.var_y, linha)
        linha += 1

        self._campo_normal(frame_editor, "Scroll amount:", self.var_scroll, linha)
        linha += 1

        chk = tk.Checkbutton(
            frame_editor,
            text="Etapa ativa",
            variable=self.var_ativo
        )
        chk.grid(row=linha, column=1, sticky="w", padx=8, pady=8)
        linha += 1

        texto_ajuda = tk.Label(
            frame_editor,
            text=(
                "Dica: para scroll, valores negativos descem e positivos sobem.\n"
                "Se o scroll ficou fraco, aumente a intensidade. Exemplo: -10, -20, -40."
            ),
            justify="left",
            fg="#666666"
        )
        texto_ajuda.grid(row=linha, column=0, columnspan=2, sticky="w", padx=8, pady=(8, 4))
        linha += 1

        frame_botoes_editor = tk.Frame(frame_editor)
        frame_botoes_editor.grid(row=linha, column=0, columnspan=2, sticky="ew", padx=8, pady=10)
        frame_botoes_editor.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        tk.Button(
            frame_botoes_editor,
            text="Salvar edição",
            command=self._salvar_edicao
        ).grid(row=0, column=0, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_editor,
            text="Adicionar texto",
            command=self._adicionar_texto
        ).grid(row=0, column=1, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_editor,
            text="Adicionar tecla",
            command=self._adicionar_tecla
        ).grid(row=0, column=2, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_editor,
            text="Adicionar espera",
            command=self._adicionar_espera
        ).grid(row=0, column=3, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_editor,
            text="Subir",
            command=self._subir_etapa
        ).grid(row=0, column=4, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_editor,
            text="Descer",
            command=self._descer_etapa
        ).grid(row=0, column=5, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_editor,
            text="Excluir",
            command=self._excluir_etapa
        ).grid(row=0, column=6, sticky="ew", padx=4)
        frame_botoes_finais = tk.Frame(self.root)
        frame_botoes_finais.grid(row=2, column=0, columnspan=2, sticky="ew", padx=14, pady=(0, 14))
        frame_botoes_finais.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        tk.Button(
            frame_botoes_finais,
            text="Salvar JSON revisado",
            command=self._salvar_json_revisado
        ).grid(row=0, column=0, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_finais,
            text="Gerar script revisado",
            command=self._gerar_script_revisado
        ).grid(row=0, column=1, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_finais,
            text="Salvar e gerar",
            command=self._salvar_e_gerar
        ).grid(row=0, column=2, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_finais,
            text="Fechar",
            command=self.root.destroy
        ).grid(row=0, column=3, sticky="ew", padx=4)

        tk.Button(
            frame_botoes_finais,
            text="Abrir pasta",
            command=self._abrir_pasta_treinamento
        ).grid(row=0, column=4, sticky="ew", padx=4)

    def _campo_readonly(self, parent, label, var, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=8, pady=6)
        entry = tk.Entry(parent, textvariable=var, state="readonly")
        entry.grid(row=row, column=1, sticky="ew", padx=8, pady=6)

    def _campo_normal(self, parent, label, var, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=8, pady=6)
        entry = tk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=1, sticky="ew", padx=8, pady=6)

    def _resumo_acao(self, idx, acao):
        ativo = "✓" if acao.get("ativo", True) else "X"
        tipo = acao.get("tipo", "")

        if tipo == "click":
            return f"{idx:03d} [{ativo}] CLICK  x={acao.get('x')} y={acao.get('y')} botão={acao.get('botao', 'left')}"

        if tipo == "texto":
            valor = acao.get("valor", "")
            if len(valor) > 35:
                valor = valor[:35] + "..."
            return f"{idx:03d} [{ativo}] TEXTO  {repr(valor)}"

        if tipo == "scroll":
            return f"{idx:03d} [{ativo}] SCROLL amount={acao.get('scroll_amount')} x={acao.get('x')} y={acao.get('y')}"

        if tipo == "inicio":
            return f"{idx:03d} [{ativo}] INÍCIO"

        if tipo == "fim":
            return f"{idx:03d} [{ativo}] FIM"

        if tipo == "espera":
            return f"{idx:03d} [{ativo}] ESPERA {acao.get('segundos', 1)}s"

        if tipo == "tecla":
            return f"{idx:03d} [{ativo}] TECLA  {acao.get('tecla')}"

        return f"{idx:03d} [{ativo}] {tipo.upper()}"

    def _atualizar_lista(self):
        self.lista.delete(0, tk.END)

        for idx, acao in enumerate(self.acoes):
            self.lista.insert(tk.END, self._resumo_acao(idx, acao))

    def _ao_selecionar(self, event=None):
        selecao = self.lista.curselection()

        if not selecao:
            return

        self.indice_atual = selecao[0]
        acao = self.acoes[self.indice_atual]

        self.var_tipo.set(acao.get("tipo", ""))
        self.var_descricao.set(acao.get("descricao", ""))
        self.var_delay.set(str(acao.get("delay", 0)))

        if acao.get("tipo") == "espera":
            self.var_texto.set(str(acao.get("segundos", "")))
        else:
            self.var_texto.set(str(acao.get("valor", "")))

        self.var_x.set(str(acao.get("x", "")))
        self.var_y.set(str(acao.get("y", "")))
        self.var_scroll.set(str(acao.get("scroll_amount", "")))
        self.var_ativo.set(bool(acao.get("ativo", True)))

        if acao.get("tipo") == "espera":
            self.var_texto.set(str(acao.get("segundos", "")))

    def _salvar_edicao(self):
        if self.indice_atual is None:
            messagebox.showwarning("Revisor", "Selecione uma etapa primeiro.")
            return

        acao = self.acoes[self.indice_atual]
        tipo = acao.get("tipo")

        acao["descricao"] = self.var_descricao.get().strip()
        acao["ativo"] = bool(self.var_ativo.get())

        try:
            acao["delay"] = float(self.var_delay.get().replace(",", "."))
        except Exception:
            messagebox.showwarning("Revisor", "Delay inválido.")
            return

        if tipo == "texto":
            acao["valor"] = self.var_texto.get()

        if tipo == "espera":
            try:
                acao["segundos"] = float(self.var_texto.get().replace(",", "."))
            except Exception:
                messagebox.showwarning("Revisor", "Tempo de espera inválido.")
                return

        if tipo in ["click", "scroll"]:
            try:
                if self.var_x.get().strip():
                    acao["x"] = int(float(self.var_x.get().replace(",", ".")))
                if self.var_y.get().strip():
                    acao["y"] = int(float(self.var_y.get().replace(",", ".")))
            except Exception:
                messagebox.showwarning("Revisor", "Coordenadas X/Y inválidas.")
                return

        if tipo == "scroll":
            try:
                acao["scroll_amount"] = int(float(self.var_scroll.get().replace(",", ".")))
            except Exception:
                messagebox.showwarning("Revisor", "Scroll amount inválido.")
                return

        self._atualizar_lista()
        self.lista.selection_clear(0, tk.END)
        self.lista.selection_set(self.indice_atual)
        self.lista.see(self.indice_atual)

    def _excluir_etapa(self):
        if self.indice_atual is None:
            messagebox.showwarning("Revisor", "Selecione uma etapa primeiro.")
            return

        resposta = messagebox.askyesno(
            "Excluir etapa",
            "Deseja excluir esta etapa da gravação?"
        )

        if not resposta:
            return

        del self.acoes[self.indice_atual]
        self.indice_atual = None
        self._limpar_campos()
        self._atualizar_lista()

    def _duplicar_etapa(self):
        if self.indice_atual is None:
            messagebox.showwarning("Revisor", "Selecione uma etapa primeiro.")
            return

        acao_original = self.acoes[self.indice_atual].copy()
        self.acoes.insert(self.indice_atual + 1, acao_original)
        self._atualizar_lista()

    def _adicionar_texto(self):
        texto = simpledialog.askstring(
            "Adicionar texto",
            "Digite o texto que o robô deverá escrever:"
        )

        if texto is None:
            return

        if texto == "":
            messagebox.showwarning(
                "Adicionar texto",
                "O texto não pode ficar vazio."
            )
            return

        nova_acao = {
            "tipo": "texto",
            "valor": texto,
            "delay": 0.3,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "janela": "",
            "ativo": True,
            "descricao": "Texto adicionado manualmente no revisor"
        }

        self._inserir_acao_apos_atual(nova_acao)

    def _adicionar_tecla(self):
        tecla = simpledialog.askstring(
            "Adicionar tecla",
            "Digite a tecla ou combinação.\n\n"
            "Exemplos:\n"
            "tab\n"
            "enter\n"
            "esc\n"
            "backspace\n"
            "delete\n"
            "ctrl+a\n"
            "ctrl+c\n"
            "ctrl+v"
        )

        if tecla is None:
            return

        tecla = tecla.strip().lower()

        if not tecla:
            messagebox.showwarning(
                "Adicionar tecla",
                "A tecla não pode ficar vazia."
            )
            return

        nova_acao = {
            "tipo": "tecla",
            "tecla": tecla,
            "delay": 0.3,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "janela": "",
            "ativo": True,
            "descricao": "Tecla adicionada manualmente no revisor"
        }

        self._inserir_acao_apos_atual(nova_acao)


    def _adicionar_espera(self):
        segundos = simpledialog.askfloat(
            "Adicionar espera",
            "Digite o tempo de espera em segundos:",
            minvalue=0.1
        )

        if segundos is None:
            return

        nova_acao = {
            "tipo": "espera",
            "segundos": float(segundos),
            "delay": 0,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "janela": "",
            "ativo": True,
            "descricao": "Espera adicionada manualmente no revisor"
        }

        self._inserir_acao_apos_atual(nova_acao)


    def _inserir_acao_apos_atual(self, nova_acao):
        if self.indice_atual is None:
            self.acoes.append(nova_acao)
            novo_indice = len(self.acoes) - 1
        else:
            self.acoes.insert(self.indice_atual + 1, nova_acao)
            novo_indice = self.indice_atual + 1

        self._atualizar_lista()

        self.lista.selection_clear(0, tk.END)
        self.lista.selection_set(novo_indice)
        self.lista.see(novo_indice)

        self.indice_atual = novo_indice
        self._ao_selecionar()


    def _subir_etapa(self):
        if self.indice_atual is None:
            messagebox.showwarning("Revisor", "Selecione uma etapa primeiro.")
            return

        if self.indice_atual <= 0:
            return

        idx = self.indice_atual

        self.acoes[idx - 1], self.acoes[idx] = self.acoes[idx], self.acoes[idx - 1]
        self.indice_atual = idx - 1

        self._atualizar_lista()
        self.lista.selection_clear(0, tk.END)
        self.lista.selection_set(self.indice_atual)
        self.lista.see(self.indice_atual)
        self._ao_selecionar()


    def _descer_etapa(self):
        if self.indice_atual is None:
            messagebox.showwarning("Revisor", "Selecione uma etapa primeiro.")
            return

        if self.indice_atual >= len(self.acoes) - 1:
            return

        idx = self.indice_atual

        self.acoes[idx + 1], self.acoes[idx] = self.acoes[idx], self.acoes[idx + 1]
        self.indice_atual = idx + 1

        self._atualizar_lista()
        self.lista.selection_clear(0, tk.END)
        self.lista.selection_set(self.indice_atual)
        self.lista.see(self.indice_atual)
        self._ao_selecionar()

    def _abrir_pasta_treinamento(self):
        pasta = self.arquivo_json.parent

        try:
            os.startfile(pasta)
        except Exception as e:
            messagebox.showerror(
                "Abrir pasta",
                f"Não foi possível abrir a pasta:\n\n{pasta}\n\nErro:\n{e}"
            )


    def _limpar_campos(self):
        self.var_tipo.set("")
        self.var_descricao.set("")
        self.var_delay.set("")
        self.var_texto.set("")
        self.var_x.set("")
        self.var_y.set("")
        self.var_scroll.set("")
        self.var_ativo.set(True)

    def _salvar_json_revisado(self):
        self.treinador.salvar_json(self.arquivo_json_revisado, self.acoes)

        messagebox.showinfo(
            "Revisor",
            f"JSON revisado salvo em:\n{self.arquivo_json_revisado}"
        )

    def _gerar_script_revisado(self):
        self.treinador.gerar_script_py(self.arquivo_py_revisado, self.acoes)

        messagebox.showinfo(
            "Revisor",
            f"Script revisado gerado em:\n{self.arquivo_py_revisado}"
        )

    def _salvar_e_gerar(self):
        self.treinador.salvar_json(self.arquivo_json_revisado, self.acoes)
        self.treinador.gerar_script_py(self.arquivo_py_revisado, self.acoes)

        messagebox.showinfo(
            "Revisor",
            "JSON revisado e script revisado foram gerados com sucesso."
        )


def iniciar_treinador(nome_processo=None):
    treinador = TreinadorRobos(
        pasta_saida="robos_treinados",
        capturar_prints=True
    )
    treinador.iniciar_gravacao(nome_processo=nome_processo)


if __name__ == "__main__":
    iniciar_treinador()