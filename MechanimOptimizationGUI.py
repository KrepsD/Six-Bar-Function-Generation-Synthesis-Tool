import customtkinter as ctk
import math
import scipy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image
from matplotlib.patches import Arc
import pandas as pd
import time
from scipy.optimize import root

# ---------------------------------------------------------------------------
# Síntese de mecanismos - Interface GUI
#
# Este arquivo implementa uma interface gráfica usando CustomTkinter para
# sintetizar mecanismos (Watt, Stephenson, etc.) e executar otimizações.
# Contém:
# - classe App: gerencia a janela, widgets e lógica da interface
# - métodos para criar widgets (frames, botões, entradas, sliders, plots)
# - funções de otimização e visualização (raiz numérica, desenho dos elos)
#
# Observações:
# - Comentários em português inseridos progressivamente (início do arquivo).
# - Alterações futuras serão feitas em lotes para facilitar revisão.
# ---------------------------------------------------------------------------


# Classe que define os objetos no loop da interface do CustomTkinter
class App(ctk.CTk):
    def __init__(self):

        # Inicializa a janela principal da aplicação.
        # Aqui chamamos o construtor da classe-pai (CTk) e delegamos a
        # construção dos componentes de interface para `init_ui()`.
        super().__init__()
        self.init_ui()

        # Garante que, ao fechar a janela, plots do matplotlib sejam
        # fechados corretamente e a aplicação seja destruída.
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        plt.close('all')
        self.destroy()

    def init_ui(self):

        self.initial_guess = None
        #243464
        # Constants
        #IMAGE_PATH1 = "C:\\Users\\Daniel\\OneDrive\\Documentos\\TCC\\Oertical_extenso_fundo_claro_ok.png"
        #IMAGE_PATH2 = "C:\\Users\\Daniel\\OneDrive\\Documentos\\TCC\\Configuracao1mec.png"
        #IMAGE_PATH3 = "C:\\Users\\Daniel\\OneDrive\\Documentos\\TCC\\Configuracao2mec.png"
        self.FRAME_BG_COLOR = "#243464"
        self.LABEL_FONT = ("Arial", 15)
        self.LABEL_FONT_SMALL = ("Arial", 14)
        self.LABEL_FONT_LARGE = ("Arial", 30)
        self.BUTTON_COLOR = "#243464"
        self.BUTTON_HOVER_COLOR = "#3567AD"
        self.BUTTON_BORDER_COLOR = "#243464"
        self.BUTTON_TEXT_COLOR = "#FFFFFF"
        self.SLIDER_COLOR = "#aaaca4"

        # -----------------------------
        # Configurações visuais e constantes
        # - Paths de imagens usadas na UI
        # - Cores e fontes padronizadas para widgets
        # Essas constantes facilitam alterar o tema da aplicação em um
        # único local.
        # -----------------------------

        # Window settings
        self.title("Síntese de mecanismos")
        self.geometry("1920.0x1080.0")
        #self.resizable(True, True)
        ctk.set_appearance_mode('dark')
        self.configure(fg_color="#fffaf4")
        #ctk.set_widget_scaling(1.0)

    # -----------------------------
    # Configuração da janela principal
    # - título, tamanho inicial e comportamento de redimensionamento
    # - modo de aparência (dark/light) e escala de widgets
    # -----------------------------

        # Load image
        #image1 = Image.open(IMAGE_PATH1)
        #image2 = Image.open(IMAGE_PATH2)
        #image3 = Image.open(IMAGE_PATH3)
        #ctk_image1 = ctk.CTkImage(image1, size=(300, 65))
        #ctk_image2 = ctk.CTkImage(image2, size=(300, 150))
        #ctk_image3 = ctk.CTkImage(image3, size=(300, 150))

    # -----------------------------
    # Carregamento de imagens
    # - as imagens são convertidas para CTkImage para uso em labels
    # - atenção: caminhos absolutos são usados; se mover o projeto,
    #   atualize os caminhos ou use caminhos relativos.
    # -----------------------------

        # Create tab view
        self.create_tab_view()

        # Create frames
        self.create_frames()

        # Create buttons
        self.create_buttons()

        # Create labels
        self.create_labels()

        # Create combo boxes
        self.create_combo_boxes()

        # Create entries
        self.create_entries()

        # Create sliders
        self.create_sliders()

        # Create switches
        self.create_switches()

        # Create plots
        self.create_plots()

        # Display image
        #image_label1 = ctk.CTkLabel(self, image=ctk_image1, text="")
        #image_label1.place(x=1200, y=20)

    def create_tab_view(self):
        """Cria a visualização em abas (tab view) usada pela interface.

        Cada aba corresponde a um tipo de mecanismo ou à aba de
        configurações. Esta função apenas instancia o widget e cria as
        abas vazias - o conteúdo é desenhado em frames separados.
        """
        self.tabview = ctk.CTkTabview(master=self, fg_color="#e7e7e7", width=1100, height=650, border_color="#000000", segmented_button_fg_color="#243464", segmented_button_selected_color="#3567AD", segmented_button_unselected_color="#243464")
        self.tabview.place(relx=0.23, rely=0.613, anchor="w")
        for tab_name in ["Watt 1", "Watt 2", "Stephenson 1", "Stephenson 2", "Stephenson 3", "Configurações"]:
            self.tabview.add(tab_name)

    def create_frames(self):
        """Cria e posiciona os frames principais da UI.

        - frames comuns (topo, barra, painel esquerdo)
        - frames específicos para cada aba (um frame por aba do tabview)

        Os frames são armazenados em `self.frames` para referência posterior
        quando outros widgets forem adicionados.
        """
        self.frames = {}
        frame_specs = [
            ("frame_1", self, "#8eaef1", 1100, 80, 0.03, 0.07),
            ("frame_2", self, "#e7e7e7", 1920, 50, 0.0, 0.16),
            ("frame_3", self, "#8eaef1", 320, 400, 0.0, 0.47),
        ]
        for name, master, color, width, height, relx, rely in frame_specs:
            # Cada frame principal é criado e posicionado com place()
            self.frames[name] = ctk.CTkFrame(master=master, fg_color=color, width=width, height=height)
            self.frames[name].place(relx=relx, rely=rely, anchor="w")

        # Cria frames específicos dentro de cada aba do tabview.
        for tab_name in ["Watt 1", "Watt 2", "Stephenson 1", "Stephenson 2", "Stephenson 3", "Configurações"]:
            frame_name = f"frame_4_{tab_name.replace(' ', '_')}"
            self.frames[frame_name] = ctk.CTkFrame(master=self.tabview.tab(tab_name), fg_color="#8eaef1", width=1920, height=515, border_color="#000000")
            self.frames[frame_name].place(relx=0, rely=0, anchor="nw")

    def create_buttons(self):
        """Cria botões usados na interface e armazena-os em `self.buttons`.

        - 'Home' e 'Otimizar' como botões principais.
        - Botão adicional em cada aba para mostrar o gráfico de ângulos.
        """
        self.buttons = {}  # Dictionary to store button references

        button_specs = [
            ("Home", self.frames["frame_2"], 0.1, 0.5, self.reset_ALL),
            ("Otimizar", self.frames["frame_3"], 0.5, 0.8, self.entregar_p_otimizar),
        ]
        for text, frame, relx, rely, command in button_specs:
            button = ctk.CTkButton(frame, text=text, corner_radius=32, fg_color=self.BUTTON_COLOR, hover_color=self.BUTTON_HOVER_COLOR, border_color=self.BUTTON_BORDER_COLOR, border_width=2, command=command, text_color=self.BUTTON_TEXT_COLOR)
            button.place(relx=relx, rely=rely, anchor="center")
            self.buttons[text] = button  # Store button reference

        # Botão de visualização de ângulos para cada aba de mecanismo
        for tab_name in ["Watt 1", "Watt 2", "Stephenson 1", "Stephenson 2", "Stephenson 3"]:
            frame_name = f"frame_4_{tab_name.replace(' ', '_')}"
            button = ctk.CTkButton(self.frames[frame_name], text="Mostrar grafico dos angulos de entrada e saida", corner_radius=32, fg_color=self.BUTTON_COLOR, hover_color=self.BUTTON_HOVER_COLOR, border_color=self.BUTTON_BORDER_COLOR, border_width=2, command=self.mostrar_angulos)
            button.place(relx=0.3, rely=0.83, anchor="w")
            self.buttons[f"Mostrar grafico {tab_name}"] = button  # Store button reference

    def create_labels(self):
        """Cria labels estáticos usados pela interface.

        A função centraliza e posiciona textos explicativos e etiquetas de
        saída usados nas várias abas.
        """
        # Criação dos textos da interface (suas funções segundo o bloco 'text=')
        self.label = ctk.CTkLabel(self.frames["frame_1"], text="Síntese de geração de função de mecanismos de seis barras por meio de otimização", font=("Arial", 29), text_color="#000000")
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.label1 = ctk.CTkLabel(self.frames["frame_3"], text="Mecanismo a ser otimizado:", font=("Arial", 15), text_color="#000000")
        self.label1.place(relx=0.5, rely=0.05, anchor="center")

        self.label222 = ctk.CTkLabel(self.frames["frame_3"], text="Limites dos ângulos de qualidade de transmissão (90º+-valor)", font=("Arial", 11), text_color="#000000")
        self.label222.place(relx=0.5, rely=0.62, anchor="center")

        # Texto Watt2
        self.label3 = ctk.CTkLabel(self.frames["frame_4_Watt_2"], text="Par de ângulos otimizados:", font=("Arial", 15), text_color="#000000")
        self.label3.place(relx=0.02, rely=0.71, anchor="w")

        # Texto Watt1
        self.label3_W1 = ctk.CTkLabel(self.frames["frame_4_Watt_1"], text="Par de ângulos otimizados:", font=("Arial", 15), text_color="#000000")
        self.label3_W1.place(relx=0.02, rely=0.71, anchor="w")

        # Texto stephenson1
        self.label3_S1 = ctk.CTkLabel(self.frames["frame_4_Stephenson_1"], text="Par de ângulos otimizados:", font=("Arial", 15), text_color="#000000")
        self.label3_S1.place(relx=0.02, rely=0.71, anchor="w")

        # Texto stephenson3
        self.label3_S3 = ctk.CTkLabel(self.frames["frame_4_Stephenson_3"], text="Par de ângulos otimizados:", font=("Arial", 15), text_color="#000000")
        self.label3_S3.place(relx=0.02, rely=0.71, anchor="w")

        # Texto stephenson2
        self.label3_S2 = ctk.CTkLabel(self.frames["frame_4_Stephenson_2"], text="Par de ângulos otimizados:", font=("Arial", 15), text_color="#000000")
        self.label3_S2.place(relx=0.02, rely=0.71, anchor="w")

        # Texto Watt2
        self.label6 = ctk.CTkLabel(self.frames["frame_4_Watt_2"], text="Valor \u03B8I", font=("Arial", 15), text_color="#000000")
        self.label6.place(relx=0.3, rely=0.76, anchor="w")

        self.label6Out = ctk.CTkLabel(self.frames["frame_4_Watt_2"], text="Valor \u03B8O", font=("Arial", 15), text_color="#000000")
        self.label6Out.place(relx=0.38, rely=0.76, anchor="w")

        self.label12 = ctk.CTkLabel(self.frames["frame_4_Watt_2"], text="Resultados da otimização:", font=("Arial", 14), text_color="#000000")
        self.label12.place(relx=0.02, rely=0.81, anchor="w")

        self.label13 = ctk.CTkLabel(self.frames["frame_4_Watt_2"], text="Ângulos de saída obtidos, respectivamente: ", font=("Arial", 14), text_color="#000000")
        self.label13.place(relx=0.02, rely=0.86, anchor="w")

        self.label14 = ctk.CTkLabel(self.frames["frame_4_Watt_2"], text="", font=("Arial", 13), text_color="#000000")
        self.label14.place(relx=0.17, rely=0.86, anchor="w")

        self.label15 = ctk.CTkLabel(self.frames["frame_4_Watt_2"], text="Elos l1, l2, l3, l4, l5, l6, l8, l9 e ângulos phi, alpha, gamma obtidos, respectivamente:", font=("Arial", 14), text_color="#000000")
        self.label15.place(relx=0.02, rely=0.91, anchor="w")

        self.label16 = ctk.CTkLabel(self.frames["frame_4_Watt_2"], text="", font=("Arial", 14), text_color="#000000")
        self.label16.place(relx=0.02, rely=0.96, anchor="w")

        # Texto Watt1
        self.label6_W1 = ctk.CTkLabel(self.frames["frame_4_Watt_1"], text="Valor \u03B8I", font=("Arial", 15), text_color="#000000")
        self.label6_W1.place(relx=0.3, rely=0.76, anchor="w")

        self.label6Out_W1 = ctk.CTkLabel(self.frames["frame_4_Watt_1"], text="Valor \u03B8O", font=("Arial", 15), text_color="#000000")
        self.label6Out_W1.place(relx=0.38, rely=0.76, anchor="w")

        self.label12_W1 = ctk.CTkLabel(self.frames["frame_4_Watt_1"], text="Resultados da otimização:", font=("Arial", 14), text_color="#000000")
        self.label12_W1.place(relx=0.02, rely=0.81, anchor="w")

        self.label13_W1 = ctk.CTkLabel(self.frames["frame_4_Watt_1"], text="Ângulos de saída obtidos, respectivamente: ", font=("Arial", 14), text_color="#000000")
        self.label13_W1.place(relx=0.02, rely=0.86, anchor="w")

        self.label14_W1 = ctk.CTkLabel(self.frames["frame_4_Watt_1"], text="", font=("Arial", 13), text_color="#000000")
        self.label14_W1.place(relx=0.17, rely=0.86, anchor="w")

        self.label15_W1 = ctk.CTkLabel(self.frames["frame_4_Watt_1"], text="Elos l1, l2, l3, l4, l5, l6, l8, l9 e ângulos phi, alpha, gamma obtidos, respectivamente:", font=("Arial", 14), text_color="#000000")
        self.label15_W1.place(relx=0.02, rely=0.91, anchor="w")

        self.label16_W1 = ctk.CTkLabel(self.frames["frame_4_Watt_1"], text="", font=("Arial", 14), text_color="#000000")
        self.label16_W1.place(relx=0.02, rely=0.96, anchor="w")

        # Texto stephenson1
        self.label6_S1 = ctk.CTkLabel(self.frames["frame_4_Stephenson_1"], text="Valor \u03B8I", font=("Arial", 15), text_color="#000000")
        self.label6_S1.place(relx=0.3, rely=0.76, anchor="w")

        self.label6Out_S1 = ctk.CTkLabel(self.frames["frame_4_Stephenson_1"], text="Valor \u03B8O", font=("Arial", 15), text_color="#000000")
        self.label6Out_S1.place(relx=0.38, rely=0.76, anchor="w")

        self.label12_S1 = ctk.CTkLabel(self.frames["frame_4_Stephenson_1"], text="Resultados da otimização:", font=("Arial", 14), text_color="#000000")
        self.label12_S1.place(relx=0.02, rely=0.81, anchor="w")

        self.label13_S1 = ctk.CTkLabel(self.frames["frame_4_Stephenson_1"], text="Ângulos de saída obtidos, respectivamente: ", font=("Arial", 14), text_color="#000000")
        self.label13_S1.place(relx=0.02, rely=0.86, anchor="w")

        self.label14_S1 = ctk.CTkLabel(self.frames["frame_4_Stephenson_1"], text="", font=("Arial", 13), text_color="#000000")
        self.label14_S1.place(relx=0.17, rely=0.86, anchor="w")

        self.label15_S1 = ctk.CTkLabel(self.frames["frame_4_Stephenson_1"], text="Elos l1, l2, l3, l4, l5, l6, l8, l9 e ângulos phi, alpha, gamma obtidos, respectivamente:", font=("Arial", 14), text_color="#000000")
        self.label15_S1.place(relx=0.02, rely=0.91, anchor="w")

        self.label16_S1 = ctk.CTkLabel(self.frames["frame_4_Stephenson_1"], text="", font=("Arial", 14), text_color="#000000")
        self.label16_S1.place(relx=0.02, rely=0.96, anchor="w")

        # Texto stephenson3
        self.label6_S3 = ctk.CTkLabel(self.frames["frame_4_Stephenson_3"], text="Valor \u03B8I", font=("Arial", 15), text_color="#000000")
        self.label6_S3.place(relx=0.3, rely=0.76, anchor="w")

        self.label6Out_S3 = ctk.CTkLabel(self.frames["frame_4_Stephenson_3"], text="Valor \u03B8O", font=("Arial", 15), text_color="#000000")
        self.label6Out_S3.place(relx=0.38, rely=0.76, anchor="w")

        self.label12_S3 = ctk.CTkLabel(self.frames["frame_4_Stephenson_3"], text="Resultados da otimização:", font=("Arial", 14), text_color="#000000")
        self.label12_S3.place(relx=0.02, rely=0.81, anchor="w")

        self.label13_S3 = ctk.CTkLabel(self.frames["frame_4_Stephenson_3"], text="Ângulos de saída obtidos, respectivamente: ", font=("Arial", 14), text_color="#000000")
        self.label13_S3.place(relx=0.02, rely=0.86, anchor="w")

        self.label14_S3 = ctk.CTkLabel(self.frames["frame_4_Stephenson_3"], text="", font=("Arial", 13), text_color="#000000")
        self.label14_S3.place(relx=0.17, rely=0.86, anchor="w")

        self.label15_S3 = ctk.CTkLabel(self.frames["frame_4_Stephenson_3"], text="Elos l1, l2, l3, l4, l5, l6, l8, l9 e ângulos phi, alpha, gamma obtidos, respectivamente:", font=("Arial", 14), text_color="#000000")
        self.label15_S3.place(relx=0.02, rely=0.91, anchor="w")

        self.label16_S3 = ctk.CTkLabel(self.frames["frame_4_Stephenson_3"], text="", font=("Arial", 14), text_color="#000000")
        self.label16_S3.place(relx=0.02, rely=0.96, anchor="w")

        # Texto stephenson2
        self.label6_S2 = ctk.CTkLabel(self.frames["frame_4_Stephenson_2"], text="Valor \u03B8I", font=("Arial", 15), text_color="#000000")
        self.label6_S2.place(relx=0.3, rely=0.76, anchor="w")

        self.label6Out_S2 = ctk.CTkLabel(self.frames["frame_4_Stephenson_2"], text="Valor \u03B8O", font=("Arial", 15), text_color="#000000")
        self.label6Out_S2.place(relx=0.38, rely=0.76, anchor="w")

        self.label12_S2 = ctk.CTkLabel(self.frames["frame_4_Stephenson_2"], text="Resultados da otimização:", font=("Arial", 14), text_color="#000000")
        self.label12_S2.place(relx=0.02, rely=0.81, anchor="w")

        self.label13_S2 = ctk.CTkLabel(self.frames["frame_4_Stephenson_2"], text="Ângulos de saída obtidos, respectivamente: ", font=("Arial", 14), text_color="#000000")
        self.label13_S2.place(relx=0.02, rely=0.86, anchor="w")

        self.label14_S2 = ctk.CTkLabel(self.frames["frame_4_Stephenson_2"], text="", font=("Arial", 13), text_color="#000000")
        self.label14_S2.place(relx=0.17, rely=0.86, anchor="w")

        self.label15_S2 = ctk.CTkLabel(self.frames["frame_4_Stephenson_2"], text="Elos l1, l2, l3, l4, l5, l6, l8, l9 e ângulos phi, alpha, gamma obtidos, respectivamente:", font=("Arial", 14), text_color="#000000")
        self.label15_S2.place(relx=0.02, rely=0.91, anchor="w")

        self.label16_S2 = ctk.CTkLabel(self.frames["frame_4_Stephenson_2"], text="", font=("Arial", 14), text_color="#000000")
        self.label16_S2.place(relx=0.02, rely=0.96, anchor="w")

        # Labels de atualização
        self.label7 = ctk.CTkLabel(self.frames["frame_3"], text="", font=("Arial", 12), text_color="#000000")
        self.label7.place(relx=0.9, rely=0.23, anchor="center")

        self.label8 = ctk.CTkLabel(self.frames["frame_3"], text="", font=("Arial", 12), text_color="#000000")
        self.label8.place(relx=0.9, rely=0.30, anchor="center")

        self.label9 = ctk.CTkLabel(self.frames["frame_3"], text="", font=("Arial", 12), text_color="#000000")
        self.label9.place(relx=0.9, rely=0.37, anchor="center")

        self.label10 = ctk.CTkLabel(self.frames["frame_3"], text="", font=("Arial", 12), text_color="#000000")
        self.label10.place(relx=0.9, rely=0.44, anchor="center")

        self.label11 = ctk.CTkLabel(self.frames["frame_3"], text="", font=("Arial", 12), text_color="#000000")
        self.label11.place(relx=0.9, rely=0.51, anchor="center")

        self.label11x = ctk.CTkLabel(self.frames["frame_3"], text="", font=("Arial", 12), text_color="#000000")
        self.label11x.place(relx=0.85, rely=0.68, anchor="center")

        self.label4 = ctk.CTkLabel(self.frames["frame_3"], text="", font=("Arial", 12), text_color="#000000")
        self.label4.place(relx=0.5, rely=0.9, anchor="center")

        # Texto Configurações
        self.labelconfig1 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Número personalizado de pares de ângulos de otimização:", font=("Arial", 14), text_color="#000000")
        self.labelconfig1.place(relx=0.003, rely=0.08, anchor="w")

        self.labelconfig2 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Ângulo de entrada:", font=("Arial", 13), text_color="#000000")
        self.labelconfig2.place(relx=0.003, rely=0.14, anchor="w")

        self.labelconfig3 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Ângulo de saída:", font=("Arial", 13), text_color="#000000")
        self.labelconfig3.place(relx=0.003, rely=0.22, anchor="w")

        self.labelconfig7 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Configurações dos parâmetros de otimização:", font=("Arial", 18), text_color="#000000")
        self.labelconfig7.place(relx=0.19, rely=0.35, anchor="w")

        self.labelconfig8 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Limites superiores e inferiores dos elos L1, L2, L3, L4, L5, L6, L8, L9 e dos ângulos phi, alfa e lambda:", font=("Arial", 15), text_color="#000000")
        self.labelconfig8.place(relx=0.003, rely=0.46, anchor="w")

        self.labelconfig9 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Limites Superiores:", font=("Arial", 13), text_color="#000000")
        self.labelconfig9.place(relx=0.003, rely=0.54, anchor="w")

        self.labelconfig10 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Limites Inferiores:", font=("Arial", 13), text_color="#000000")
        self.labelconfig10.place(relx=0.003, rely=0.62, anchor="w")

        self.labelconfig11 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Tolerância:", font=("Arial", 15), text_color="#000000")
        self.labelconfig11.place(relx=0.16, rely=0.70, anchor="e")

        self.labelconfig12 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Tolerância absoluta:", font=("Arial", 15), text_color="#000000")
        self.labelconfig12.place(relx=0.16, rely=0.78, anchor="e")

        self.labelconfig13 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Iteração máxima:", font=("Arial", 15), text_color="#000000")
        self.labelconfig13.place(relx=0.16, rely=0.86, anchor="e")

        self.labelconfig14 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Quantidade de threads (-1 = todas):", font=("Arial", 15), text_color="#000000")
        self.labelconfig14.place(relx=0.16, rely=0.94, anchor="e")

        self.labelconfig15 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Tamanho da população:", font=("Arial", 15), text_color="#000000")
        self.labelconfig15.place(relx=0.37, rely=0.70, anchor="e")

        self.labelconfig16 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Estratégia de otimização:", font=("Arial", 15), text_color="#000000")
        self.labelconfig16.place(relx=0.37, rely=0.78, anchor="e")

        self.labelconfig17 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Mutação:", font=("Arial", 15), text_color="#000000")
        self.labelconfig17.place(relx=0.37, rely=0.86, anchor="e")

        self.labelconfig17 = ctk.CTkLabel(self.frames["frame_4_Configurações"], text="Recombinação:", font=("Arial", 15), text_color="#000000")
        self.labelconfig17.place(relx=0.37, rely=0.94, anchor="e")

    def create_combo_boxes(self):
        """Cria comboboxes (drop-downs) usados na UI.

        - Um combobox principal para escolher o mecanismo a ser otimizado
        - Comboboxes por aba para controlar opções específicas (ex.: número
          de casos, configuração)

        Os widgets são armazenados em `self.combo_boxes` para uso posterior
        nas callbacks.
        """
        self.combo_boxes = {}  # Dictionary to store combo box references

        # Combobox principal (seleção do mecanismo a otimizar)
        self.combobox = ctk.CTkComboBox(self.frames["frame_3"], values=["Watt 1", "Watt 2", "Stephenson 1", "Stephenson 2", "Stephenson 3"], fg_color="#243464", border_color="#243464", dropdown_fg_color="#243464", text_color="#FFFFFF", dropdown_text_color="#FFFFFF")
        self.combobox.place(relx=0.5, rely=0.12, anchor="center")
        self.combo_boxes["main"] = self.combobox  # Store main combo box reference

        # Comboboxes por aba: opções de exemplo/configuração
        for tab_name in ["Watt 1", "Watt 2", "Stephenson 1", "Stephenson 2", "Stephenson 3", "Configurações"]:
            frame_name = f"frame_4_{tab_name.replace(' ', '_')}"
            if tab_name != "Configurações":    
                combobox = ctk.CTkComboBox(self.frames[frame_name], values=["0", "1", "2", "3", "4", "5"], fg_color="#243464", border_color="#243464", dropdown_fg_color="#243464", text_color="#FFFFFF", dropdown_text_color="#FFFFFF", command=self.mudar_configuracao)
                combobox.place(relx=0.13, rely=0.71, anchor="w")
                self.combo_boxes[tab_name] = combobox  # Store combo box reference
            else:
                # Aba de configurações usa valores diferentes
                combobox = ctk.CTkComboBox(self.frames[frame_name], values=["randtobest1bin", "best1bin" ,"best1exp", "rand1bin", "rand1exp", "rand2bin", "rand2exp", "randtobest1exp", "currenttobest1bin", "currenttobest1exp", "best2exp", "best2bin"], fg_color="#243464", border_color="#243464", dropdown_fg_color="#243464", text_color="#FFFFFF", dropdown_text_color="#FFFFFF", width= 135)
                combobox.place(relx=0.375, rely=0.78, anchor="w")
                self.combo_boxes[tab_name] = combobox

    def create_entries(self):
        """Cria campos de entrada (Entry) usados para recepção de dados.

        - Usa uma lista de especificações (`entry_specs`) para evitar repetição.
        - Entradas small (dentro de frame_3) e entradas largas (na aba de configurações).
        """
        self.entries = {}  # Dictionary to store entry references

        entry_specs = [
            (self.frames["frame_3"], "Entrada 1", 0.2, 0.23),
            (self.frames["frame_3"], "Saída 1", 0.5, 0.23),
            (self.frames["frame_3"], "Entrada 2", 0.2, 0.30),
            (self.frames["frame_3"], "Saída 2", 0.5, 0.30),
            (self.frames["frame_3"], "Entrada 3", 0.2, 0.37),
            (self.frames["frame_3"], "Saída 3", 0.5, 0.37),
            (self.frames["frame_3"], "Entrada 4", 0.2, 0.44),
            (self.frames["frame_3"], "Saída 4", 0.5, 0.44),
            (self.frames["frame_3"], "Entrada 5", 0.2, 0.51),
            (self.frames["frame_3"], "Saída 5", 0.5, 0.51),
            (self.frames["frame_3"], "Padrão: 50", 0.35, 0.68),
            (self.frames["frame_4_Configurações"], "Exemplo: 40 50 100 120 150 200 300", 0.06, 0.14),
            (self.frames["frame_4_Configurações"], "Exemplo: 40 50 100 120 150 200 300", 0.06, 0.22),
            (self.frames["frame_4_Configurações"], "L1", 0.064, 0.54),
            (self.frames["frame_4_Configurações"], "L2", 0.104, 0.54),
            (self.frames["frame_4_Configurações"], "L3", 0.104+1*0.04, 0.54),
            (self.frames["frame_4_Configurações"], "L4", 0.104+2*0.04, 0.54),
            (self.frames["frame_4_Configurações"], "L5", 0.104+3*0.04, 0.54),
            (self.frames["frame_4_Configurações"], "L6", 0.104+4*0.04, 0.54),
            (self.frames["frame_4_Configurações"], "L8", 0.104+5*0.04, 0.54),
            (self.frames["frame_4_Configurações"], "L9", 0.104+6*0.04, 0.54),
            (self.frames["frame_4_Configurações"], "φ", 0.104+7*0.04, 0.54),
            (self.frames["frame_4_Configurações"], "α", 0.104+8*0.04, 0.54),
            (self.frames["frame_4_Configurações"], "λ", 0.104+9*0.04, 0.54),
            (self.frames["frame_4_Configurações"], "L1", 0.064, 0.62),
            (self.frames["frame_4_Configurações"], "L2", 0.104, 0.62),
            (self.frames["frame_4_Configurações"], "L3", 0.104+1*0.04, 0.62),
            (self.frames["frame_4_Configurações"], "L4", 0.104+2*0.04, 0.62),
            (self.frames["frame_4_Configurações"], "L5", 0.104+3*0.04, 0.62),
            (self.frames["frame_4_Configurações"], "L6", 0.104+4*0.04, 0.62),
            (self.frames["frame_4_Configurações"], "L8", 0.104+5*0.04, 0.62),
            (self.frames["frame_4_Configurações"], "L9", 0.104+6*0.04, 0.62),
            (self.frames["frame_4_Configurações"], "φ", 0.104+7*0.04, 0.62),
            (self.frames["frame_4_Configurações"], "α", 0.104+8*0.04, 0.62),
            (self.frames["frame_4_Configurações"], "λ", 0.104+9*0.04, 0.62),
            (self.frames["frame_4_Configurações"], "Padrão: 0.01", 0.163, 0.7),
            (self.frames["frame_4_Configurações"], "Padrão: 0.0001", 0.163, 0.78),
            (self.frames["frame_4_Configurações"], "Padrão: 2000", 0.163, 0.86),
            (self.frames["frame_4_Configurações"], "Padrão: -1", 0.163, 0.94),
            (self.frames["frame_4_Configurações"], "Padrão: 15", 0.375, 0.7),
            (self.frames["frame_4_Configurações"], "Padrão: 0.5, 1", 0.375, 0.86),
            (self.frames["frame_4_Configurações"], "Padrão: 0.7", 0.375, 0.94),


        ]
        for frame, placeholder, relx, rely in entry_specs:
            if frame == self.frames["frame_3"]:
                # Entradas compactas para a área de seleção rápida
                entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=80, placeholder_text_color="#FFFFFF", fg_color="#243464", border_color="#243464")
                entry.place(relx=relx, rely=rely, anchor="w")
                self.entries[placeholder] = entry  # Store entry reference
            
            elif rely > 0.25 and rely <= 0.65:
                # Entradas médias para parâmetros de configuração
                entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=70, placeholder_text_color="#FFFFFF", fg_color="#243464", border_color="#243464")
                entry.place(relx=relx, rely=rely, anchor="w")
                self.entries[placeholder] = entry
            
            elif rely > 0.65:
                # Entradas médias para parâmetros de configuração
                entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=110, placeholder_text_color="#FFFFFF", fg_color="#243464", border_color="#243464")
                entry.place(relx=relx, rely=rely, anchor="w")
                self.entries[placeholder] = entry 
        
            else:
                # Entradas largas usadas em configurações (texto explicativo)
                entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=940, height = 30, placeholder_text_color="#FFFFFF", fg_color="#243464", border_color="#243464")
                entry.place(relx=relx, rely=rely, anchor="w")
                self.entries[placeholder] = entry
        
    def create_sliders(self):
        """Cria sliders horizontais para seleção de ângulo inicial por aba.

        Cada slider controla o valor inicial thetaI mostrado na interface e
        chama `valor_thetaI_slider` quando alterado.
        """
        self.sliders = {}  # Dictionary to store slider references

        for tab_name in ["Watt 1", "Watt 2", "Stephenson 1", "Stephenson 2", "Stephenson 3"]:
            frame_name = f"frame_4_{tab_name.replace(' ', '_')}"
            slider = ctk.CTkSlider(self.frames[frame_name], from_=0, to=359, button_color=self.SLIDER_COLOR, orientation="horizontal", width=470, command=self.valor_thetaI_slider)
            slider.set(0)
            slider.place(relx=0.3, rely=0.71, anchor="w")
            self.sliders[tab_name] = slider  # Store slider reference

    def create_switches(self):
        """Cria switches (checkbox-like) para alternar exibições.

        Exemplo: alternar a numeração dos elos quando a função de desenho é
        invocada.
        """
        self.switches = {}  # Dictionary to store switch references

        # Especificações de switches por aba
        switch_specs = [
            ("Watt 1", self.frames["frame_4_Watt_1"], "Mostrar a numeração dos elos", 0.07, 0.02, self.MostrarElosEangulos),
            ("Watt 2", self.frames["frame_4_Watt_2"], "Mostrar a numeração dos elos", 0.07, 0.02, self.MostrarElosEangulos),
            ("Stephenson 1", self.frames["frame_4_Stephenson_1"], "Mostrar a numeração dos elos", 0.07, 0.02, self.MostrarElosEangulos),
            ("Stephenson 2", self.frames["frame_4_Stephenson_2"], "Mostrar a numeração dos elos", 0.07, 0.02, self.MostrarElosEangulos),
            ("Stephenson 3", self.frames["frame_4_Stephenson_3"], "Mostrar a numeração dos elos", 0.07, 0.02, self.MostrarElosEangulos),
        ]

        for tab_name, frame, text, relx, rely, command in switch_specs:
            switch = ctk.CTkSwitch(master=frame, text=text, command=command, text_color="#000000")
            switch.place(relx=relx, rely=rely, anchor="w")
            unique_key = f"{tab_name} {text}"  # Create a unique key
            self.switches[unique_key] = switch  # Store switch reference

    def create_plots(self):
        """Configura objetos de plotagem (matplotlib) usados pela UI.

        A função cria figuras e eixos que serão atualizados dinamicamente
        quando os mecanismos forem desenhados ou cálculos de posição
        ocorrerem.
        """
        # Criação de dois gráficos para cada um dos mecanismos

        # Gráficos Watt2
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(6,4)
        self.ax.set_title("Mecanismo Watt 2")
        self.ax.set_xlabel("Eixo X")   
        self.ax.set_ylabel("Eixo Y")
        self.canvas = FigureCanvasTkAgg(self.fig,self.frames["frame_4_Watt_2"])
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.02, rely=0.35, anchor="w")

        self.fig2, self.ax2 = plt.subplots()
        self.fig2.set_size_inches(6,4)
        self.ax2.set_title("Mecanismo Watt 2")
        self.ax2.set_xlabel("Eixo X")   
        self.ax2.set_ylabel("Eixo Y")
        self.canvas2 = FigureCanvasTkAgg(self.fig2, self.frames["frame_4_Watt_2"])
        self.canvas2.draw()
        self.canvas2.get_tk_widget().place(relx=0.3, rely=0.35, anchor="w")

        self.toolbar = NavigationToolbar2Tk(self.canvas2, self.frames["frame_4_Watt_2"])
        self.toolbar.update()
        self.toolbar.place(relx=0.4, rely=0.02, anchor="w")

        # Gráficos Watt1
        self.fig_W1, self.ax_W1 = plt.subplots()
        self.fig_W1.set_size_inches(6,4)
        self.ax_W1.set_title("Mecanismo Watt 1")
        self.ax_W1.set_xlabel("Eixo X")   
        self.ax_W1.set_ylabel("Eixo Y")
        self.canvas_W1 = FigureCanvasTkAgg(self.fig_W1,self.frames["frame_4_Watt_1"])
        self.canvas_W1.draw()
        self.canvas_W1.get_tk_widget().place(relx=0.02, rely=0.35, anchor="w")

        self.fig2_W1, self.ax2_W1 = plt.subplots()
        self.fig2_W1.set_size_inches(6,4)
        self.ax2_W1.set_title("Mecanismo Watt 1")
        self.ax2_W1.set_xlabel("Eixo X")   
        self.ax2_W1.set_ylabel("Eixo Y")
        self.canvas2_W1 = FigureCanvasTkAgg(self.fig2_W1, self.frames["frame_4_Watt_1"])
        self.canvas2_W1.draw()
        self.canvas2_W1.get_tk_widget().place(relx=0.3, rely=0.35, anchor="w")
        
        self.toolbar_W1 = NavigationToolbar2Tk(self.canvas2_W1, self.frames["frame_4_Watt_1"])
        self.toolbar_W1.update()
        self.toolbar_W1.place(relx=0.4, rely=0.02, anchor="w")

        # Gráficos stephenson1
        self.fig_S1, self.ax_S1 = plt.subplots()
        self.fig_S1.set_size_inches(6,4)
        self.ax_S1.set_title("Mecanismo Stephenson 1")
        self.ax_S1.set_xlabel("Eixo X")   
        self.ax_S1.set_ylabel("Eixo Y")
        self.canvas_S1 = FigureCanvasTkAgg(self.fig_S1,self.frames["frame_4_Stephenson_1"])
        self.canvas_S1.draw()
        self.canvas_S1.get_tk_widget().place(relx=0.02, rely=0.35, anchor="w")

        self.fig2_S1, self.ax2_S1 = plt.subplots()
        self.fig2_S1.set_size_inches(6,4)
        self.ax2_S1.set_title("Mecanismo Stephenson 1")
        self.ax2_S1.set_xlabel("Eixo X")   
        self.ax2_S1.set_ylabel("Eixo Y")
        self.canvas2_S1 = FigureCanvasTkAgg(self.fig2_S1, self.frames["frame_4_Stephenson_1"])
        self.canvas2_S1.draw()
        self.canvas2_S1.get_tk_widget().place(relx=0.3, rely=0.35, anchor="w")

        self.toolbar_S1 = NavigationToolbar2Tk(self.canvas2_S1, self.frames["frame_4_Stephenson_1"])
        self.toolbar_S1.update()
        self.toolbar_S1.place(relx=0.4, rely=0.02, anchor="w")

        # Gráficos stephenson3
        self.fig_S3, self.ax_S3 = plt.subplots()
        self.fig_S3.set_size_inches(6,4)
        self.ax_S3.set_title("Mecanismo Stephenson 3")
        self.ax_S3.set_xlabel("Eixo X")   
        self.ax_S3.set_ylabel("Eixo Y")
        self.canvas_S3 = FigureCanvasTkAgg(self.fig_S3, self.frames["frame_4_Stephenson_3"])
        self.canvas_S3.draw()
        self.canvas_S3.get_tk_widget().place(relx=0.02, rely=0.35, anchor="w")

        self.fig2_S3, self.ax2_S3 = plt.subplots()
        self.fig2_S3.set_size_inches(6,4)
        self.ax2_S3.set_title("Mecanismo Stephenson 3")
        self.ax2_S3.set_xlabel("Eixo X")   
        self.ax2_S3.set_ylabel("Eixo Y")
        self.canvas2_S3 = FigureCanvasTkAgg(self.fig2_S3, self.frames["frame_4_Stephenson_3"])
        self.canvas2_S3.draw()
        self.canvas2_S3.get_tk_widget().place(relx=0.3, rely=0.35, anchor="w")

        self.toolbar_S3 = NavigationToolbar2Tk(self.canvas2_S3, self.frames["frame_4_Stephenson_3"])
        self.toolbar_S3.update()
        self.toolbar_S3.place(relx=0.4, rely=0.02, anchor="w")

        # Gráficos stephenson2
        self.fig_S2, self.ax_S2 = plt.subplots()
        self.fig_S2.set_size_inches(6,4)
        self.ax_S2.set_title("Mecanismo Stephenson 2")
        self.ax_S2.set_xlabel("Eixo X")   
        self.ax_S2.set_ylabel("Eixo Y")
        self.canvas_S2 = FigureCanvasTkAgg(self.fig_S2, self.frames["frame_4_Stephenson_2"])
        self.canvas_S2.draw()
        self.canvas_S2.get_tk_widget().place(relx=0.02, rely=0.35, anchor="w")

        self.fig2_S2, self.ax2_S2 = plt.subplots()
        self.fig2_S2.set_size_inches(6,4)
        self.ax2_S2.set_title("Mecanismo Stephenson 2")
        self.ax2_S2.set_xlabel("Eixo X")   
        self.ax2_S2.set_ylabel("Eixo Y")
        self.canvas2_S2 = FigureCanvasTkAgg(self.fig2_S2, self.frames["frame_4_Stephenson_2"])
        self.canvas2_S2.draw()
        self.canvas2_S2.get_tk_widget().place(relx=0.3, rely=0.35, anchor="w")

        self.toolbar_S2 = NavigationToolbar2Tk(self.canvas2_S2, self.frames["frame_4_Stephenson_2"])
        self.toolbar_S2.update()
        self.toolbar_S2.place(relx=0.4, rely=0.02, anchor="w")

    def reset_ALL(self):
        """Reinicializa toda a interface reconstruindo todos os widgets.

        Uso: chamado pelo botão 'Home' para descartar os widgets atuais e
        recriar toda a interface a partir de `init_ui()`.
        """
        # Função que reseta a interface para sua construção inicial
        for widget in self.winfo_children():
            widget.destroy()

        # Reconstrói a interface do zero
        self.init_ui()

    def MostrarElosEangulos(self):
        """Desenha o mecanismo selecionado e rotula elos/juntas/ângulos.

        Esta função é invocada por switches/botões que pedem a
        exibição detalhada do mecanismo (nomenclatura de elos, arcos de
        ângulos etc.). A função trata cada tipo de mecanismo separadamente
        (Watt 1, Watt 2, Stephenson 1/2/3). Usa `Modelos_mecanismos` para
        obter coordenadas e ângulos.
        """

        # Função dos botões de interrupção que mostram a nomenclatura de cada elo e ângulo otimizado de determinado mecanismo

        if self.combobox.get() == "Watt 1":
            
            # Try e Except para que, caso haja erros (como matemáticos [acos = x>1]), assim a interface não deixará de executar
            try:    
                
                # Define o ângulo que será colocado na função Modelos_mecanismos
                AngE = self.thetaI_W1[0]
                [A_W1, B_W1, C_W1, D_W1, E_W1, F_W1, G_W1, mi1_W1, mi2_W1, thetaO_W1] = self.Modelos_mecanismos('W1', AngE)
                
                # Plota o mecanismo no primeiro axis
                self.ax_W1.clear()
                self.ax_W1.plot([A_W1[0], B_W1[0]], [A_W1[1], B_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([A_W1[0], C_W1[0]], [A_W1[1], C_W1[1]], '-og', markersize=4, alpha=0.5)
                self.ax_W1.plot([B_W1[0], D_W1[0]], [B_W1[1], D_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([B_W1[0], G_W1[0]], [B_W1[1], G_W1[1]], '-or', markersize=4, alpha=0.5)
                self.ax_W1.plot([G_W1[0], D_W1[0]], [G_W1[1], D_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([G_W1[0], F_W1[0]], [G_W1[1], F_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([D_W1[0], C_W1[0]], [D_W1[1], C_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([D_W1[0], E_W1[0]], [D_W1[1], E_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([C_W1[0], E_W1[0]], [C_W1[1], E_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([E_W1[0], F_W1[0]], [E_W1[1], F_W1[1]], '-ok', markersize=4, alpha=0.5)

                # Escreve as letras referentes a cada junta do mecanismo
                points_W1 = {'A': A_W1, 'B': B_W1, 'C': C_W1, 'D': D_W1, 'E': E_W1, 'F': F_W1, 'G': G_W1}
                for letter, (x, y) in points_W1.items():
                    self.ax_W1.text(x, y+2.5, letter, fontsize=12, ha='right')
                
                # Define a ordem dos elos que conectam cada junta
                lines_W1 = [
                    ('A', 'B'), ('A', 'C'), ('C', 'D'), ('B', 'D'), ('E', 'C'),
                    ('G', 'B'), ('D', 'E'), ('E', 'F'), ('F', 'G'), ('G', 'D')
                ]

                # Caso o interruptor seja ativado, escreve a nomenclatura de todos os elos (ex: L1) no primeiro axis
                if self.switches["Watt 1 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_W1):
                            # Label each line
                        mid_x_W1 = (points_W1[start][0] + points_W1[end][0]) / 2
                        mid_y_W1= (points_W1[start][1] + points_W1[end][1]) / 2
                        self.ax_W1.text(mid_x_W1, mid_y_W1, f'L{i+1}', fontsize=12, ha='center', va='center')

                # Preenche a àrea dos elos ternários do mecanismo de laranja e cinza
                self.ax_W1.fill([B_W1[0], G_W1[0], D_W1[0]], [B_W1[1], G_W1[1], D_W1[1]], color='orange', alpha=0.5)
                self.ax_W1.fill([C_W1[0], D_W1[0], E_W1[0]], [C_W1[1], D_W1[1], E_W1[1]], color='gray', alpha=0.5)
                
                ArcoThetaI = Arc(xy=A_W1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI_W1[0]))
                ArcoThetaO = Arc(xy=B_W1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_W1))
                angleMi1 = math.atan2((C_W1[1]-D_W1[1]),(C_W1[0]-D_W1[0]))
                angleMi2 = math.atan2((E_W1[1]-F_W1[1]),(E_W1[0]-F_W1[0]))
                ArcoMi1 = Arc(xy=D_W1, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_W1+angleMi1))
                ArcoMi2 = Arc(xy=F_W1, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_W1+angleMi2))
                self.ax_W1.add_patch(ArcoThetaI)
                self.ax_W1.add_patch(ArcoThetaO)
                self.ax_W1.add_patch(ArcoMi1)
                self.ax_W1.add_patch(ArcoMi2)
                self.ax_W1.text(A_W1[0] + 5, A_W1[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax_W1.text(B_W1[0] + 5, B_W1[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax_W1.text(D_W1[0] + 5, D_W1[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax_W1.text(F_W1[0] + 5, F_W1[1], r"$\mu$2", fontsize=12, ha='center', va='center')
                
                # Configuração geral do axis
                self.ax_W1.set_title("Mecanismo Watt 1")
                self.ax_W1.set_xlabel("Eixo X")   
                self.ax_W1.set_ylabel("Eixo Y")
                self.ax_W1.set_xlim(self.x_min_W1, self.x_max_W1)
                self.ax_W1.set_ylim(self.y_min_W1, self.y_max_W1)

                self.canvas_W1.draw()

            except:
                aaaaa =1   

            # Para os outros mecanismos desta função (MostrarElosEangulos), o funcionamento segue o mesmo modelo deste.

        elif self.combobox.get() == "Watt 2":

            try:
                
                AngE = self.thetaI[0]
                [A, B, C, D, E, F, G, mi1, mi2, thetaO] = self.Modelos_mecanismos('W2', AngE)
                
                self.ax.clear()
                self.ax.plot([A[0], B[0]], [A[1], B[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([B[0], C[0]], [B[1], C[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([C[0], E[0]], [C[1], E[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([C[0], F[0]], [C[1], F[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([A[0], D[0]], [A[1], D[1]], '-og', markersize=4, alpha=0.5)
                self.ax.plot([B[0], G[0]], [B[1], G[1]], '-or', markersize=4, alpha=0.5)
                self.ax.plot([D[0], E[0]], [D[1], E[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([E[0], F[0]], [E[1], F[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([F[0], G[0]], [F[1], G[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([B[0], C[0]], [B[1], C[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([A[0], C[0]], [A[1], C[1]], '-ok', markersize=4, alpha=0.5)

                points = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'G': G}

                for letter, (x, y) in points.items():
                    self.ax.text(x, y+2.5, letter, fontsize=12, ha='right')

                lines = [
                ('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'E'), ('E', 'C'),
                ('F', 'C'), ('E', 'F'), ('G', 'F'), ('B', 'G'), ('B', 'C')
                ]

                if self.switches["Watt 2 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines):
                            # Label each line
                        mid_x = (points[start][0] + points[end][0]) / 2
                        mid_y= (points[start][1] + points[end][1]) / 2
                        self.ax.text(mid_x, mid_y, f'L{i+1}', fontsize=12, ha='center', va='center')


                self.ax.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], color='orange', alpha=0.5)
                self.ax.fill([C[0], E[0], F[0]], [C[1], E[1], F[1]], color='gray', alpha=0.5)

                ArcoThetaI = Arc(xy=A, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI[0]))
                ArcoThetaO = Arc(xy=B, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO))
                angleMi1 = math.atan2((D[1]-E[1]),(D[0]-E[0]))
                angleMi2 = math.atan2((F[1]-G[1]),(F[0]-G[0]))
                ArcoMi1 = Arc(xy=E, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1+angleMi1))
                ArcoMi2 = Arc(xy=G, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2+angleMi2))
                self.ax.add_patch(ArcoThetaI)
                self.ax.add_patch(ArcoThetaO)
                self.ax.add_patch(ArcoMi1)
                self.ax.add_patch(ArcoMi2)
                self.ax.text(A[0] + 5, A[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax.text(B[0] + 5, B[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax.text(E[0] + 5, E[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax.text(G[0] + 5, G[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                self.ax.set_title("Mecanismo Watt 2")
                self.ax.set_xlabel("Eixo X")   
                self.ax.set_ylabel("Eixo Y")
                self.ax.set_xlim(self.x_min, self.x_max)
                self.ax.set_ylim(self.y_min, self.y_max)
                self.canvas.draw()

                
            except:
                pass

            # -----------------------------
            # Caso Stephenson 3: leitura de pares de ângulos e preparação para otimização
            # Mesma lógica dos demais casos.
            # -----------------------------

        elif self.combobox.get() == "Stephenson 3":
            try:
                self.thetaI_S3 = []
                self.thetaOd_S3 = []

                AngE = self.thetaI_S1[0]
                [A_S1, B_S1, C_S1, D_S1, E_S1, F_S1, G_S1, mi1_S1, mi2_S1, thetaO_S1] = self.Modelos_mecanismos('S1', AngE)
                
                self.ax_S1.clear()
                self.ax_S1.plot([A_S1[0], B_S1[0]], [A_S1[1], B_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([A_S1[0], C_S1[0]], [A_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([A_S1[0], D_S1[0]], [A_S1[1], D_S1[1]], '-og', markersize=4, alpha=0.5)
                self.ax_S1.plot([B_S1[0], E_S1[0]], [B_S1[1], E_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([B_S1[0], F_S1[0]], [B_S1[1], F_S1[1]], '-or', markersize=4, alpha=0.5)
                self.ax_S1.plot([F_S1[0], E_S1[0]], [F_S1[1], E_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([F_S1[0], G_S1[0]], [F_S1[1], G_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([E_S1[0], D_S1[0]], [E_S1[1], D_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([D_S1[0], C_S1[0]], [D_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([G_S1[0], C_S1[0]], [G_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)

                points_S1 = {'A': A_S1, 'B': B_S1, 'C': C_S1, 'D': D_S1, 'E': E_S1, 'F': F_S1, 'G': G_S1}
            
                for letter, (x, y) in points_S1.items():
                    self.ax_S1.text(x, y+2.5, letter, fontsize=12, ha='right')

                lines_S1 = [
                    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'E'), ('D', 'E'),
                    ('B', 'F'), ('C', 'D'), ('C', 'G'), ('G', 'F'), ('F', 'E')
                ]
                
                if self.switches["Stephenson 1 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_S1):
                        # Label each line
                        mid_x_S1 = (points_S1[start][0] + points_S1[end][0]) / 2
                        mid_y_S1= (points_S1[start][1] + points_S1[end][1]) / 2
                        self.ax_S1.text(mid_x_S1, mid_y_S1, f'L{i+1}', fontsize=12, ha='center', va='center')
                
                self.ax_S1.fill([A_S1[0], C_S1[0], D_S1[0]], [A_S1[1], C_S1[1], D_S1[1]], color='orange', alpha=0.5)
                self.ax_S1.fill([B_S1[0], E_S1[0], F_S1[0]], [B_S1[1], E_S1[1], F_S1[1]], color='gray', alpha=0.5)
                
                ArcoThetaI = Arc(xy=A_S1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI_S1[0]))
                ArcoThetaO = Arc(xy=B_S1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_S1))
                angleMi1 = math.atan2((D_S1[1]-E_S1[1]),(D_S1[0]-E_S1[0]))
                angleMi2 = math.atan2((C_S1[1]-G_S1[1]),(C_S1[0]-G_S1[0]))
                ArcoMi1 = Arc(xy=E_S1, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_S1+angleMi1))
                ArcoMi2 = Arc(xy=G_S1, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_S1+angleMi2))
                self.ax_S1.add_patch(ArcoThetaI)
                self.ax_S1.add_patch(ArcoThetaO)
                self.ax_S1.add_patch(ArcoMi1)
                self.ax_S1.add_patch(ArcoMi2)
                self.ax_S1.text(A_S1[0] + 5, A_S1[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax_S1.text(B_S1[0] + 5, B_S1[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax_S1.text(E_S1[0] + 5, E_S1[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax_S1.text(G_S1[0] + 5, G_S1[1], r"$\mu$2", fontsize=12, ha='center', va='center')
                
                self.ax_S1.set_title("Mecanismo Stephenson 1")
                self.ax_S1.set_xlabel("Eixo X")   
                self.ax_S1.set_ylabel("Eixo Y")
                self.ax_S1.set_xlim(self.x_min_S1, self.x_max_S1)
                self.ax_S1.set_ylim(self.y_min_S1, self.y_max_S1)
                self.canvas_S1.draw()


            except:
                pass    

        elif self.combobox.get() == "Stephenson 2":
                
                AngE = self.thetaI_S2[0]
                [A_S2, B_S2, C_S2, D_S2, E_S2, F_S2, G_S2, mi1_S2, mi2_S2, thetaO_S2] = self.Modelos_mecanismos('S2', AngE)
                
                self.ax_S2.clear()
                self.ax_S2.plot([A_S2[0], B_S2[0]], [A_S2[1], B_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([A_S2[0], C_S2[0]], [A_S2[1], C_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([A_S2[0], D_S2[0]], [A_S2[1], D_S2[1]], '-og', markersize=4, alpha=0.5)
                self.ax_S2.plot([B_S2[0], G_S2[0]], [B_S2[1], G_S2[1]], '-or', markersize=4, alpha=0.5)
                self.ax_S2.plot([G_S2[0], E_S2[0]], [G_S2[1], E_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([G_S2[0], F_S2[0]], [G_S2[1], F_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([E_S2[0], F_S2[0]], [E_S2[1], F_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([F_S2[0], D_S2[0]], [F_S2[1], D_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([D_S2[0], C_S2[0]], [D_S2[1], C_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([C_S2[0], E_S2[0]], [C_S2[1], E_S2[1]], '-ok', markersize=4, alpha=0.5)

                points_S2 = {'A': A_S2, 'B': B_S2, 'C': C_S2, 'D': D_S2, 'E': E_S2, 'F': F_S2, 'G': G_S2}
                
                for letter, (x, y) in points_S2.items():
                    self.ax_S2.text(x, y+2.5, letter, fontsize=12, ha='right')

                lines_S2 = [
                    ('A', 'B'), ('A', 'D'), ('A', 'C'), ('C', 'E'), ('D', 'F'),
                    ('F', 'E'), ('C', 'D'), ('F', 'G'), ('G', 'B'), ('G', 'E')
                ]

                if self.switches["Stephenson 2 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_S2):
                            # Label each line
                        mid_x_S2 = (points_S2[start][0] + points_S2[end][0]) / 2
                        mid_y_S2= (points_S2[start][1] + points_S2[end][1]) / 2
                        self.ax_S2.text(mid_x_S2, mid_y_S2, f'L{i+1}', fontsize=12, ha='center', va='center')
                    

                self.ax_S2.fill([A_S2[0], D_S2[0], C_S2[0]], [A_S2[1], D_S2[1], C_S2[1]],color='orange', alpha=0.5)
                self.ax_S2.fill([G_S2[0], E_S2[0], F_S2[0]], [G_S2[1], E_S2[1], F_S2[1]], color='gray', alpha=0.5)

                ArcoThetaI = Arc(xy=A_S2, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI_S2[0]))
                ArcoThetaO = Arc(xy=B_S2, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_S2))
                angleMi1 = math.atan2((C_S2[1]-E_S2[1]),(C_S2[0]-E_S2[0]))
                angleMi2 = math.atan2((F_S2[1]-G_S2[1]),(F_S2[0]-G_S2[0]))
                ArcoMi1 = Arc(xy=E_S2, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_S2+angleMi1))
                ArcoMi2 = Arc(xy=G_S2, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_S2+angleMi2))
                self.ax_S2.add_patch(ArcoThetaI)
                self.ax_S2.add_patch(ArcoThetaO)
                self.ax_S2.add_patch(ArcoMi1)
                self.ax_S2.add_patch(ArcoMi2)
                self.ax_S2.text(A_S2[0] + 5, A_S2[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax_S2.text(B_S2[0] + 5, B_S2[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax_S2.text(E_S2[0] + 5, E_S2[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax_S2.text(G_S2[0] + 5, G_S2[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                self.ax_S2.set_title("Mecanismo Stephenson 2")
                self.ax_S2.set_xlabel("Eixo X")   
                self.ax_S2.set_ylabel("Eixo Y")
                self.ax_S2.set_xlim(self.x_min_S2, self.x_max_S2)
                self.ax_S2.set_ylim(self.y_min_S2, self.y_max_S2)
                self.canvas_S2.draw()

        elif self.combobox.get() == "Stephenson 3":
            try:    

                AngE = self.thetaI_S3[0]
                [A_S3, B_S3, C_S3, D_S3, E_S3, F_S3, G_S3, mi1_S3, mi2_S3, thetaO_S3] = self.Modelos_mecanismos('S3', AngE)
                
                self.ax_S3.clear()
                self.ax_S3.plot([A_S3[0], B_S3[0]], [A_S3[1], B_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([A_S3[0], C_S3[0]], [A_S3[1], C_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([A_S3[0], D_S3[0]], [A_S3[1], D_S3[1]], '-og', markersize =4, alpha=0.5)
                self.ax_S3.plot([B_S3[0], C_S3[0]], [B_S3[1], C_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([C_S3[0], F_S3[0]], [C_S3[1], F_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([D_S3[0], F_S3[0]], [D_S3[1], F_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([D_S3[0], E_S3[0]], [D_S3[1], E_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([F_S3[0], E_S3[0]], [F_S3[1], E_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([G_S3[0], E_S3[0]], [G_S3[1], E_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([G_S3[0], B_S3[0]], [G_S3[1], B_S3[1]], '-or', markersize =4, alpha=0.5)

                points_S3 = {'A': A_S3, 'B': B_S3, 'C': C_S3, 'D': D_S3, 'E': E_S3, 'F': F_S3, 'G': G_S3}
            
                for letter, (x, y) in points_S3.items():
                    self.ax_S3.text(x, y+2.5, letter, fontsize=12, ha='right')

                lines_S3 = [
                ('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'F'), ('C', 'F'),
                ('E', 'F'), ('D', 'E'), ('G', 'E'), ('G', 'B'), ('B', 'C')
                ]

                if self.switches["Stephenson 3 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_S3):
                            # Label each line
                        mid_x_S3 = (points_S3[start][0] + points_S3[end][0]) / 2
                        mid_y_S3= (points_S3[start][1] + points_S3[end][1]) / 2
                        self.ax_S3.text(mid_x_S3, mid_y_S3, f'L{i+1}', fontsize=12, ha='center', va='center')
            
                self.ax_S3.fill([A_S3[0], B_S3[0], C_S3[0]], [A_S3[1], B_S3[1], C_S3[1]],color='orange', alpha=0.5)
                self.ax_S3.fill([D_S3[0], E_S3[0], F_S3[0]], [D_S3[1], E_S3[1], F_S3[1]], color='gray', alpha=0.5)
                
                ArcoThetaI = Arc(xy=A_S3, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI_S3[0]))
                ArcoThetaO = Arc(xy=B_S3, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_S3))
                angleMi1 = math.atan2((D_S3[1]-F_S3[1]),(D_S3[0]-F_S3[0]))
                angleMi2 = math.atan2((E_S3[1]-G_S3[1]),(E_S3[0]-G_S3[0]))
                ArcoMi1 = Arc(xy=F_S3, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_S3+angleMi1))
                ArcoMi2 = Arc(xy=G_S3, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_S3+angleMi2))
                self.ax_S3.add_patch(ArcoThetaI)
                self.ax_S3.add_patch(ArcoThetaO)
                self.ax_S3.add_patch(ArcoMi1)
                self.ax_S3.add_patch(ArcoMi2)
                self.ax_S3.text(A_S3[0] + 5, A_S3[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax_S3.text(B_S3[0] + 5, B_S3[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax_S3.text(F_S3[0] + 5, F_S3[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax_S3.text(G_S3[0] + 5, G_S3[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                self.ax_S3.set_title("Mecanismo Stephenson 3")
                self.ax_S3.set_xlabel("Eixo X")   
                self.ax_S3.set_ylabel("Eixo Y")
                self.ax_S3.set_xlim(self.x_min_S3, self.x_max_S3)
                self.ax_S3.set_ylim(self.y_min_S3, self.y_max_S3)
                self.canvas_S3.draw()


            except:
                aaaaa =1

    def Modelos_mecanismos(self, TipoDeMec, AngDeEntrada):
        """Retorna as coordenadas dos elos/juntas e ângulos importantes.

        Parâmetros:
        - TipoDeMec: string identificando o modelo ('W1', 'W2', 'S1', 'S2', 'S3')
        - AngDeEntrada: ângulo de entrada (radianos) para as equações cinemáticas

        Retorna lista com os pontos A..G, os ângulos mi1, mi2 e thetaO.
        Esta função implementa a cinemática geométrica para cada
        configuração de mecanismo suportada.
        """

        # Função que é chamada por outras funções para calcular as posições do mecanismo e seus ângulos de importância (cinemática)

        if TipoDeMec == 'W1':
            
            # Cálculo da cinemática do mecanismo
            A_W1 = [0,0]
            B_W1 = [self.L1_W1*math.cos(self.phi_W1),self.L1_W1*math.sin(self.phi_W1)]
            C_W1 = [self.L2_W1*math.cos(AngDeEntrada),self.L2_W1*math.sin(AngDeEntrada)]
            e1_W1 = math.sqrt((B_W1[0]-C_W1[0])**2 + (B_W1[1]-C_W1[1])**2)
            omega_W1 = math.atan2(B_W1[1]-C_W1[1], B_W1[0]-C_W1[0])
            delta_W1 = math.acos((self.L3_W1**2+e1_W1**2-self.L4_W1**2)/(2*e1_W1*self.L3_W1))
            D_W1 = [C_W1[0] + self.L3_W1*math.cos(delta_W1+omega_W1),C_W1[1] + self.L3_W1*math.sin(delta_W1+omega_W1)]
            E_W1 = [C_W1[0] + self.L5_W1*math.cos(delta_W1+omega_W1+self.alpha_W1),C_W1[1] + self.L5_W1*math.sin(delta_W1+omega_W1+self.alpha_W1)]
            
            beta1_W1 = math.atan2(D_W1[1]-B_W1[1], D_W1[0]-B_W1[0])
            thetaO_W1 = beta1_W1-self.lambda_W1
            G_W1  = [B_W1[0] + self.L6_W1*math.cos(thetaO_W1),B_W1[1] + self.L6_W1*math.sin(thetaO_W1)]
            e2_W1 = math.sqrt((E_W1[0]-G_W1[0])**2 + (E_W1[1]-G_W1[1])**2)
            beta2_W1 = math.atan2(E_W1[1]-G_W1[1], E_W1[0]-G_W1[0])
            beta3_W1 = math.acos((self.L9_W1**2+e2_W1**2-self.L8_W1**2)/(2*self.L9_W1*e2_W1))
            F_W1  = [G_W1[0] + self.L9_W1*math.cos(beta2_W1-beta3_W1),G_W1[1] + self.L9_W1*math.sin(beta2_W1-beta3_W1)]
                
            mi1_W1 = math.acos((self.L4_W1**2+self.L3_W1**2-e1_W1**2)/(2*self.L4_W1*self.L3_W1))           
            mi2_W1 = math.acos((self.L8_W1**2+self.L9_W1**2-e2_W1**2)/(2*self.L8_W1*self.L9_W1))

            # Retorna os valores pertinentes calculados nesta função
            return [A_W1, B_W1, C_W1, D_W1, E_W1, F_W1, G_W1, mi1_W1, mi2_W1, thetaO_W1]
        
            # Para os outros mecanismos desta função (Modelos_mecanismos), o funcionamento segue o mesmo modelo deste.

        elif TipoDeMec == 'W2':
            A = [0,0]
            B = [self.L1*math.cos(self.phi),self.L1*math.sin(self.phi)] 
            C = [self.L2*math.cos(self.phi+self.alpha1),self.L2*math.sin(self.phi+self.alpha1)]
            D = [self.L3*math.cos(AngDeEntrada),self.L3*math.sin(AngDeEntrada)]
            x1 = math.sqrt((D[0]-C[0])**2 + (D[1]-C[1])**2)
            Beta1 = math.atan2(C[1]-D[1], C[0]-D[0])
            Beta2 = math.acos((self.L4**2+x1**2-self.L5**2)/(2*self.L4*x1))
            E = [D[0]+self.L4*math.cos(Beta1+Beta2),D[1]+self.L4*math.sin(Beta1+Beta2)]
            lambda0 = math.atan2(E[1]-C[1], E[0]-C[0])
            F = [C[0]+self.L6*math.cos(lambda0-self.lambda1),C[1]+self.L6*math.sin(lambda0-self.lambda1)]
            x2 = math.sqrt((F[0]-B[0])**2 + (F[1]-B[1])**2)
            psi = math.atan2(F[1]-B[1], F[0]-B[0])
            omega2 = math.acos((x2**2+self.L9**2-self.L8**2)/(2*self.L9*x2))
            omega1 = psi-omega2-self.phi
            thetaO = self.phi+omega1
            G = [B[0]+self.L9*math.cos(thetaO),B[1]+self.L9*math.sin(thetaO)]
            mi1 = math.acos((self.L4**2+self.L5**2-x1**2)/(2*self.L4*self.L5))
            mi2 = math.acos((self.L8**2+self.L9**2-x2**2)/(2*self.L8*self.L9))

            if(mi1 < 0):
                mi1 = mi1+2*math.pi
            if(mi2 < 0):
                mi2 = mi2+2*math.pi

            return [A, B, C, D, E, F, G, mi1, mi2, thetaO]
        
        elif TipoDeMec == 'S1':

            A_S1 = [0,0]
            B_S1 = [self.L1_S1*math.cos(self.phi_S1),self.L1_S1*math.sin(self.phi_S1)]
            C_S1 = [self.L2_S1*math.cos(AngDeEntrada+self.alpha1_S1),self.L2_S1*math.sin(AngDeEntrada+self.alpha1_S1)]
            D_S1 = [self.L3_S1*math.cos(AngDeEntrada),self.L3_S1*math.sin(AngDeEntrada)]
            e1_S1 = math.sqrt((D_S1[0]-B_S1[0])**2 + (D_S1[1]-B_S1[1])**2)
            beta_S1 = math.atan2(B_S1[1]-D_S1[1], B_S1[0]-D_S1[0])
            omega_S1 = math.acos((e1_S1**2+self.L5_S1**2-self.L4_S1**2)/(2*e1_S1*self.L5_S1))
            E_S1 = [D_S1[0] + self.L5_S1*math.cos(beta_S1+omega_S1), D_S1[1] + self.L5_S1*math.sin(beta_S1+omega_S1)]
            ksi_S1 = math.atan2(E_S1[1]-B_S1[1], E_S1[0]-B_S1[0])
            thetaO_S1 = ksi_S1 - self.lambda1_S1
            F_S1 = [B_S1[0] + self.L6_S1*math.cos(ksi_S1-self.lambda1_S1), B_S1[1] + self.L6_S1*math.sin(ksi_S1-self.lambda1_S1)]
            e2_S1 = math.sqrt((C_S1[0]-F_S1[0])**2 + (C_S1[1]-F_S1[1])**2)
            gamma_S1 = math.atan2(C_S1[1]-F_S1[1], C_S1[0]-F_S1[0])
            delta_S1 = math.acos((e2_S1**2+self.L9_S1**2-self.L8_S1**2)/(2*e2_S1*self.L9_S1))
            G_S1 = [F_S1[0] + self.L9_S1*math.cos(gamma_S1-delta_S1), F_S1[1] + self.L9_S1*math.sin(gamma_S1-delta_S1)]
            mi1_S1 = math.acos((self.L5_S1**2+self.L4_S1**2-e1_S1**2)/(2*self.L5_S1*self.L4_S1))
            mi2_S1 = math.acos((self.L9_S1**2+self.L8_S1**2-e2_S1**2)/(2*self.L9_S1*self.L8_S1))

            if(mi1_S1 < 0):
                mi1_S1 = mi1_S1+2*math.pi
            if(mi2_S1 < 0):
                mi2_S1 = mi2_S1+2*math.pi

            return [A_S1, B_S1, C_S1, D_S1, E_S1, F_S1, G_S1, mi1_S1, mi2_S1, thetaO_S1]

        elif TipoDeMec == 'S2':
            A_S2 = [0,0]
            B_S2 = [self.L1_S2*math.cos(self.phi_S2),self.L1_S2*math.sin(self.phi_S2)]
            C_S2 = [self.L3_S2*math.cos(AngDeEntrada+self.alpha1_S2),self.L3_S2*math.sin(AngDeEntrada+self.alpha1_S2)]
            D_S2 = [self.L2_S2*math.cos(AngDeEntrada),self.L2_S2*math.sin(AngDeEntrada)]

            E_S2 = [C_S2[0] + self.L4_S2*math.cos(self.gammaVetor_S2[np.int64(np.rad2deg(AngDeEntrada)*100)]), C_S2[1] + self.L4_S2*math.sin(self.gammaVetor_S2[np.int64(np.rad2deg(AngDeEntrada)*100)])]
            e1_S2 = math.sqrt((E_S2[0]-D_S2[0])**2 + (E_S2[1]-D_S2[1])**2)
            omega_S2 = math.atan2(E_S2[1]-D_S2[1], E_S2[0]-D_S2[0])
            omega2_S2 = math.acos((e1_S2**2 + self.L5_S2**2 - self.L6_S2**2) / (2 * e1_S2 * self.L5_S2))
            F_S2 = [D_S2[0] + self.L5_S2*math.cos(omega_S2-omega2_S2), D_S2[1] + self.L5_S2*math.sin(omega_S2-omega2_S2)]
            omega3_S2 = math.atan2(E_S2[1]-F_S2[1], E_S2[0]-F_S2[0])
            G_S2 = [F_S2[0] + self.L8_S2*math.cos(omega3_S2-self.lambda1_S2), F_S2[1] + self.L8_S2*math.sin(omega3_S2-self.lambda1_S2)]

            thetaO_S2 = math.atan2(G_S2[1]-B_S2[1], G_S2[0]-B_S2[0])

            e2_S2 = math.sqrt((F_S2[0]-B_S2[0])**2 + (F_S2[1]-B_S2[1])**2)

            e3_S2 = math.sqrt((F_S2[0]-C_S2[0])**2 + (F_S2[1]-C_S2[1])**2)

            mi1_S2 = math.acos((self.L4_S2**2 + self.L6_S2**2 - e3_S2**2) / (2 * self.L4_S2 * self.L6_S2))
            mi2_S2 = math.acos((self.L8_S2**2+self.L9_S2**2-e2_S2**2)/(2*self.L8_S2*self.L9_S2))

            if(mi1_S2 < 0):
                mi1_S2 = mi1_S2+2*math.pi
            if(mi2_S2 < 0):
                mi2_S2 = mi2_S2+2*math.pi

            return [A_S2, B_S2, C_S2, D_S2, E_S2, F_S2, G_S2, mi1_S2, mi2_S2, thetaO_S2]
        
        elif TipoDeMec == 'S3':
            A_S3 = [0,0]
            B_S3 = [self.L1_S3*math.cos(self.phi_S3),self.L1_S3*math.sin(self.phi_S3)]
            C_S3 = [self.L2_S3*math.cos(self.phi_S3+self.alpha1_S3),self.L2_S3*math.sin(self.phi_S3+self.alpha1_S3)]
            D_S3 = [self.L3_S3*math.cos(AngDeEntrada),self.L3_S3*math.sin(AngDeEntrada)]
            e1_S3 = math.sqrt((D_S3[0]-C_S3[0])**2 + (D_S3[1]-C_S3[1])**2)
            omega_S3 = math.acos((e1_S3**2+self.L5_S3**2-self.L4_S3**2)/(2*e1_S3*self.L5_S3))
            beta_S3 = math.atan2(D_S3[1]-C_S3[1], D_S3[0]-C_S3[0])
            F_S3 = [C_S3[0] + self.L5_S3*math.cos(beta_S3-omega_S3), C_S3[1] + self.L5_S3*math.sin(beta_S3-omega_S3)]
            lambda0_S3 = math.atan2(D_S3[1]-F_S3[1], D_S3[0]-F_S3[0])
            E_S3 = [F_S3[0] + self.L6_S3*math.cos(lambda0_S3-self.lambda1_S3), F_S3[1] + self.L6_S3*math.sin(lambda0_S3-self.lambda1_S3)]
            e2_S3 = math.sqrt((E_S3[0]-B_S3[0])**2 + (E_S3[1]-B_S3[1])**2)
            gamma_S3 = math.acos((e2_S3**2+self.L9_S3**2-self.L8_S3**2)/(2*e2_S3*self.L9_S3))
            gamma1_S3 = math.atan2(E_S3[1]-B_S3[1], E_S3[0]-B_S3[0])
            thetaO_S3 = gamma1_S3-gamma_S3
            G_S3 = [B_S3[0] + self.L9_S3*math.cos(thetaO_S3), B_S3[1] + self.L9_S3*math.sin(thetaO_S3)]

            mi1_S3 = math.acos((self.L5_S3**2+self.L4_S3**2-e1_S3**2)/(2*self.L5_S3*self.L4_S3))
            mi2_S3 = math.acos((self.L8_S3**2+self.L9_S3**2-e2_S3**2)/(2*self.L8_S3*self.L9_S3))

            if(mi1_S3 < 0):
                mi1_S3 = mi1_S3+2*math.pi
            if(mi2_S3 < 0):
                mi2_S3 = mi2_S3+2*math.pi
            

            return [A_S3, B_S3, C_S3, D_S3, E_S3, F_S3, G_S3, mi1_S3, mi2_S3, thetaO_S3]

    def mostrar_angulos(self):
        """Gera gráficos das relações entre ângulos importantes.

        Substitui a visualização do mecanismo por gráficos que mostram as
        relações entre o ângulo de entrada (theta I) e ângulos de saída
        ou qualidade de transmissão (mu1, mu2) ao longo do ciclo.
        """

        try:
            if self.combobox.get() == "Watt 1":
                # Inicialização de variáveis
                mi11_W1 = []
                mi22_W1 = []
                thetaOutput_W1 = []
                ThetaInicial_W1 = [i * (359 / 3599) for i in range(3600)]

                # Laço que obtém 3600 (Entre 0 e 360 graus) valores do ângulo de saída e dos ângulos de qualidade de transmissão e armazena em vetores. 
                for i in range(3600):
                    try:

                        AngE = math.radians(ThetaInicial_W1[i])
                        [A_W1, B_W1, C_W1, D_W1, E_W1, F_W1, G_W1, mi1_W1, mi2_W1, thetaO_W1] = self.Modelos_mecanismos('W1', AngE)
                        thetaOutput_W1.append(math.degrees(thetaO_W1))

                        mi11_W1.append(math.degrees(mi1_W1))
                        mi22_W1.append(math.degrees(mi2_W1))
                    except:
                        thetaOutput_W1.append(0)
                        mi11_W1.append(0)
                        mi22_W1.append(0)

                self.ax2_W1.clear()

                # Plota todos os dados no segundo axis
                self.ax2_W1.plot(ThetaInicial_W1, thetaOutput_W1, '-', color='blue', label = r"$\theta$I x $\theta$O")
                self.ax2_W1.plot(ThetaInicial_W1, mi11_W1, '-', color='red', label = r"$\theta$I x $\mu$1")
                self.ax2_W1.plot(ThetaInicial_W1, mi22_W1, '-', color='green', label = r"$\theta$I x $\mu$2")
                self.ax2_W1.plot(np.rad2deg(self.thetaI_W1), np.rad2deg(self.thetaOd_W1), 'o', color='red', label = r"$\theta$I x $\theta$O desejado")
                self.ax2_W1.plot(np.rad2deg(self.thetaI_W1), np.rad2deg(self.thetaO_W1), 'o', color='black', label = r"$\theta$I x $\theta$O otimizado")

                # COnfigurações gerais do axis
                self.ax2_W1.legend()
                self.ax2_W1.set_title("Relação de ângulos - Watt 1")
                self.ax2_W1.set_xlabel(r"$\theta$I de entrada (graus)")   
                self.ax2_W1.set_ylabel(r"Ângulos (graus)")
                self.ax2_W1.set_xlim(0, max(np.rad2deg(self.thetaI_W1))+10)
                self.ax2_W1.set_ylim(-5, 359)
                self.ax2_W1.grid(True)
                self.canvas2_W1.draw()
                self.fig2_W1.savefig('destination_pathANG_W1.svg', format='svg')
                # Para os outros mecanismos desta função (mostrar_angulos), o funcionamento segue o mesmo modelo deste.
            
            elif self.combobox.get() == "Watt 2":

                mi11 = []
                mi22 = []
                thetaOutput = []
                ThetaInicial = [i * (359 / 3599) for i in range(3600)]

                for i in range(3600):
                    try:

                        AngE = math.radians(ThetaInicial[i])
                        [A, B, C, D, E, F, G, mi1, mi2, thetaO] = self.Modelos_mecanismos('W2', AngE)
                        thetaOutput.append(math.degrees(thetaO))

                        mi11.append(math.degrees(mi1))
                        mi22.append(math.degrees(mi2))

                    except:
                        thetaOutput.append(0)
                        mi11.append(0)
                        mi22.append(0)

                self.ax2.clear()

                self.ax2.plot(ThetaInicial, thetaOutput, '-', color='blue', label = r"$\theta$I x $\theta$O")
                print("Watt 2 input", ThetaInicial)
                print("Watt 2 output", thetaOutput)
                self.ax2.plot(ThetaInicial, mi11, '-', color='red', label = r"$\theta$I x $\mu$1")
                self.ax2.plot(ThetaInicial, mi22, '-', color='green', label = r"$\theta$I x $\mu$2")
                self.ax2.plot(np.rad2deg(self.thetaI), np.rad2deg(self.thetaOd), 'o', color='red', label = r"$\theta$I x $\theta$O desejado")
                self.ax2.plot(np.rad2deg(self.thetaI), np.rad2deg(self.thetaO), 'o', color='black', label = r"$\theta$I x $\theta$O Otimizado")
                self.ax2.legend()
                self.ax2.set_title("Relação de ângulos - Watt 2")
                self.ax2.set_xlabel(r"$\theta$I de entrada (graus)")   
                self.ax2.set_ylabel(r"Ângulos (graus)")
                self.ax2.set_xlim(0, max(np.rad2deg(self.thetaI))+5)
                self.ax2.set_ylim(-5, 360)
                self.ax2.grid(True)
                self.canvas2.draw()
                self.fig2.savefig('destination_pathANG.svg', format='svg') 

            elif self.combobox.get() == "Stephenson 1":

                mi11_S1 = []
                mi22_S1 = []
                thetaOutput_S1 = []
                ThetaInicial_S1 = [i * (359 / 3599) for i in range(3600)]

                for i in range(3600):
                    try:

                        AngE = math.radians(ThetaInicial_S1[i])
                        [A_S1, B_S1, C_S1, D_S1, E_S1, F_S1, G_S1, mi1_S1, mi2_S1, thetaO_S1] = self.Modelos_mecanismos('S1', AngE)

                        thetaOutput_S1.append(math.degrees(thetaO_S1))
                        mi11_S1.append(math.degrees(mi1_S1))
                        mi22_S1.append(math.degrees(mi2_S1))

                    except:
                        thetaOutput_S1.append(0)
                        mi11_S1.append(0)
                        mi22_S1.append(0)

                self.ax2_S1.clear()

                self.ax2_S1.plot(ThetaInicial_S1, thetaOutput_S1, '-', color='blue', label = r"$theta$I x $theta$O")
                
                self.ax2_S1.plot(ThetaInicial_S1, mi11_S1, '-', color='red', label = r"$theta$I x $mu$1")
                self.ax2_S1.plot(ThetaInicial_S1, mi22_S1, '-', color='green', label = r"$theta$I x $mu$2")
                self.ax2_S1.plot(np.rad2deg(self.thetaI_S1), np.rad2deg(self.thetaOd_S1), 'o', color='red', label = r"$\theta$I x $\theta$O desejado")
                self.ax2_S1.plot(np.rad2deg(self.thetaI_S1), np.rad2deg(self.thetaO_S1), 'o', color='black', label = r"$\theta$I x $\theta$O otimizado")
                self.ax2_S1.legend()
                self.ax2_S1.set_title("Relação de ângulos - Stephenson 1")
                self.ax2_S1.set_xlabel(r"$\theta$I (graus)")   
                self.ax2_S1.set_ylabel(r"Ângulos (graus)")
                self.ax2_S1.set_xlim(0, max(np.rad2deg(self.thetaI_S1))+5)
                self.ax2_S1.set_ylim(-5, 360)
                self.ax2_S1.grid(True)
                self.canvas2_S1.draw()
                self.fig2_S1.savefig('destination_pathANG_S1.svg', format='svg')

            elif self.combobox.get() == "Stephenson 2":
                mi11_S2 = []
                mi22_S2 = []
                thetaOutput_S2 = []
                Theta_print = []
                ThetaOutput_print = []
                ThetaInicial_S2 = [i * 0.01 for i in range(36000)]

                for i in range(36000):
                    try:
                        
                        AngE = math.radians(i/100)
                        [A_S2, B_S2, C_S2, D_S2, E_S2, F_S2, G_S2, mi1_S2, mi2_S2, thetaO_S2] = self.Modelos_mecanismos('S2', AngE)

                        thetaOutput_S2.append(math.degrees(thetaO_S2)) 
                        mi11_S2.append(math.degrees(mi1_S2))
                        mi22_S2.append(math.degrees(mi2_S2))

                        if i % 50 == 0:
                            Theta_print.append(i / 100)  # em graus
                            ThetaOutput_print.append(math.degrees(thetaO_S2))

                    except:
                        thetaOutput_S2.append(0)
                        mi11_S2.append(0)
                        mi22_S2.append(0)

                self.ax2_S2.clear()

                self.ax2_S2.plot(ThetaInicial_S2, thetaOutput_S2, '-', color='blue', label = r"$\theta$I x $\theta$O")
                print("Steph 2 input",Theta_print)
                print("Steph 2 output" ,ThetaOutput_print)
                self.ax2_S2.plot(ThetaInicial_S2, mi11_S2, '-', color='red', label = r"$\theta$I x $\mu$1")
                self.ax2_S2.plot(ThetaInicial_S2, mi22_S2, '-', color='green', label = r"$\theta$I x $\mu$2")
                self.ax2_S2.plot(np.rad2deg(self.thetaI_S2), np.rad2deg(self.thetaOd_S2), 'o', color='red', label = r"$\theta$I x $\theta$O desejado")
                self.ax2_S2.plot(np.rad2deg(self.thetaI_S2),np.rad2deg(self.thetaO_S2), 'o', color='black', label = r"$\theta$I x $\theta$O otimizado")
                self.ax2_S2.legend()
                self.ax2_S2.set_title("Relação de ângulos - Stephenson 2")
                self.ax2_S2.set_xlabel(r"$\theta$I (graus)")   
                self.ax2_S2.set_ylabel(r"Angulos (graus)")
                self.ax2_S2.set_xlim(0, max(np.rad2deg(self.thetaI_S2))+5)
                self.ax2_S2.set_ylim(-5, 360)
                self.ax2_S2.grid(True)
                self.canvas2_S2.draw()
                self.fig2_S2.savefig('destination_pathANG_S2.svg', format='svg')

            elif self.combobox.get() == "Stephenson 3":

                mi11_S3 = []
                mi22_S3 = []
                thetaOutput_S3 = []
                ThetaInicial_S3 = [i * (359 / 3599) for i in range(3600)]

                for i in range(3600):
                    try:
                        
                        AngE = math.radians(ThetaInicial_S3[i])
                        [A_S3, B_S3, C_S3, D_S3, E_S3, F_S3, G_S3, mi1_S3, mi2_S3, thetaO_S3] = self.Modelos_mecanismos('S3', AngE)

                        thetaOutput_S3.append(math.degrees(thetaO_S3)) 
                        mi11_S3.append(math.degrees(mi1_S3))
                        mi22_S3.append(math.degrees(mi2_S3))

                    except:
                        thetaOutput_S3.append(0)
                        mi11_S3.append(0)
                        mi22_S3.append(0)

                self.ax2_S3.clear()

                self.ax2_S3.plot(ThetaInicial_S3, thetaOutput_S3, '-', color='blue', label = r"$\theta$I x $\theta$O")
                print("Steph 3 input", ThetaInicial_S3)
                print("Steph 3 output", thetaOutput_S3)
                self.ax2_S3.plot(ThetaInicial_S3, mi11_S3, '-', color='red', label = r"$\theta$I x $\mu$1")
                self.ax2_S3.plot(ThetaInicial_S3, mi22_S3, '-', color='green', label = r"$\theta$I x $\mu$2")
                self.ax2_S3.plot(np.rad2deg(self.thetaI_S3), np.rad2deg(self.thetaOd_S3), 'o', color='red', label = r"$\theta$I x $\theta$O desejado")
                self.ax2_S3.plot(np.rad2deg(self.thetaI_S3), np.rad2deg(self.thetaO_S3), 'o', color='black', label = r"$\theta$I x $\theta$O otimizado")
                self.ax2_S3.legend()
                self.ax2_S3.set_title("Relação de ângulos - Stephenson 3")
                self.ax2_S3.set_xlabel(r"$\theta$I (graus)")   
                self.ax2_S3.set_ylabel(r"Ângulos em graus")
                self.ax2_S3.set_xlim(0, max(np.rad2deg(self.thetaI_S3))+5)
                self.ax2_S3.set_ylim(-5, 360)
                self.ax2_S3.grid(True)
                self.canvas2_S3.draw()
                self.fig2_S3.savefig('destination_pathANG_S3.svg', format='svg')
        except:
            a=111

    def valor_thetaI_slider(self, value):
        """Callback do slider que atualiza a visualização do mecanismo conforme o ângulo de entrada.

        Recebe `value` (graus) e redesenha os eixos com a configuração
        do mecanismo correspondente ao ângulo atual.
        """
        try:

            if self.combobox.get() == "Watt 1":

                # Try e Except para que, caso haja erros (como matemáticos [acos = x>1]), assim a interface não deixará de executar
                try:

                    # Define o ângulo que será colocado na função Modelos_mecanismos
                    AngE = math.radians(value)
                    [A_W1, B_W1, C_W1, D_W1, E_W1, F_W1, G_W1, mi1_W1, mi2_W1, thetaO_W1] = self.Modelos_mecanismos('W1', AngE)                
                    
                    self.ax2_W1.clear()

                    # Mostra o mecanismo no segundo axis
                    self.ax2_W1.plot([A_W1[0], B_W1[0]], [A_W1[1], B_W1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_W1.plot([A_W1[0], C_W1[0]], [A_W1[1], C_W1[1]], '-og', markersize=4, alpha=0.5)
                    self.ax2_W1.plot([B_W1[0], D_W1[0]], [B_W1[1], D_W1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_W1.plot([B_W1[0], G_W1[0]], [B_W1[1], G_W1[1]], '-or', markersize=4, alpha=0.5)
                    self.ax2_W1.plot([G_W1[0], D_W1[0]], [G_W1[1], D_W1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_W1.plot([G_W1[0], F_W1[0]], [G_W1[1], F_W1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_W1.plot([D_W1[0], C_W1[0]], [D_W1[1], C_W1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_W1.plot([D_W1[0], E_W1[0]], [D_W1[1], E_W1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_W1.plot([C_W1[0], E_W1[0]], [C_W1[1], E_W1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_W1.plot([E_W1[0], F_W1[0]], [E_W1[1], F_W1[1]], '-ok', markersize=4, alpha=0.5)

                    # Escreve a letra que corresponde cada junta do mecanismo
                    points_W1 = {'A': A_W1, 'B': B_W1, 'C': C_W1, 'D': D_W1, 'E': E_W1, 'F': F_W1, 'G': G_W1}
                    for letter, (x, y) in points_W1.items():
                        self.ax2_W1.text(x, y+2.5, letter, fontsize=12, ha='right')

                    # Define a ordem dos elos que conectam cada junta
                    lines_W1 = [
                    ('A', 'B'), ('A', 'C'), ('C', 'D'), ('B', 'D'), ('E', 'C'),
                    ('G', 'B'), ('D', 'E'), ('E', 'F'), ('F', 'G'), ('G', 'D')
                    ]

                    # Caso o interruptor seja ativado, escreve a nomenclatura de todos os elos (ex: L1) no primeiro axis
                    if self.switches["Watt 1 Mostrar a numeração dos elos"].get() == 1:
                        for i, (start, end) in enumerate(lines_W1):
                            # Label each line
                            mid_x_W1 = (points_W1[start][0] + points_W1[end][0]) / 2
                            mid_y_W1= (points_W1[start][1] + points_W1[end][1]) / 2
                            self.ax2_W1.text(mid_x_W1, mid_y_W1, f'L{i+1}', fontsize=12, ha='center', va='center')

                    # Preenche os elos ternários do mecanismo com as cores laranja e cinza
                    self.ax2_W1.fill([B_W1[0], G_W1[0], D_W1[0]], [B_W1[1], G_W1[1], D_W1[1]], color='orange', alpha=0.5)
                    self.ax2_W1.fill([C_W1[0], D_W1[0], E_W1[0]], [C_W1[1], D_W1[1], E_W1[1]], color='gray', alpha=0.5)
                    
                    ArcoThetaI = Arc(xy=A_W1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(AngE))
                    ArcoThetaO = Arc(xy=B_W1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_W1))
                    angleMi1 = math.atan2((C_W1[1]-D_W1[1]),(C_W1[0]-D_W1[0]))
                    angleMi2 = math.atan2((E_W1[1]-F_W1[1]),(E_W1[0]-F_W1[0]))
                    ArcoMi1 = Arc(xy=D_W1, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_W1+angleMi1))
                    ArcoMi2 = Arc(xy=F_W1, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_W1+angleMi2))
                    self.ax2_W1.add_patch(ArcoThetaI)
                    self.ax2_W1.add_patch(ArcoThetaO)
                    self.ax2_W1.add_patch(ArcoMi1)
                    self.ax2_W1.add_patch(ArcoMi2)
                    self.ax2_W1.text(A_W1[0] + 5, A_W1[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                    self.ax2_W1.text(B_W1[0] + 5, B_W1[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                    self.ax2_W1.text(D_W1[0] + 5, D_W1[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                    self.ax2_W1.text(F_W1[0] + 5, F_W1[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                    # configurações padrões do axis
                    self.ax2_W1.set_title("Mecanismo Watt 1")
                    self.ax2_W1.set_xlabel("Eixo X")
                    self.ax2_W1.set_ylabel("Eixo Y")
                    self.ax2_W1.set_xlim(self.x_min_W1, self.x_max_W1)
                    self.ax2_W1.set_ylim(self.y_min_W1, self.y_max_W1)
                    self.canvas2_W1.draw()


                except:
                    thetaO_W1 = np.deg2rad(-1)
                
                # Mostra os valores do angulo de entrada e de saída na interface, abaixo do axis
                strvalue = str(round(value, 3))
                strOutvalue = str(np.round(np.rad2deg(thetaO_W1),decimals=3))
                self.label6_W1.configure(text = "Valores \u03B8I: "+strvalue)
                self.label6Out_W1.configure(text = "Valores \u03B8O: "+strOutvalue)

                # Para os outros mecanismos desta função (mostrar_angulos), o funcionamento segue o mesmo modelo deste.

            elif self.combobox.get() == "Watt 2":

                try:
                    
                    AngE = math.radians(value)
                    [A, B, C, D, E, F, G, mi1, mi2, thetaO] = self.Modelos_mecanismos('W2', AngE)

                    self.ax2.clear()

                    self.ax2.plot([A[0], B[0]], [A[1], B[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2.plot([B[0], C[0]], [B[1], C[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2.plot([C[0], E[0]], [C[1], E[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2.plot([C[0], F[0]], [C[1], F[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2.plot([A[0], D[0]], [A[1], D[1]], '-og', markersize=4, alpha=0.5)
                    self.ax2.plot([B[0], G[0]], [B[1], G[1]], '-or', markersize=4, alpha=0.5)
                    self.ax2.plot([D[0], E[0]], [D[1], E[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2.plot([E[0], F[0]], [E[1], F[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2.plot([F[0], G[0]], [F[1], G[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2.plot([B[0], C[0]], [B[1], C[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2.plot([A[0], C[0]], [A[1], C[1]], '-ok', markersize=4, alpha=0.5)
                    points = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'G': G}
                    for letter, (x, y) in points.items():
                        self.ax2.text(x, y+2.5, letter, fontsize=14, ha='right')

                    lines = [
                    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'E'), ('E', 'C'),
                    ('F', 'C'), ('E', 'F'), ('G', 'F'), ('B', 'G'), ('B', 'C')
                    ]

                    if self.switches["Watt 2 Mostrar a numeração dos elos"].get() == 1:
                        for i, (start, end) in enumerate(lines):
                                # Label each line
                            mid_x = (points[start][0] + points[end][0]) / 2
                            mid_y= (points[start][1] + points[end][1]) / 2
                            self.ax2.text(mid_x, mid_y, f'L{i+1}', fontsize=12, ha='center', va='center')

                    self.ax2.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], color='orange', alpha=0.5)
                    self.ax2.fill([C[0], E[0], F[0]], [C[1], E[1], F[1]], color='gray', alpha=0.5)

                    ArcoThetaI = Arc(xy=A, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(AngE))
                    ArcoThetaO = Arc(xy=B, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO))
                    angleMi1 = math.atan2((D[1]-E[1]),(D[0]-E[0]))
                    angleMi2 = math.atan2((F[1]-G[1]),(F[0]-G[0]))
                    ArcoMi1 = Arc(xy=E, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1+angleMi1))
                    ArcoMi2 = Arc(xy=G, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2+angleMi2))
                    self.ax2.add_patch(ArcoThetaI)
                    self.ax2.add_patch(ArcoThetaO)
                    self.ax2.add_patch(ArcoMi1)
                    self.ax2.add_patch(ArcoMi2)
                    self.ax2.text(A[0] + 5, A[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                    self.ax2.text(B[0] + 5, B[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                    self.ax2.text(E[0] + 5, E[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                    self.ax2.text(G[0] + 5, G[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                    self.ax2.set_title("Mecanismo Watt 2")
                    self.ax2.set_xlabel("Eixo X")
                    self.ax2.set_ylabel("Eixo Y")
                    self.ax2.set_xlim(self.x_min, self.x_max)
                    self.ax2.set_ylim(self.y_min, self.y_max)
                    self.canvas2.draw()


                except:
                    thetaO=np.deg2rad(-1)

                strOutvalue = str(np.round(np.rad2deg(thetaO),decimals=3))
                strvalue = str(round(value, 3))
                self.label6.configure(text = "Valores \u03B8I: "+strvalue)
                self.label6Out.configure(text = "Valores \u03B8O: "+strOutvalue)

            elif self.combobox.get() == "Stephenson 1":

                try:
                    
                    AngE = math.radians(value)
                    [A_S1, B_S1, C_S1, D_S1, E_S1, F_S1, G_S1, mi1_S1, mi2_S1, thetaO_S1] = self.Modelos_mecanismos('S1', AngE)

                    self.ax2_S1.clear()

                    self.ax2_S1.plot([A_S1[0], B_S1[0]], [A_S1[1], B_S1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S1.plot([A_S1[0], C_S1[0]], [A_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S1.plot([A_S1[0], D_S1[0]], [A_S1[1], D_S1[1]], '-og', markersize=4, alpha=0.5)
                    self.ax2_S1.plot([B_S1[0], E_S1[0]], [B_S1[1], E_S1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S1.plot([B_S1[0], F_S1[0]], [B_S1[1], F_S1[1]], '-or', markersize=4, alpha=0.5)
                    self.ax2_S1.plot([F_S1[0], E_S1[0]], [F_S1[1], E_S1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S1.plot([F_S1[0], G_S1[0]], [F_S1[1], G_S1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S1.plot([E_S1[0], D_S1[0]], [E_S1[1], D_S1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S1.plot([D_S1[0], C_S1[0]], [D_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S1.plot([G_S1[0], C_S1[0]], [G_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)
                    points_S1 = {'A': A_S1, 'B': B_S1, 'C': C_S1, 'D': D_S1, 'E': E_S1, 'F': F_S1, 'G': G_S1}

                    for letter, (x, y) in points_S1.items():
                        self.ax2_S1.text(x, y+2.5, letter, fontsize=12, ha='right')
                    
                    lines_S1 = [
                        ('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'E'), ('D', 'E'),
                        ('B', 'F'), ('C', 'D'), ('C', 'G'), ('G', 'F'), ('F', 'E')
                    ]
                    
                    if self.switches["Stephenson 1 Mostrar a numeração dos elos"].get() == 1:
                        for i, (start, end) in enumerate(lines_S1):
                            # Label each line
                            mid_x_S1 = (points_S1[start][0] + points_S1[end][0]) / 2
                            mid_y_S1= (points_S1[start][1] + points_S1[end][1]) / 2
                            self.ax2_S1.text(mid_x_S1, mid_y_S1, f'L{i+1}', fontsize=12, ha='center', va='center')
                    
                    self.ax2_S1.fill([A_S1[0], C_S1[0], D_S1[0]], [A_S1[1], C_S1[1], D_S1[1]], color='orange', alpha=0.5)
                    self.ax2_S1.fill([B_S1[0], E_S1[0], F_S1[0]], [B_S1[1], E_S1[1], F_S1[1]], color='gray', alpha=0.5)
                    
                    ArcoThetaI = Arc(xy=A_S1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(AngE))
                    ArcoThetaO = Arc(xy=B_S1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_S1))
                    angleMi1 = math.atan2((D_S1[1]-E_S1[1]),(D_S1[0]-E_S1[0]))
                    angleMi2 = math.atan2((C_S1[1]-G_S1[1]),(C_S1[0]-G_S1[0]))
                    ArcoMi1 = Arc(xy=E_S1, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_S1+angleMi1))
                    ArcoMi2 = Arc(xy=G_S1, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_S1+angleMi2))
                    self.ax2_S1.add_patch(ArcoThetaI)
                    self.ax2_S1.add_patch(ArcoThetaO)
                    self.ax2_S1.add_patch(ArcoMi1)
                    self.ax2_S1.add_patch(ArcoMi2)
                    self.ax2_S1.text(A_S1[0] + 5, A_S1[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                    self.ax2_S1.text(B_S1[0] + 5, B_S1[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                    self.ax2_S1.text(E_S1[0] + 5, E_S1[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                    self.ax2_S1.text(G_S1[0] + 5, G_S1[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                    self.ax2_S1.set_title("Mecanismo Stephenson 1")
                    self.ax2_S1.set_xlabel("Eixo X")   
                    self.ax2_S1.set_ylabel("Eixo Y")
                    self.ax2_S1.set_xlim(self.x_min_S1, self.x_max_S1)
                    self.ax2_S1.set_ylim(self.y_min_S1, self.y_max_S1)
                    self.canvas2_S1.draw()


                except:
                    thetaO_S1 = np.deg2rad(-1)
                strOutvalue = str(np.round(np.rad2deg(thetaO_S1),decimals=3))
                strvalue_S1 = str(round(value, 3))
                self.label6_S1.configure(text = "Valores \u03B8I: "+strvalue_S1)
                self.label6Out_S1.configure(text = "Valores \u03B8O: "+strOutvalue)

            elif self.combobox.get() == "Stephenson 2":
                try:

                    AngE = math.radians(value)
                    [A_S2, B_S2, C_S2, D_S2, E_S2, F_S2, G_S2, mi1_S2, mi2_S2, thetaO_S2] = self.Modelos_mecanismos('S2', AngE)

                    self.ax2_S2.clear()

                    self.ax2_S2.plot([A_S2[0], B_S2[0]], [A_S2[1], B_S2[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S2.plot([A_S2[0], C_S2[0]], [A_S2[1], C_S2[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S2.plot([A_S2[0], D_S2[0]], [A_S2[1], D_S2[1]], '-og', markersize=4, alpha=0.5)
                    self.ax2_S2.plot([B_S2[0], G_S2[0]], [B_S2[1], G_S2[1]], '-or', markersize=4, alpha=0.5)
                    self.ax2_S2.plot([G_S2[0], E_S2[0]], [G_S2[1], E_S2[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S2.plot([G_S2[0], F_S2[0]], [G_S2[1], F_S2[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S2.plot([E_S2[0], F_S2[0]], [E_S2[1], F_S2[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S2.plot([F_S2[0], D_S2[0]], [F_S2[1], D_S2[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S2.plot([D_S2[0], C_S2[0]], [D_S2[1], C_S2[1]], '-ok', markersize=4, alpha=0.5)
                    self.ax2_S2.plot([C_S2[0], E_S2[0]], [C_S2[1], E_S2[1]], '-ok', markersize=4, alpha=0.5)

                    points_S2 = {'A': A_S2, 'B': B_S2, 'C': C_S2, 'D': D_S2, 'E': E_S2, 'F': F_S2, 'G': G_S2}

                    for letter, (x, y) in points_S2.items():
                        self.ax2_S2.text(x, y+2.5, letter, fontsize=12, ha='right')
                    
                    lines_S2 = [
                        ('A', 'B'), ('A', 'D'), ('A', 'C'), ('C', 'E'), ('D', 'F'),
                        ('F', 'E'), ('C', 'D'), ('F', 'G'), ('G', 'B'), ('G', 'E')
                    ]

                    if self.switches["Stephenson 2 Mostrar a numeração dos elos"].get() == 1:
                        for i, (start, end) in enumerate(lines_S2):
                                # Label each line
                            mid_x_S2 = (points_S2[start][0] + points_S2[end][0]) / 2
                            mid_y_S2= (points_S2[start][1] + points_S2[end][1]) / 2
                            self.ax2_S2.text(mid_x_S2, mid_y_S2, f'L{i+1}', fontsize=12, ha='center', va='center')
                        
                    self.ax2_S2.fill([A_S2[0], D_S2[0], C_S2[0]], [A_S2[1], D_S2[1], C_S2[1]],color='orange', alpha=0.5)
                    self.ax2_S2.fill([G_S2[0], E_S2[0], F_S2[0]], [G_S2[1], E_S2[1], F_S2[1]], color='gray', alpha=0.5)

                    ArcoThetaI = Arc(xy=A_S2, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(AngE))
                    ArcoThetaO = Arc(xy=B_S2, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_S2))
                    angleMi1 = math.atan2((C_S2[1]-E_S2[1]),(C_S2[0]-E_S2[0]))
                    angleMi2 = math.atan2((F_S2[1]-G_S2[1]),(F_S2[0]-G_S2[0]))
                    ArcoMi1 = Arc(xy=E_S2, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_S2+angleMi1))
                    ArcoMi2 = Arc(xy=G_S2, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_S2+angleMi2))
                    self.ax2_S2.add_patch(ArcoThetaI)
                    self.ax2_S2.add_patch(ArcoThetaO)
                    self.ax2_S2.add_patch(ArcoMi1)
                    self.ax2_S2.add_patch(ArcoMi2)
                    self.ax2_S2.text(A_S2[0] + 5, A_S2[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                    self.ax2_S2.text(B_S2[0] + 5, B_S2[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                    self.ax2_S2.text(E_S2[0] + 5, E_S2[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                    self.ax2_S2.text(G_S2[0] + 5, G_S2[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                    self.ax2_S2.set_title("Mecanismo Stephenson 2")
                    self.ax2_S2.set_xlabel("Eixo X")   
                    self.ax2_S2.set_ylabel("Eixo Y")
                    self.ax2_S2.set_xlim(self.x_min_S2, self.x_max_S2)
                    self.ax2_S2.set_ylim(self.y_min_S2, self.y_max_S2)
                    self.canvas2_S2.draw()


                except:
                    thetaO_S2 = np.deg2rad(-1)
                
                strOutvalue = str(np.round(np.rad2deg(thetaO_S2),decimals=3))
                strvalue_S2 = str(round(value, 3))
                self.label6_S2.configure(text = "Valores \u03B8I: "+strvalue_S2)
                self.label6Out_S2.configure(text = "Valores \u03B8O: "+strOutvalue)

            elif self.combobox.get() == "Stephenson 3":

                try:

                    AngE = math.radians(value)
                    [A_S3, B_S3, C_S3, D_S3, E_S3, F_S3, G_S3, mi1_S3, mi2_S3, thetaO_S3] = self.Modelos_mecanismos('S3', AngE)

                    self.ax2_S3.clear()

                    self.ax2_S3.plot([A_S3[0], B_S3[0]], [A_S3[1], B_S3[1]], '-ok', markersize =4, alpha=0.5)
                    self.ax2_S3.plot([A_S3[0], C_S3[0]], [A_S3[1], C_S3[1]], '-ok', markersize =4, alpha=0.5)
                    self.ax2_S3.plot([A_S3[0], D_S3[0]], [A_S3[1], D_S3[1]], '-og', markersize =4, alpha=0.5)
                    self.ax2_S3.plot([B_S3[0], C_S3[0]], [B_S3[1], C_S3[1]], '-ok', markersize =4, alpha=0.5)
                    self.ax2_S3.plot([C_S3[0], F_S3[0]], [C_S3[1], F_S3[1]], '-ok', markersize =4, alpha=0.5)
                    self.ax2_S3.plot([D_S3[0], F_S3[0]], [D_S3[1], F_S3[1]], '-ok', markersize =4, alpha=0.5)
                    self.ax2_S3.plot([D_S3[0], E_S3[0]], [D_S3[1], E_S3[1]], '-ok', markersize =4, alpha=0.5)
                    self.ax2_S3.plot([F_S3[0], E_S3[0]], [F_S3[1], E_S3[1]], '-ok', markersize =4, alpha=0.5)
                    self.ax2_S3.plot([G_S3[0], E_S3[0]], [G_S3[1], E_S3[1]], '-ok', markersize =4, alpha=0.5)
                    self.ax2_S3.plot([G_S3[0], B_S3[0]], [G_S3[1], B_S3[1]], '-or', markersize =4, alpha=0.5)
                    points_S3 = {'A': A_S3, 'B': B_S3, 'C': C_S3, 'D': D_S3, 'E': E_S3, 'F': F_S3, 'G': G_S3}

                    for letter, (x, y) in points_S3.items():
                        self.ax2_S3.text(x, y+2.5, letter, fontsize=12, ha='right')

                    lines_S3 = [
                    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'F'), ('C', 'F'),
                    ('E', 'F'), ('D', 'E'), ('G', 'E'), ('G', 'B'), ('B', 'C')
                    ]

                    if self.switches["Stephenson 3 Mostrar a numeração dos elos"].get() == 1:
                        for i, (start, end) in enumerate(lines_S3):
                                # Label each line
                            mid_x_S3 = (points_S3[start][0] + points_S3[end][0]) / 2
                            mid_y_S3= (points_S3[start][1] + points_S3[end][1]) / 2
                            self.ax2_S3.text(mid_x_S3, mid_y_S3, f'L{i+1}', fontsize=12, ha='center', va='center')
    
                    self.ax2_S3.fill([A_S3[0], B_S3[0], C_S3[0]], [A_S3[1], B_S3[1], C_S3[1]],color='orange', alpha=0.5)
                    self.ax2_S3.fill([D_S3[0], E_S3[0], F_S3[0]], [D_S3[1], E_S3[1], F_S3[1]], color='gray', alpha=0.5)
                    
                    ArcoThetaI = Arc(xy=A_S3, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(AngE))
                    ArcoThetaO = Arc(xy=B_S3, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_S3))
                    angleMi1 = math.atan2((D_S3[1]-F_S3[1]),(D_S3[0]-F_S3[0]))
                    angleMi2 = math.atan2((E_S3[1]-G_S3[1]),(E_S3[0]-G_S3[0]))
                    ArcoMi1 = Arc(xy=F_S3, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_S3+angleMi1))
                    ArcoMi2 = Arc(xy=G_S3, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_S3+angleMi2))
                    self.ax2_S3.add_patch(ArcoThetaI)
                    self.ax2_S3.add_patch(ArcoThetaO)
                    self.ax2_S3.add_patch(ArcoMi1)
                    self.ax2_S3.add_patch(ArcoMi2)
                    self.ax2_S3.text(A_S3[0] + 5, A_S3[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                    self.ax2_S3.text(B_S3[0] + 5, B_S3[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                    self.ax2_S3.text(F_S3[0] + 5, F_S3[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                    self.ax2_S3.text(G_S3[0] + 5, G_S3[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                    self.ax2_S3.set_title("Mecanismo Stephenson 3")
                    self.ax2_S3.set_xlabel("Eixo X")   
                    self.ax2_S3.set_ylabel("Eixo Y")
                    self.ax2_S3.set_xlim(self.x_min_S3, self.x_max_S3)
                    self.ax2_S3.set_ylim(self.y_min_S3, self.y_max_S3)
                    self.canvas2_S3.draw()

                except:
                    thetaO_S3 = np.deg2rad(-1)

                strOutvalue = str(np.round(np.rad2deg(thetaO_S3),decimals=3))
                strvalue_S3 = str(round(value, 3))
                self.label6_S3.configure(text = "Valores \u03B8I: "+strvalue_S3)
                self.label6Out_S3.configure(text = "Valores \u03B8O: "+strOutvalue)

        except:
            a=111
            
    def mudar_configuracao(self, value):
        """Altera a visualização conforme a configuração selecionada na combobox.

        `value` indica a posição selecionada (1,2,...). A função redesenha
        o mecanismo correspondente com o conjunto de ângulos escolhido.
        """

        if self.combobox.get() == "Watt 1":
            # Laço que obtém 3600 (Entre 0 e 360 graus) valores do ângulo de saída e dos ângulos de qualidade de transmissão e armazena em vetores. 
            try:
                # Valor que corresponde a caixa seletora
                value = int(value)
                # Define o ângulo que será colocado na função Modelos_mecanismos
                AngE = self.thetaI_W1[value-1]
                [A_W1, B_W1, C_W1, D_W1, E_W1, F_W1, G_W1, mi1_W1, mi2_W1, thetaO_W1] = self.Modelos_mecanismos('W1', AngE)

                self.ax_W1.clear()
                # Plota o mecanismo no primeiro axis
                self.ax_W1.plot([A_W1[0], B_W1[0]], [A_W1[1], B_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([A_W1[0], C_W1[0]], [A_W1[1], C_W1[1]], '-og', markersize=4, alpha=0.5)
                self.ax_W1.plot([B_W1[0], D_W1[0]], [B_W1[1], D_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([B_W1[0], G_W1[0]], [B_W1[1], G_W1[1]], '-or', markersize=4, alpha=0.5)
                self.ax_W1.plot([G_W1[0], D_W1[0]], [G_W1[1], D_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([G_W1[0], F_W1[0]], [G_W1[1], F_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([D_W1[0], C_W1[0]], [D_W1[1], C_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([D_W1[0], E_W1[0]], [D_W1[1], E_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([C_W1[0], E_W1[0]], [C_W1[1], E_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([E_W1[0], F_W1[0]], [E_W1[1], F_W1[1]], '-ok', markersize=4, alpha=0.5)

                # Escreve as letras referentes a cada junta do mecanismo
                points_W1 = {'A': A_W1, 'B': B_W1, 'C': C_W1, 'D': D_W1, 'E': E_W1, 'F': F_W1, 'G': G_W1}
                for letter, (x, y) in points_W1.items():
                    self.ax_W1.text(x, y+2.5, letter, fontsize=12, ha='right')
                
                # Define a ordem dos elos que conectam cada junta
                lines_W1 = [
                    ('A', 'B'), ('A', 'C'), ('C', 'D'), ('B', 'D'), ('E', 'C'),
                    ('G', 'B'), ('D', 'E'), ('E', 'F'), ('F', 'G'), ('G', 'D')
                ]

                # Caso o interruptor seja ativado, escreve a nomenclatura de todos os elos (ex: L1) no primeiro axis
                if self.switches["Watt 1 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_W1):
                            # Label each line
                        mid_x_W1 = (points_W1[start][0] + points_W1[end][0]) / 2
                        mid_y_W1= (points_W1[start][1] + points_W1[end][1]) / 2
                        self.ax_W1.text(mid_x_W1, mid_y_W1, f'L{i+1}', fontsize=12, ha='center', va='center')

                # Preenche a àrea dos elos ternários do mecanismo de laranja e cinza
                self.ax_W1.fill([B_W1[0], G_W1[0], D_W1[0]], [B_W1[1], G_W1[1], D_W1[1]], color='orange', alpha=0.5)
                self.ax_W1.fill([C_W1[0], D_W1[0], E_W1[0]], [C_W1[1], D_W1[1], E_W1[1]], color='gray', alpha=0.5)
                
                ArcoThetaI = Arc(xy=A_W1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI_W1[value-1]))
                ArcoThetaO = Arc(xy=B_W1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_W1))
                angleMi1 = math.atan2((C_W1[1]-D_W1[1]),(C_W1[0]-D_W1[0]))
                angleMi2 = math.atan2((E_W1[1]-F_W1[1]),(E_W1[0]-F_W1[0]))
                ArcoMi1 = Arc(xy=D_W1, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_W1+angleMi1))
                ArcoMi2 = Arc(xy=F_W1, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_W1+angleMi2))
                self.ax_W1.add_patch(ArcoThetaI)
                self.ax_W1.add_patch(ArcoThetaO)
                self.ax_W1.add_patch(ArcoMi1)
                self.ax_W1.add_patch(ArcoMi2)
                self.ax_W1.text(A_W1[0] + 5, A_W1[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax_W1.text(B_W1[0] + 5, B_W1[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax_W1.text(D_W1[0] + 5, D_W1[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax_W1.text(F_W1[0] + 5, F_W1[1], r"$\mu$2", fontsize=12, ha='center', va='center')
                
                # Configuração geral do axis
                self.ax_W1.set_title("Mecanismo Watt 1")
                self.ax_W1.set_xlabel("Eixo X")   
                self.ax_W1.set_ylabel("Eixo Y")
                self.ax_W1.set_xlim(self.x_min_W1, self.x_max_W1)
                self.ax_W1.set_ylim(self.y_min_W1, self.y_max_W1)

                self.canvas_W1.draw()

            except:
                aaaaa =1

                # Para os outros mecanismos desta função (mostrar_angulos), o funcionamento segue o mesmo modelo deste.

        elif self.combobox.get() == "Watt 2":

            #try:
                
                value = int(value)
                AngE = self.thetaI[value-1]
                [A, B, C, D, E, F, G, mi1, mi2, thetaO] = self.Modelos_mecanismos('W2', AngE)
                
                self.ax.clear()
                self.ax.plot([A[0], B[0]], [A[1], B[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([B[0], C[0]], [B[1], C[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([C[0], E[0]], [C[1], E[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([C[0], F[0]], [C[1], F[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([A[0], D[0]], [A[1], D[1]], '-og', markersize=4, alpha=0.5)
                self.ax.plot([B[0], G[0]], [B[1], G[1]], '-or', markersize=4, alpha=0.5)
                self.ax.plot([D[0], E[0]], [D[1], E[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([E[0], F[0]], [E[1], F[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([F[0], G[0]], [F[1], G[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([B[0], C[0]], [B[1], C[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([A[0], C[0]], [A[1], C[1]], '-ok', markersize=4, alpha=0.5)

                points = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'G': G}

                for letter, (x, y) in points.items():
                    self.ax.text(x, y+2.5, letter, fontsize=12, ha='right')

                lines = [
                ('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'E'), ('E', 'C'),
                ('F', 'C'), ('E', 'F'), ('G', 'F'), ('B', 'G'), ('B', 'C')
                ]

                if self.switches["Watt 2 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines):
                            # Label each line
                        mid_x = (points[start][0] + points[end][0]) / 2
                        mid_y= (points[start][1] + points[end][1]) / 2
                        self.ax.text(mid_x, mid_y, f'L{i+1}', fontsize=12, ha='center', va='center')


                self.ax.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], color='orange', alpha=0.5)
                self.ax.fill([C[0], E[0], F[0]], [C[1], E[1], F[1]], color='gray', alpha=0.5)

                ArcoThetaI = Arc(xy=A, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI[value-1]))
                ArcoThetaO = Arc(xy=B, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO))
                angleMi1 = math.atan2((D[1]-E[1]),(D[0]-E[0]))
                angleMi2 = math.atan2((F[1]-G[1]),(F[0]-G[0]))
                ArcoMi1 = Arc(xy=E, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1+angleMi1))
                ArcoMi2 = Arc(xy=G, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2+angleMi2))
                self.ax.add_patch(ArcoThetaI)
                self.ax.add_patch(ArcoThetaO)
                self.ax.add_patch(ArcoMi1)
                self.ax.add_patch(ArcoMi2)
                self.ax.text(A[0] + 5, A[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax.text(B[0] + 5, B[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax.text(E[0] + 5, E[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax.text(G[0] + 5, G[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                self.ax.set_title("Mecanismo Watt 2")
                self.ax.set_xlabel("Eixo X")   
                self.ax.set_ylabel("Eixo Y")
                self.ax.set_xlim(self.x_min, self.x_max)
                self.ax.set_ylim(self.y_min, self.y_max)
                self.canvas.draw()             

            #except:
                aaaaaa=1

        elif self.combobox.get() == "Stephenson 1":
            
            try:    
                value = int(value)

                AngE = self.thetaI_S1[value-1]
                [A_S1, B_S1, C_S1, D_S1, E_S1, F_S1, G_S1, mi1_S1, mi2_S1, thetaO_S1] = self.Modelos_mecanismos('S1', AngE)
                
                self.ax_S1.clear()
                self.ax_S1.plot([A_S1[0], B_S1[0]], [A_S1[1], B_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([A_S1[0], C_S1[0]], [A_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([A_S1[0], D_S1[0]], [A_S1[1], D_S1[1]], '-og', markersize=4, alpha=0.5)
                self.ax_S1.plot([B_S1[0], E_S1[0]], [B_S1[1], E_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([B_S1[0], F_S1[0]], [B_S1[1], F_S1[1]], '-or', markersize=4, alpha=0.5)
                self.ax_S1.plot([F_S1[0], E_S1[0]], [F_S1[1], E_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([F_S1[0], G_S1[0]], [F_S1[1], G_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([E_S1[0], D_S1[0]], [E_S1[1], D_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([D_S1[0], C_S1[0]], [D_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([G_S1[0], C_S1[0]], [G_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)

                points_S1 = {'A': A_S1, 'B': B_S1, 'C': C_S1, 'D': D_S1, 'E': E_S1, 'F': F_S1, 'G': G_S1}
            
                for letter, (x, y) in points_S1.items():
                    self.ax_S1.text(x, y+2.5, letter, fontsize=12, ha='right')

                lines_S1 = [
                    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'E'), ('D', 'E'),
                    ('B', 'F'), ('C', 'D'), ('C', 'G'), ('G', 'F'), ('F', 'E')
                ]
                
                if self.switches["Stephenson 1 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_S1):
                        # Label each line
                        mid_x_S1 = (points_S1[start][0] + points_S1[end][0]) / 2
                        mid_y_S1= (points_S1[start][1] + points_S1[end][1]) / 2
                        self.ax_S1.text(mid_x_S1, mid_y_S1, f'L{i+1}', fontsize=12, ha='center', va='center')
                
                self.ax_S1.fill([A_S1[0], C_S1[0], D_S1[0]], [A_S1[1], C_S1[1], D_S1[1]], color='orange', alpha=0.5)
                self.ax_S1.fill([B_S1[0], E_S1[0], F_S1[0]], [B_S1[1], E_S1[1], F_S1[1]], color='gray', alpha=0.5)
                
                ArcoThetaI = Arc(xy=A_S1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI_S1[value-1]))
                ArcoThetaO = Arc(xy=B_S1, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_S1))
                angleMi1 = math.atan2((D_S1[1]-E_S1[1]),(D_S1[0]-E_S1[0]))
                angleMi2 = math.atan2((C_S1[1]-G_S1[1]),(C_S1[0]-G_S1[0]))
                ArcoMi1 = Arc(xy=E_S1, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_S1+angleMi1))
                ArcoMi2 = Arc(xy=G_S1, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_S1+angleMi2))
                self.ax_S1.add_patch(ArcoThetaI)
                self.ax_S1.add_patch(ArcoThetaO)
                self.ax_S1.add_patch(ArcoMi1)
                self.ax_S1.add_patch(ArcoMi2)
                self.ax_S1.text(A_S1[0] + 5, A_S1[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax_S1.text(B_S1[0] + 5, B_S1[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax_S1.text(E_S1[0] + 5, E_S1[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax_S1.text(G_S1[0] + 5, G_S1[1], r"$\mu$2", fontsize=12, ha='center', va='center')
                
                self.ax_S1.set_title("Mecanismo Stephenson 1")
                self.ax_S1.set_xlabel("Eixo X")   
                self.ax_S1.set_ylabel("Eixo Y")
                self.ax_S1.set_xlim(self.x_min_S1, self.x_max_S1)
                self.ax_S1.set_ylim(self.y_min_S1, self.y_max_S1)
                self.canvas_S1.draw()

            except:
                aaaaa =1    

        elif self.combobox.get() == "Stephenson 2":
            
            try:    
                value = int(value)

                AngE = self.thetaI_S2[value-1]
                [A_S2, B_S2, C_S2, D_S2, E_S2, F_S2, G_S2, mi1_S2, mi2_S2, thetaO_S2] = self.Modelos_mecanismos('S2', AngE)
                
                self.ax_S2.clear()
                self.ax_S2.plot([A_S2[0], B_S2[0]], [A_S2[1], B_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([A_S2[0], C_S2[0]], [A_S2[1], C_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([A_S2[0], D_S2[0]], [A_S2[1], D_S2[1]], '-og', markersize=4, alpha=0.5)
                self.ax_S2.plot([B_S2[0], G_S2[0]], [B_S2[1], G_S2[1]], '-or', markersize=4, alpha=0.5)
                self.ax_S2.plot([G_S2[0], E_S2[0]], [G_S2[1], E_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([G_S2[0], F_S2[0]], [G_S2[1], F_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([E_S2[0], F_S2[0]], [E_S2[1], F_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([F_S2[0], D_S2[0]], [F_S2[1], D_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([D_S2[0], C_S2[0]], [D_S2[1], C_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([C_S2[0], E_S2[0]], [C_S2[1], E_S2[1]], '-ok', markersize=4, alpha=0.5)

                points_S2 = {'A': A_S2, 'B': B_S2, 'C': C_S2, 'D': D_S2, 'E': E_S2, 'F': F_S2, 'G': G_S2}
                
                for letter, (x, y) in points_S2.items():
                    self.ax_S2.text(x, y+2.5, letter, fontsize=12, ha='right')

                lines_S2 = [
                    ('A', 'B'), ('A', 'D'), ('A', 'C'), ('C', 'E'), ('D', 'F'),
                    ('F', 'E'), ('C', 'D'), ('F', 'G'), ('G', 'B'), ('G', 'E')
                ]

                if self.switches["Stephenson 2 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_S2):
                            # Label each line
                        mid_x_S2 = (points_S2[start][0] + points_S2[end][0]) / 2
                        mid_y_S2= (points_S2[start][1] + points_S2[end][1]) / 2
                        self.ax_S2.text(mid_x_S2, mid_y_S2, f'L{i+1}', fontsize=12, ha='center', va='center')
                    

                self.ax_S2.fill([A_S2[0], D_S2[0], C_S2[0]], [A_S2[1], D_S2[1], C_S2[1]],color='orange', alpha=0.5)
                self.ax_S2.fill([G_S2[0], E_S2[0], F_S2[0]], [G_S2[1], E_S2[1], F_S2[1]], color='gray', alpha=0.5)

                ArcoThetaI = Arc(xy=A_S2, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI_S2[value-1]))
                ArcoThetaO = Arc(xy=B_S2, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_S2))
                angleMi1 = math.atan2((C_S2[1]-E_S2[1]),(C_S2[0]-E_S2[0]))
                angleMi2 = math.atan2((F_S2[1]-G_S2[1]),(F_S2[0]-G_S2[0]))
                ArcoMi1 = Arc(xy=E_S2, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_S2+angleMi1))
                ArcoMi2 = Arc(xy=G_S2, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_S2+angleMi2))
                self.ax_S2.add_patch(ArcoThetaI)
                self.ax_S2.add_patch(ArcoThetaO)
                self.ax_S2.add_patch(ArcoMi1)
                self.ax_S2.add_patch(ArcoMi2)
                self.ax_S2.text(A_S2[0] + 5, A_S2[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax_S2.text(B_S2[0] + 5, B_S2[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax_S2.text(E_S2[0] + 5, E_S2[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax_S2.text(G_S2[0] + 5, G_S2[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                self.ax_S2.set_title("Mecanismo Stephenson 2")
                self.ax_S2.set_xlabel("Eixo X")   
                self.ax_S2.set_ylabel("Eixo Y")
                self.ax_S2.set_xlim(self.x_min_S2, self.x_max_S2)
                self.ax_S2.set_ylim(self.y_min_S2, self.y_max_S2)
                self.canvas_S2.draw()

            except:
                aaaaa =1

        elif self.combobox.get() == "Stephenson 3":
            
            try:    
                value = int(value)

                AngE = self.thetaI_S3[value-1]
                [A_S3, B_S3, C_S3, D_S3, E_S3, F_S3, G_S3, mi1_S3, mi2_S3, thetaO_S3] = self.Modelos_mecanismos('S3', AngE)
                
                self.ax_S3.clear()
                self.ax_S3.plot([A_S3[0], B_S3[0]], [A_S3[1], B_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([A_S3[0], C_S3[0]], [A_S3[1], C_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([A_S3[0], D_S3[0]], [A_S3[1], D_S3[1]], '-og', markersize =4, alpha=0.5)
                self.ax_S3.plot([B_S3[0], C_S3[0]], [B_S3[1], C_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([C_S3[0], F_S3[0]], [C_S3[1], F_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([D_S3[0], F_S3[0]], [D_S3[1], F_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([D_S3[0], E_S3[0]], [D_S3[1], E_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([F_S3[0], E_S3[0]], [F_S3[1], E_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([G_S3[0], E_S3[0]], [G_S3[1], E_S3[1]], '-ok', markersize =4, alpha=0.5)
                self.ax_S3.plot([G_S3[0], B_S3[0]], [G_S3[1], B_S3[1]], '-or', markersize =4, alpha=0.5)

                points_S3 = {'A': A_S3, 'B': B_S3, 'C': C_S3, 'D': D_S3, 'E': E_S3, 'F': F_S3, 'G': G_S3}
            
                for letter, (x, y) in points_S3.items():
                    self.ax_S3.text(x, y+2.5, letter, fontsize=12, ha='right')

                lines_S3 = [
                ('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'F'), ('C', 'F'),
                ('E', 'F'), ('D', 'E'), ('G', 'E'), ('G', 'B'), ('B', 'C')
                ]

                if self.switches["Stephenson 3 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_S3):
                            # Label each line
                        mid_x_S3 = (points_S3[start][0] + points_S3[end][0]) / 2
                        mid_y_S3= (points_S3[start][1] + points_S3[end][1]) / 2
                        self.ax_S3.text(mid_x_S3, mid_y_S3, f'L{i+1}', fontsize=12, ha='center', va='center')
            
                self.ax_S3.fill([A_S3[0], B_S3[0], C_S3[0]], [A_S3[1], B_S3[1], C_S3[1]],color='orange', alpha=0.5)
                self.ax_S3.fill([D_S3[0], E_S3[0], F_S3[0]], [D_S3[1], E_S3[1], F_S3[1]], color='gray', alpha=0.5)
                
                ArcoThetaI = Arc(xy=A_S3, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(self.thetaI_S3[value-1]))
                ArcoThetaO = Arc(xy=B_S3, width=15, height=15, angle= 0, theta1 = 0, theta2 = np.rad2deg(thetaO_S3))
                angleMi1 = math.atan2((D_S3[1]-F_S3[1]),(D_S3[0]-F_S3[0]))
                angleMi2 = math.atan2((E_S3[1]-G_S3[1]),(E_S3[0]-G_S3[0]))
                ArcoMi1 = Arc(xy=F_S3, width=15, height=15, angle=0, theta1 = np.rad2deg(angleMi1), theta2 = np.rad2deg(mi1_S3+angleMi1))
                ArcoMi2 = Arc(xy=G_S3, width=15, height=15, angle= 0, theta1 = np.rad2deg(angleMi2), theta2 = np.rad2deg(mi2_S3+angleMi2))
                self.ax_S3.add_patch(ArcoThetaI)
                self.ax_S3.add_patch(ArcoThetaO)
                self.ax_S3.add_patch(ArcoMi1)
                self.ax_S3.add_patch(ArcoMi2)
                self.ax_S3.text(A_S3[0] + 5, A_S3[1], r"$\theta$I", fontsize=12, ha='center', va='center')
                self.ax_S3.text(B_S3[0] + 5, B_S3[1], r"$\theta$O", fontsize=12, ha='center', va='center')
                self.ax_S3.text(F_S3[0] + 5, F_S3[1], r"$\mu$1", fontsize=12, ha='center', va='center')
                self.ax_S3.text(G_S3[0] + 5, G_S3[1], r"$\mu$2", fontsize=12, ha='center', va='center')

                self.ax_S3.set_title("Mecanismo Stephenson 3")
                self.ax_S3.set_xlabel("Eixo X")   
                self.ax_S3.set_ylabel("Eixo Y")
                self.ax_S3.set_xlim(self.x_min_S3, self.x_max_S3)
                self.ax_S3.set_ylim(self.y_min_S3, self.y_max_S3)
                self.canvas_S3.draw()

            except:
                aaaaa =1

    def entregar_p_otimizar(self):
        """Lê entradas da UI e inicia o processo de otimização.

        Esta função coleta os pares de ângulos inseridos pelo usuário,
        configura variáveis iniciais e chama rotinas numéricas para
        encontrar parâmetros do mecanismo que atendam às especificações.
        """
        try:
            self.disable_interactives()
            # Reseta valores de textos da interface
            self.label7.configure(text="")
            self.label8.configure(text="")
            self.label9.configure(text="")
            self.label10.configure(text="")
            self.label11.configure(text="")
            self.label11x.configure(text="")
            self.label4.configure(text="")

            if self.combobox.get() == "Watt 1":
            # -----------------------------
            # Caso Watt 1: le os pares de ângulos (entrada/saída)
            # Abaixo há um conjunto de condicionais que detectam quantos
            # pares o usuário preench eu (1..4) e constroem os vetores
            # `self.thetaI_W1` e `self.thetaOd_W1` em radianos.
            # -----------------------------
                
            # Inicialização de variáveis
                self.thetaI_W1 = []
                self.thetaOd_W1 = []

            # Pega os valores de cada caixa de entrada fornecidos pelo usuário
                
                if ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI_W1 = np.array([math.radians(float(self.entries["Entrada 1"].get()))])
                    self.thetaOd_W1 = np.array([math.radians(float(self.entries["Saída 1"].get()))])
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI_W1 = np.array([math.radians(float(self.entries["Entrada 1"].get())), 
                                            math.radians(float(self.entries["Entrada 2"].get()))])
                    self.thetaOd_W1 = np.array([math.radians(float(self.entries["Saída 1"].get())), 
                                                math.radians(float(self.entries["Saída 2"].get()))])
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI_W1 = np.array([math.radians(float(self.entries["Entrada 1"].get())), 
                                            math.radians(float(self.entries["Entrada 2"].get())), 
                                            math.radians(float(self.entries["Entrada 3"].get()))])
                    self.thetaOd_W1 = np.array([math.radians(float(self.entries["Saída 1"].get())), 
                                                math.radians(float(self.entries["Saída 2"].get())), 
                                                math.radians(float(self.entries["Saída 3"].get()))])
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI_W1 = np.array([math.radians(float(self.entries["Entrada 1"].get())), 
                                            math.radians(float(self.entries["Entrada 2"].get())), 
                                            math.radians(float(self.entries["Entrada 3"].get())), 
                                            math.radians(float(self.entries["Entrada 4"].get()))])
                    self.thetaOd_W1 = np.array([math.radians(float(self.entries["Saída 1"].get())), 
                                                math.radians(float(self.entries["Saída 2"].get())), 
                                                math.radians(float(self.entries["Saída 3"].get())), 
                                                math.radians(float(self.entries["Saída 4"].get()))])
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() != "") & (self.entries["Saída 5"].get() != "")):
                    self.thetaI_W1 = np.array([math.radians(float(self.entries["Entrada 1"].get())), 
                                            math.radians(float(self.entries["Entrada 2"].get())), 
                                            math.radians(float(self.entries["Entrada 3"].get())), 
                                            math.radians(float(self.entries["Entrada 4"].get())), 
                                            math.radians(float(self.entries["Entrada 5"].get()))])
                    self.thetaOd_W1 = np.array([math.radians(float(self.entries["Saída 1"].get())), 
                                                math.radians(float(self.entries["Saída 2"].get())), 
                                                math.radians(float(self.entries["Saída 3"].get())), 
                                                math.radians(float(self.entries["Saída 4"].get())), 
                                                math.radians(float(self.entries["Saída 5"].get()))])
                elif ((self.entries["Entrada 1"].get() == "") & (self.entries["Saída 1"].get() == "") & 
                    (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI_W1 = np.array([math.radians(50), math.radians(71), math.radians(80), 
                                            math.radians(89), math.radians(100), math.radians(110)])
                    self.thetaOd_W1 = np.array([math.radians(20), math.radians(56), math.radians(59.57), 
                                                math.radians(70.17), math.radians(80), math.radians(93.8)])
                elif ((self.entries["Entrada 1"].get() == "1") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI_W1 = np.array([
                        math.radians(0.37), math.radians(3.32), math.radians(9.13), math.radians(17.68),
                        math.radians(28.75), math.radians(42.07), math.radians(57.30), math.radians(74.08),
                        math.radians(91.99), math.radians(110.58), math.radians(129.42), math.radians(148.01),
                        math.radians(165.92), math.radians(182.70), math.radians(197.93), math.radians(211.25),
                        math.radians(222.32), math.radians(230.87), math.radians(236.68), math.radians(239.63)
                    ])

                    self.thetaOd_W1 = np.array([
                        math.radians(14.29), math.radians(15.73), math.radians(18.78), math.radians(23.73),
                        math.radians(30.74), math.radians(39.49), math.radians(48.85), math.radians(56.77),
                        math.radians(60.88), math.radians(59.71), math.radians(53.80), math.radians(45.60),
                        math.radians(38.16), math.radians(33.51), math.radians(31.92), math.radians(32.47),
                        math.radians(33.91), math.radians(35.33), math.radians(36.32), math.radians(36.81)
                    ])
                else:
                    self.label4.configure(text="ERRO: Revise os dados preenchidos")
                    return

                if self.entries["Padrão: 50"].get() == "":
                    self.Delta_mi_W1 = 50
                else:
                    self.Delta_mi_W1 = float(self.entries["Padrão: 50"].get())
                
                # Define o limite superior e inferior que o ângulo de transmissão poderá assumir na otimização
                self.lb_W1 = math.radians(90-self.Delta_mi_W1)
                self.rb_W1 = math.radians(90 + self.Delta_mi_W1)

                self.label4.configure(text="Calculando...")

                self.n_W1 = len(self.thetaI_W1)
                # Limites inferiores e superiores para os valores que serão otimizados
                self.bounds_W1 = [[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[0, math.radians(360)], [math.radians(0), math.radians(360)],[math.radians(0), math.radians(360)]]
                start = time.time()

                # Entrega todos os dados para a função objetivo que otimizará o mecanismo
                self.result_W1 = scipy.optimize.differential_evolution(App.funcx_W1, self.bounds_W1, args=(self.thetaI_W1, self.thetaOd_W1, self.n_W1, self.lb_W1, self.rb_W1), tol=1e-2, atol=1e-4, maxiter = 2000, callback = self.callbackAtualizacao, workers = -1, updating='deferred', popsize = 15, strategy='randtobest1bin')
                end = time.time()

                self.label4.configure(text="Conferindo ordem e ângulos de transmissão")

                self.L1_W1 = self.result_W1.x[0]
                self.L2_W1 = self.result_W1.x[1]
                self.L3_W1 = self.result_W1.x[2]
                self.L4_W1 = self.result_W1.x[3]
                self.L5_W1 = self.result_W1.x[4]
                self.L6_W1 = self.result_W1.x[5]
                self.L8_W1 = self.result_W1.x[6]
                self.L9_W1 = self.result_W1.x[7]
                self.phi_W1 = self.result_W1.x[8]
                self.alpha_W1 = self.result_W1.x[9]
                self.lambda_W1 = self.result_W1.x[10]
                self.thetaO_W1 = []
                miok_W1 = 0
                mi11 =[]
                mi22 = []

                # Laço que verifica se os ângulos de saída otimizados estão de acordo com os ângulos de saída desejados (Com limiar de +-5).
                # Também verifica se os ângulos de transmissão de qualidade para cada ângulo de sáida otimizado está entre os limites definidos.
                for i in range(self.n_W1):
                    
                    AngE = self.thetaI_W1[i]
                    [A_W1, B_W1, C_W1, D_W1, E_W1, F_W1, G_W1, mi1_W1, mi2_W1, thetaO_W1] = self.Modelos_mecanismos('W1', AngE)
                    self.thetaO_W1.append(thetaO_W1)
                    mi11.append(math.degrees(mi1_W1))
                    mi22.append(math.degrees(mi2_W1))

                    if abs(np.rad2deg(self.thetaO_W1[i]) - math.degrees(self.thetaOd_W1[i])) > 5:
                        self.label4.configure(text="Erro")
                    else: 
                        if i == 0:
                            self.label7.configure(text="Ok")
                        elif i == 1:
                            self.label8.configure(text="Ok")
                        elif i == 2:
                            self.label9.configure(text="Ok")
                        elif i == 3:
                            self.label10.configure(text="Ok")
                        elif i == 4:   
                            self.label11.configure(text="Ok")

                    if (mi1_W1>self.lb_W1) and (mi1_W1<self.rb_W1) and (mi2_W1>self.lb_W1) and (mi2_W1<self.rb_W1):
                        miok_W1 = miok_W1 +1

                # Pega valores máximos e mínimos de todas as juntas em um alcance de 0 até o maior ângulo de entrada para definir os limites
                # de x e y nos gráficos. Ou seja, é feito para enquadrar o mecanismo no gráfico.
                THEI_W1 = [i for i in range(math.ceil(max(np.rad2deg(self.thetaI_W1))))]
                Ax_W1, Bx_W1, Cx_W1, Dx_W1, Ex_W1, Fx_W1, Gx_W1 = [],[],[],[],[],[],[]
                Ay_W1, By_W1, Cy_W1, Dy_W1, Ey_W1, Fy_W1, Gy_W1 = [],[],[],[],[],[],[]
    
                for i in range(len(THEI_W1)):
                    try:
                        AngE = math.radians(THEI_W1[i])
                        [A_W1, B_W1, C_W1, D_W1, E_W1, F_W1, G_W1, mi1_W1, mi2_W1, thetaO_W1] = self.Modelos_mecanismos('W1', AngE)

                        Ax_W1.append(A_W1[0]);Bx_W1.append(B_W1[0]);Cx_W1.append(C_W1[0]);Dx_W1.append(D_W1[0]);Ex_W1.append(E_W1[0]);Fx_W1.append(F_W1[0]);Gx_W1.append(G_W1[0])
                        Ay_W1.append(A_W1[1]);By_W1.append(B_W1[1]);Cy_W1.append(C_W1[1]);Dy_W1.append(D_W1[1]);Ey_W1.append(E_W1[1]);Fy_W1.append(F_W1[1]);Gy_W1.append(G_W1[1])
                    except:
                        a=0


                val_junt_X_W1 = [Ax_W1, Bx_W1, Cx_W1, Dx_W1, Ex_W1, Fx_W1, Gx_W1]
                val_junt_Y_W1 = [Ay_W1, By_W1, Cy_W1, Dy_W1, Ey_W1, Fy_W1, Gy_W1]
                flattened_X_W1 = [item for sublist in val_junt_X_W1 for item in sublist]
                flattened_Y_W1 = [item for sublist in val_junt_Y_W1 for item in sublist]
                self.x_min_W1 = min(flattened_X_W1) - 5
                self.y_min_W1 = min(flattened_Y_W1) - 5
                self.x_max_W1 = max(flattened_X_W1) + 5
                self.y_max_W1 = max(flattened_Y_W1) + 5
                        
                if miok_W1 == self.n_W1:
                    self.label11x.configure(text="Ok")
                else:
                    self.label4.configure(text="Erro")

                self.label4.configure(text="Finalizado")

                AngE = self.thetaI_W1[0]
                [A_W1, B_W1, C_W1, D_W1, E_W1, F_W1, G_W1, mi1_W1, mi2_W1, thetaO_W1] = self.Modelos_mecanismos('W1', AngE)

                # Define um data frame com dados importantes de otmização que serão exportados para uma planilha no excel
                marks_data = pd.DataFrame([{
                    'L1': round(self.L1_W1, 2),
                    'L2': round(self.L2_W1, 2),
                    'L3': round(self.L3_W1, 2),
                    'L4': round(self.L4_W1, 2),
                    'L5': round(self.L5_W1, 2),
                    'L6': round(self.L6_W1, 2),
                    'L8': round(self.L8_W1, 2),
                    'L9': round(self.L9_W1, 2),
                    'φ': round(math.degrees(self.phi_W1), 2),  # Phi symbol
                    'α': round(math.degrees(self.alpha_W1), 2),  # Alpha symbol
                    'λ': round(math.degrees(self.lambda_W1), 2),  # Lambda symbol
                    'μ1': np.round(mi11, 2).tolist(),  # Mu symbol
                    'μ2': np.round(mi22, 2).tolist(),  # Mu symbol
                    'θI': np.round(np.rad2deg(self.thetaI_W1), 2).tolist(),  # Theta symbol
                    'θOd': np.round(np.rad2deg(self.thetaOd_W1), 2).tolist(),  # Theta symbol
                    'θO': np.round(np.rad2deg(self.thetaO_W1), 2).tolist(),  # Theta symbol
                    'tempo otimizando': round(end - start, 2)
                }])

                file_name = 'MarksData_W1.xlsx'

                # saving the excel
                marks_data.to_excel(file_name)

                # Plota o mecanismo
                self.ax_W1.clear()
                self.ax_W1.plot([A_W1[0], B_W1[0]], [A_W1[1], B_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([A_W1[0], C_W1[0]], [A_W1[1], C_W1[1]], '-og', markersize=4, alpha=0.5)
                self.ax_W1.plot([B_W1[0], D_W1[0]], [B_W1[1], D_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([B_W1[0], G_W1[0]], [B_W1[1], G_W1[1]], '-or', markersize=4, alpha=0.5)
                self.ax_W1.plot([G_W1[0], D_W1[0]], [G_W1[1], D_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([G_W1[0], F_W1[0]], [G_W1[1], F_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([D_W1[0], C_W1[0]], [D_W1[1], C_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([D_W1[0], E_W1[0]], [D_W1[1], E_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([C_W1[0], E_W1[0]], [C_W1[1], E_W1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_W1.plot([E_W1[0], F_W1[0]], [E_W1[1], F_W1[1]], '-ok', markersize=4, alpha=0.5)

                # Escreve letras correspondentes a cada junta
                points_W1 = {'A': A_W1, 'B': B_W1, 'C': C_W1, 'D': D_W1, 'E': E_W1, 'F': F_W1, 'G': G_W1}
                for letter, (x, y) in points_W1.items():
                    self.ax_W1.text(x, y, letter, fontsize=12, ha='right')

                # Define ordem dos elos
                lines_W1 = [
                        ('A', 'B'), ('A', 'C'), ('C', 'D'), ('B', 'D'), ('C', 'E'),
                        ('D', 'G'), ('E', 'D'), ('E', 'F'), ('G', 'B'), ('F', 'G')
                    ]

                # Caso a interrupção seja ativada, mostra a numeração dos elos (ex: L1)
                if self.switches["Watt 1 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_W1):
                            # Label each line
                        mid_x_W1 = (points_W1[start][0] + points_W1[end][0]) / 2
                        mid_y_W1= (points_W1[start][1] + points_W1[end][1]) / 2
                        self.ax_W1.text(mid_x_W1, mid_y_W1, f'L{i+1}', fontsize=12, ha='center', va='center')

                # preenche os elos ternários com as cores laranja e cinza
                self.ax_W1.fill([B_W1[0], G_W1[0], D_W1[0]], [B_W1[1], G_W1[1], D_W1[1]], color='orange', alpha=0.5)
                self.ax_W1.fill([C_W1[0], D_W1[0], E_W1[0]], [C_W1[1], D_W1[1], E_W1[1]], color='gray', alpha=0.5)

                #Configurações gerais do axis
                self.ax_W1.set_title("Mecanismo Watt 1")
                self.ax_W1.set_xlabel("Eixo X")   
                self.ax_W1.set_ylabel("Eixo Y")
                self.ax_W1.set_xlim(self.x_min_W1, self.x_max_W1)
                self.ax_W1.set_ylim(self.y_min_W1, self.y_max_W1)
                self.canvas_W1.draw()
                self.fig_W1.savefig('destination_path_W1.svg', format='svg')


                # Mostra dados de otimização na interface
                AngSaidaTex_W1 = ', '.join(str(x) for x in np.round(np.rad2deg(self.thetaO_W1), decimals = 3))
                self.label14_W1.configure(text=AngSaidaTex_W1)

                valoresotimizados_W1 = [round(self.L1_W1,3),round(self.L2_W1,3),round(self.L3_W1,3),round(self.L4_W1,3),round(self.L5_W1,3), round(self.L6_W1,3), round(self.L8_W1,3),round(self.L9_W1,3),round(math.degrees(self.phi_W1),3),round(math.degrees(self.alpha_W1),3),round(math.degrees(self.lambda_W1),3)]
                valoresotimizadosTex_W1 = ', '.join(str(x) for x in valoresotimizados_W1)
                self.label16_W1.configure(text=valoresotimizadosTex_W1)

                # Para os outros mecanismos desta função, o funcionamento segue o mesmo modelo deste.

            # -----------------------------
            # Caso Watt 2: leitura de pares de ângulos e preparação para otimização
            # Formato análogo ao caso Watt 1, com vetores `self.thetaI` e
            # `self.thetaOd` em radianos.
            # -----------------------------
            elif self.combobox.get() == "Watt 2":

                self.thetaI = []
                self.thetaOd = []
                
                if ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI = np.array([math.radians(float(self.entries["Entrada 1"].get()))])
                    self.thetaOd = np.array([math.radians(float(self.entries["Saída 1"].get()))])
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get()))])
                    self.thetaOd = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get()))])
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get()))])
                    self.thetaOd = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get()))])
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get())), math.radians(float(self.entries["Entrada 4"].get()))])
                    self.thetaOd = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get())), math.radians(float(self.entries["Saída 4"].get()))])
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() != "") & (self.entries["Saída 5"].get() != "")):
                    self.thetaI = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get())), math.radians(float(self.entries["Entrada 4"].get())), math.radians(float(self.entries["Entrada 5"].get()))])
                    self.thetaOd = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get())), math.radians(float(self.entries["Saída 4"].get())), math.radians(float(self.entries["Saída 5"].get()))])
                
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() != "") & (self.entries["Saída 5"].get() != "")):
                    self.thetaI = np.array([math.radians(float(self.entries["Entrada 1"].get())), 
                                            math.radians(float(self.entries["Entrada 2"].get())), 
                                            math.radians(float(self.entries["Entrada 3"].get())), 
                                            math.radians(float(self.entries["Entrada 4"].get())), 
                                            math.radians(float(self.entries["Entrada 5"].get()))])
                    self.thetaOd = np.array([math.radians(float(self.entries["Saída 1"].get())), 
                                                math.radians(float(self.entries["Saída 2"].get())), 
                                                math.radians(float(self.entries["Saída 3"].get())), 
                                                math.radians(float(self.entries["Saída 4"].get())), 
                                                math.radians(float(self.entries["Saída 5"].get()))])
                    
                elif ((self.entries["Entrada 1"].get() == "") & (self.entries["Saída 1"].get() == "") & 
                    (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI = np.array([
                        math.radians(0.181), math.radians(1.629), math.radians(4.513), math.radians(8.810),
                        math.radians(14.485), math.radians(21.493), math.radians(29.777), math.radians(39.270),
                        math.radians(49.897), math.radians(61.571), math.radians(74.199), math.radians(87.678),
                        math.radians(101.901), math.radians(116.753), math.radians(132.113), math.radians(147.860),
                        math.radians(163.865), math.radians(180.000), math.radians(196.135), math.radians(212.140),
                        math.radians(227.887), math.radians(243.247), math.radians(258.099), math.radians(272.322),
                        math.radians(285.801), math.radians(298.429), math.radians(310.103), math.radians(320.730),
                        math.radians(330.223), math.radians(338.507), math.radians(345.515), math.radians(351.190),
                        math.radians(355.487), math.radians(358.371), math.radians(359.819)
                    ])

                    self.thetaOd = np.array([
                        math.radians(0.153689), math.radians(1.345134), math.radians(3.515762), math.radians(6.205697),
                        math.radians(8.679246), math.radians(9.987203), math.radians(9.209976), math.radians(5.881364),
                        math.radians(0.386127), math.radians(-6.039273), math.radians(-11.887996), math.radians(-16.170413),
                        math.radians(-18.727994), math.radians(-19.945016), math.radians(-20.444563), math.radians(-21.031757),
                        math.radians(-22.460632), math.radians(-25.084347), math.radians(-29.019430), math.radians(-34.463506),
                        math.radians(-41.245032), math.radians(-48.207226), math.radians(-53.695682), math.radians(-56.635104),
                        math.radians(-56.763686), math.radians(-54.085410), math.radians(-48.645379), math.radians(-40.867413),
                        math.radians(-31.771521), math.radians(-22.682751), math.radians(-14.721443), math.radians(-8.496894),
                        math.radians(-4.123539), math.radians(-1.424592), math.radians(-0.154673)
                    ])
                elif ((self.entries["Entrada 1"].get() == "1") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI = np.array([
                        math.radians(0.37), math.radians(3.32), math.radians(9.13), math.radians(17.68),
                        math.radians(28.75), math.radians(42.07), math.radians(57.30), math.radians(74.08),
                        math.radians(91.99), math.radians(110.58), math.radians(129.42), math.radians(148.01),
                        math.radians(165.92), math.radians(182.70), math.radians(197.93), math.radians(211.25),
                        math.radians(222.32), math.radians(230.87), math.radians(236.68), math.radians(239.63)
                    ])

                    self.thetaOd = np.array([
                        math.radians(14.29), math.radians(15.73), math.radians(18.78), math.radians(23.73),
                        math.radians(30.74), math.radians(39.49), math.radians(48.85), math.radians(56.77),
                        math.radians(60.88), math.radians(59.71), math.radians(53.80), math.radians(45.60),
                        math.radians(38.16), math.radians(33.51), math.radians(31.92), math.radians(32.47),
                        math.radians(33.91), math.radians(35.33), math.radians(36.32), math.radians(36.81)
                    ])
                elif ((self.entries["Entrada 1"].get() == "11") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI = np.array([
                        math.radians(359.819), math.radians(358.371), math.radians(355.487), math.radians(351.190),
                        math.radians(345.515), math.radians(338.507), math.radians(330.223), math.radians(320.730),
                        math.radians(310.103), math.radians(298.429), math.radians(285.801), math.radians(272.322),
                        math.radians(258.099), math.radians(243.247), math.radians(227.887), math.radians(212.140),
                        math.radians(196.135), math.radians(180.000), math.radians(163.865), math.radians(147.860),
                        math.radians(132.113), math.radians(116.753), math.radians(101.901), math.radians(87.678),
                        math.radians(74.199), math.radians(61.571), math.radians(49.897), math.radians(39.270),
                        math.radians(29.777), math.radians(21.493), math.radians(14.485), math.radians(8.810),
                        math.radians(4.513), math.radians(1.629), math.radians(0.181)
                    ])

                    self.thetaOd = np.array([
                        math.radians(+0.003993), math.radians(+0.034021), math.radians(+0.083827), math.radians(+0.131962),
                        math.radians(+0.140663), math.radians(+0.041205), math.radians(-0.293884), math.radians(-1.085149),
                        math.radians(-2.660230), math.radians(-5.400312), math.radians(-9.577984), math.radians(-15.107274),
                        math.radians(-21.334624), math.radians(-27.071709), math.radians(-30.990287), math.radians(-32.244143),
                        math.radians(-30.929663), math.radians(-28.016479), math.radians(-24.746722), math.radians(-21.928729),
                        math.radians(-19.631086), math.radians(-17.428312), math.radians(-14.905608), math.radians(-12.000662),
                        math.radians(-8.994751), math.radians(-6.275680), math.radians(-4.109544), math.radians(-2.559295),
                        math.radians(-1.535663), math.radians(-0.892650), math.radians(-0.497793), math.radians(-0.258079),
                        math.radians(-0.116227), math.radians(-0.038214), math.radians(-0.004045)
                    ])
                elif ((self.entries["Entrada 1"].get() == "111") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI = np.array([
                        math.radians(359.819), math.radians(358.371), math.radians(355.487), math.radians(351.190),
                        math.radians(345.515), math.radians(338.507), math.radians(330.223), math.radians(320.730),
                        math.radians(310.103), math.radians(298.429), math.radians(285.801), math.radians(272.322),
                        math.radians(258.099), math.radians(243.247), math.radians(227.887), math.radians(212.140),
                        math.radians(196.135), math.radians(180.000), math.radians(163.865), math.radians(147.860),
                        math.radians(132.113), math.radians(116.753), math.radians(101.901), math.radians(87.678),
                        math.radians(74.199), math.radians(61.571), math.radians(49.897), math.radians(39.270),
                        math.radians(29.777), math.radians(21.493), math.radians(14.485), math.radians(8.810),
                        math.radians(4.513), math.radians(1.629), math.radians(0.181)
                    ])

                    self.thetaOd = np.array([
                        math.radians(-0.168853), math.radians(-1.561672), math.radians(-4.551444), math.radians(-9.443883),
                        math.radians(-16.420666), math.radians(-25.207716), math.radians(-34.784249), math.radians(-43.433399),
                        math.radians(-49.375104), math.radians(-51.736403), math.radians(-51.044852), math.radians(-48.711871),
                        math.radians(-46.198882), math.radians(-44.839344), math.radians(-45.579920), math.radians(-47.496290),
                        math.radians(-47.160457), math.radians(-41.783847), math.radians(-33.080108), math.radians(-25.771960),
                        math.radians(-22.285283), math.radians(-21.074605), math.radians(-19.758097), math.radians(-17.444599),
                        math.radians(-13.986443), math.radians(-9.097044), math.radians(-2.967841), math.radians(+3.158495),
                        math.radians(+7.628694), math.radians(+9.462576), math.radians(+8.790395), math.radians(+6.522731),
                        math.radians(+3.773340), math.radians(+1.459815), math.radians(+0.167591)
                    ])
                else:
                    self.label4.configure(text="ERRO: Revise os dados preenchidos")
                    return

                
                if self.entries["Padrão: 50"].get() == "":
                    self.Delta_mi = 50

                else:
                    self.Delta_mi = float(self.entries["Padrão: 50"].get())
                
                self.lb = math.radians(90-self.Delta_mi)
                self.rb = math.radians(90 + self.Delta_mi)

                self.label4.configure(text="Calculando...")

                self.n = len(self.thetaI)
                self.bounds = [[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[0, math.radians(360)], [math.radians(0), math.radians(360)],[math.radians(0), math.radians(360)]]
                start = time.time()
                self.result = scipy.optimize.differential_evolution(App.funcx, self.bounds, args=(self.thetaI, self.thetaOd, self.n, self.lb, self.rb), tol=1e-2, atol=1e-4, maxiter = 2000, callback = self.callbackAtualizacao, workers = -1, updating='deferred', popsize = 15, strategy='randtobest1bin')
                end = time.time()

                self.label4.configure(text="Conferindo ordem e ângulos de transmissão")

                self.L1 = self.result.x[0]
                self.L2 = self.result.x[1]
                self.L3 = self.result.x[2]
                self.L4 = self.result.x[3]
                self.L5 = self.result.x[4]
                self.L6 = self.result.x[5]
                self.L8 = self.result.x[6]
                self.L9 = self.result.x[7]
                self.phi = self.result.x[8]
                self.alpha1 = self.result.x[9]
                self.lambda1 = self.result.x[10]
                self.thetaO = []

                miok = 0
                mi11 = []
                mi22 = []
                for i in range(self.n):

                    AngE = self.thetaI[i]
                    [A, B, C, D, E, F, G, mi1, mi2, thetaO] = self.Modelos_mecanismos('W2', AngE)
                    self.thetaO.append(thetaO)

                    mi11.append(math.degrees(mi1))
                    mi22.append(math.degrees(mi2))

                    if abs(np.rad2deg(self.thetaO[i]) - np.rad2deg(self.thetaOd[i])) > 5:
                        self.label4.configure(text="Erro")
                    else: 
                        if i == 0:
                            self.label7.configure(text="Ok")
                        elif i == 1:
                            self.label8.configure(text="Ok")
                        elif i == 2:
                            self.label9.configure(text="Ok")
                        elif i == 3:
                            self.label10.configure(text="Ok")
                        elif i == 4:   
                            self.label11.configure(text="Ok")

                    if (mi1>self.lb) and (mi1<self.rb) and (mi2>self.lb) and (mi2<self.rb):
                        miok = miok +1
                        
                if miok == self.n:
                    self.label11x.configure(text="Ok")
                else:
                    self.label4.configure(text="Erro")

                THEI = [i for i in range(math.ceil(max(np.rad2deg(self.thetaI))))]
                Ax, Bx, Cx, Dx, Ex, Fx, Gx = [],[],[],[],[],[],[]
                Ay, By, Cy, Dy, Ey, Fy, Gy = [],[],[],[],[],[],[]
                
                for i in range(len(THEI)):
                    try:
                        AngE = math.radians(THEI[i])
                        [A, B, C, D, E, F, G, mi1, mi2, thetaO] = self.Modelos_mecanismos('W2', AngE)

                        Ax.append(A[0]);Bx.append(B[0]);Cx.append(C[0]);Dx.append(D[0]);Ex.append(E[0]);Fx.append(F[0]);Gx.append(G[0])
                        Ay.append(A[1]);By.append(B[1]);Cy.append(C[1]);Dy.append(D[1]);Ey.append(E[1]);Fy.append(F[1]);Gy.append(G[1])
                    except:
                        aaaa =2

                val_junt_X = [Ax, Bx, Cx, Dx, Ex, Fx, Gx]
                val_junt_Y = [Ay, By, Cy, Dy, Ey, Fy, Gy]
                flattened_X = [item for sublist in val_junt_X for item in sublist]
                flattened_Y = [item for sublist in val_junt_Y for item in sublist]
                self.x_min = min(flattened_X) - 5
                self.y_min = min(flattened_Y) - 5
                self.x_max = max(flattened_X) + 5
                self.y_max = max(flattened_Y) + 5

                self.label4.configure(text="Finalizado")

                AngE = self.thetaI[0]
                [A, B, C, D, E, F, G, mi1, mi2, thetaO] = self.Modelos_mecanismos('W2', AngE)

                marks_data = pd.DataFrame([{
                        'L1': round(self.L1, 2),
                        'L2': round(self.L2, 2),
                        'L3': round(self.L3, 2),
                        'L4': round(self.L4, 2),
                        'L5': round(self.L5, 2),
                        'L6': round(self.L6, 2),
                        'L8': round(self.L8, 2),
                        'L9': round(self.L9, 2),
                        'φ': round(math.degrees(self.phi), 2),  # Phi symbol
                        'α': round(math.degrees(self.alpha1), 2),  # Alpha symbol
                        'λ': round(math.degrees(self.lambda1), 2),  # Lambda symbol
                        'μ1': np.round(mi11, 2).tolist(),  # Mu symbol
                        'μ2': np.round(mi22, 2).tolist(),  # Mu symbol
                        'θI': np.round(np.rad2deg(self.thetaI), 2).tolist(),  # Theta symbol
                        'θOd': np.round(np.rad2deg(self.thetaOd), 2).tolist(),  # Theta symbol
                        'θO': np.round(np.rad2deg(self.thetaO), 2).tolist(),  # Theta symbol
                        'tempo otimizando': round(end - start, 2)
                }])

                file_name = 'MarksData_W2.xlsx'

                # saving the excel
                marks_data.to_excel(file_name)
                
                self.ax.clear()
                self.ax.plot([A[0], B[0]], [A[1], B[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([B[0], C[0]], [B[1], C[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([C[0], E[0]], [C[1], E[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([C[0], F[0]], [C[1], F[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([A[0], D[0]], [A[1], D[1]], '-og', markersize=4, alpha=0.5)
                self.ax.plot([B[0], G[0]], [B[1], G[1]], '-or', markersize=4, alpha=0.5)
                self.ax.plot([D[0], E[0]], [D[1], E[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([E[0], F[0]], [E[1], F[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([F[0], G[0]], [F[1], G[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([B[0], C[0]], [B[1], C[1]], '-ok', markersize=4, alpha=0.5)
                self.ax.plot([A[0], C[0]], [A[1], C[1]], '-ok', markersize=4, alpha=0.5)

                points = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'G': G}

                for letter, (x, y) in points.items():
                    self.ax.text(x, y, letter, fontsize=12, ha='right')

                lines = [
                    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'E'), ('E', 'C'),
                    ('F', 'C'), ('E', 'F'), ('G', 'F'), ('B', 'G'), ('B', 'C')
                ]

                if self.switches["Watt 2 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines):

                        mid_x = (points[start][0] + points[end][0]) / 2
                        mid_y= (points[start][1] + points[end][1]) / 2
                        self.ax.text(mid_x, mid_y, f'L{i+1}', fontsize=12, ha='center', va='center')

                self.ax.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], color='orange', alpha=0.5)
                self.ax.fill([C[0], E[0], F[0]], [C[1], E[1], F[1]], color='gray', alpha=0.5)
                self.ax.set_title("Mecanismo Watt 2")
                self.ax.set_xlabel("Eixo X")   
                self.ax.set_ylabel("Eixo Y")
                self.ax.set_xlim(self.x_min, self.x_max)
                self.ax.set_ylim(self.y_min, self.y_max)
                self.canvas.draw()
                self.fig.savefig('destination_path.svg', format='svg')
                
                AngSaidaTex = ', '.join(str(x) for x in np.round(np.rad2deg(self.thetaO), decimals = 3))
                self.label14.configure(text=AngSaidaTex)

                valoresotimizados = [round(self.L1,3),round(self.L2,3),round(self.L3,3),round(self.L4,3),round(self.L5,3),round(self.L6,3),round(self.L8,3),round(self.L9,3),round(math.degrees(self.phi),3),round(math.degrees(self.alpha1),3),round(math.degrees(self.lambda1),3)]
                valoresotimizadosTex = ', '.join(str(x) for x in valoresotimizados)
                self.label16.configure(text=valoresotimizadosTex)

            # -----------------------------
            # Caso Stephenson 1: leitura de pares de ângulos e preparação para otimização
            # Mesmo formato dos casos anteriores; constrói `thetaI_S1` e
            # `thetaOd_S1` em radianos a partir das entradas.
            # -----------------------------
            elif self.combobox.get() == "Stephenson 1":

                self.thetaI_S1 = []
                self.thetaOd_S1 = []

                if ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S1 = np.array([math.radians(float(self.entries["Entrada 1"].get()))])
                    self.thetaOd_S1 = np.array([math.radians(float(self.entries["Saída 1"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S1 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get()))])
                    self.thetaOd_S1 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S1 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get()))])
                    self.thetaOd_S1 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S1 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get())), math.radians(float(self.entries["Entrada 4"].get()))])
                    self.thetaOd_S1 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get())), math.radians(float(self.entries["Saída 4"].get()))])
                
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() != "") & (self.entries["Saída 5"].get() != "")):
                    self.thetaI_S1 = np.array([math.radians(float(self.entries["Entrada 1"].get())), 
                                            math.radians(float(self.entries["Entrada 2"].get())), 
                                            math.radians(float(self.entries["Entrada 3"].get())), 
                                            math.radians(float(self.entries["Entrada 4"].get())), 
                                            math.radians(float(self.entries["Entrada 5"].get()))])
                    self.thetaOd_S1 = np.array([math.radians(float(self.entries["Saída 1"].get())), 
                                                math.radians(float(self.entries["Saída 2"].get())), 
                                                math.radians(float(self.entries["Saída 3"].get())), 
                                                math.radians(float(self.entries["Saída 4"].get())), 
                                                math.radians(float(self.entries["Saída 5"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() != "") & (self.entries["Saída 5"].get() != "")):

                    self.thetaI_S1 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get())), math.radians(float(self.entries["Entrada 4"].get())), math.radians(float(self.entries["Entrada 5"].get()))])
                    self.thetaOd_S1 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get())), math.radians(float(self.entries["Saída 4"].get())), math.radians(float(self.entries["Saída 5"].get()))])
                elif ((self.entries["Entrada 1"].get() == "1") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI_S1 = np.array([
                        math.radians(0.37), math.radians(3.32), math.radians(9.13), math.radians(17.68),
                        math.radians(28.75), math.radians(42.07), math.radians(57.30), math.radians(74.08),
                        math.radians(91.99), math.radians(110.58), math.radians(129.42), math.radians(148.01),
                        math.radians(165.92), math.radians(182.70), math.radians(197.93), math.radians(211.25),
                        math.radians(222.32), math.radians(230.87), math.radians(236.68), math.radians(239.63)
                    ])

                    self.thetaOd_S1 = np.array([
                        math.radians(14.29), math.radians(15.73), math.radians(18.78), math.radians(23.73),
                        math.radians(30.74), math.radians(39.49), math.radians(48.85), math.radians(56.77),
                        math.radians(60.88), math.radians(59.71), math.radians(53.80), math.radians(45.60),
                        math.radians(38.16), math.radians(33.51), math.radians(31.92), math.radians(32.47),
                        math.radians(33.91), math.radians(35.33), math.radians(36.32), math.radians(36.81)
                    ])
                else:
                    self.label4.configure(text="ERRO: Revise os dados preenchidos")
                    return

                
                if self.entries["Padrão: 50"].get() == "":
                    self.Delta_mi_S1 = 50

                else:
                    self.Delta_mi_S1 = float(self.entries["Padrão: 50"].get())
                
                self.lb_S1 = math.radians(90-self.Delta_mi_S1)
                self.rb_S1 = math.radians(90 + self.Delta_mi_S1)

                self.label4.configure(text="Calculando...")

                self.n_S1 = len(self.thetaI_S1)
                self.bounds_S1 = [[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[math.radians(0), math.radians(359)], [math.radians(0), math.radians(359)],[math.radians(0), math.radians(359)]]
                start = time.time()
                self.result_S1 = scipy.optimize.differential_evolution(App.funcx_S1, self.bounds_S1, args=(self.thetaI_S1, self.thetaOd_S1, self.n_S1, self.lb_S1, self.rb_S1), tol=1e-2, atol=1e-4, maxiter = 2000, callback = self.callbackAtualizacao, workers = -1, updating='deferred', popsize = 15, strategy='randtobest1bin')
                end = time.time()

                self.label4.configure(text="Conferindo ordem e ângulos de transmissão")

                self.L1_S1 = self.result_S1.x[0]
                self.L2_S1 = self.result_S1.x[1]
                self.L3_S1 = self.result_S1.x[2]
                self.L4_S1 = self.result_S1.x[3]
                self.L5_S1 = self.result_S1.x[4]
                self.L6_S1 = self.result_S1.x[5]
                self.L8_S1 = self.result_S1.x[6]
                self.L9_S1 = self.result_S1.x[7]
                self.phi_S1 = self.result_S1.x[8]
                self.alpha1_S1 = self.result_S1.x[9]
                self.lambda1_S1 = self.result_S1.x[10]
                self.thetaO_S1 = []

                miok_S1 = 0
                mi11 = []
                mi22=[]
                for i in range(self.n_S1):
    
                    AngE = self.thetaI_S1[i]
                    [A_S1, B_S1, C_S1, D_S1, E_S1, F_S1, G_S1, mi1_S1, mi2_S1, thetaO_S1] = self.Modelos_mecanismos('S1', AngE)
                    self.thetaO_S1.append(thetaO_S1)

                    mi11.append(math.degrees(mi1_S1))
                    mi22.append(math.degrees(mi2_S1))

                    if abs(np.rad2deg(self.thetaO_S1[i]) - math.degrees(self.thetaOd_S1[i])) > 5:
                        self.label4.configure(text="Erro")
                    else: 
                        if i == 0:
                            self.label7.configure(text="Ok")
                        elif i == 1:
                            self.label8.configure(text="Ok")
                        elif i == 2:
                            self.label9.configure(text="Ok")
                        elif i == 3:
                            self.label10.configure(text="Ok")
                        elif i == 4:   
                            self.label11.configure(text="Ok")

                    if (mi1_S1>self.lb_S1) and (mi1_S1<self.rb_S1) and (mi2_S1>self.lb_S1) and (mi2_S1<self.rb_S1):
                        miok_S1 = miok_S1 +1
                        
                if miok_S1 == self.n_S1:
                    self.label11x.configure(text="Ok")
                else:
                    self.label4.configure(text="Erro")

                THEI_S1 = [i for i in range(math.ceil(max(np.rad2deg(self.thetaI_S1))))]
                Ax_S1, Bx_S1, Cx_S1, Dx_S1, Ex_S1, Fx_S1, Gx_S1 = [],[],[],[],[],[],[]
                Ay_S1, By_S1, Cy_S1, Dy_S1, Ey_S1, Fy_S1, Gy_S1 = [],[],[],[],[],[],[]

                for i in range(len(THEI_S1)):
                    try:
                        AngE = math.radians(THEI_S1[i])
                        [A_S1, B_S1, C_S1, D_S1, E_S1, F_S1, G_S1, mi1_S1, mi2_S1, thetaO_S1] = self.Modelos_mecanismos('S1', AngE)

                        Ax_S1.append(A_S1[0]);Bx_S1.append(B_S1[0]);Cx_S1.append(C_S1[0]);Dx_S1.append(D_S1[0]);Ex_S1.append(E_S1[0]);Fx_S1.append(F_S1[0]);Gx_S1.append(G_S1[0])
                        Ay_S1.append(A_S1[1]);By_S1.append(B_S1[1]);Cy_S1.append(C_S1[1]);Dy_S1.append(D_S1[1]);Ey_S1.append(E_S1[1]);Fy_S1.append(F_S1[1]);Gy_W1.append(G_S1[1])
                    except:
                        a=0

                val_junt_X_S1 = [Ax_S1, Bx_S1, Cx_S1, Dx_S1, Ex_S1, Fx_S1, Gx_S1]
                val_junt_Y_S1 = [Ay_S1, By_S1, Cy_S1, Dy_S1, Ey_S1, Fy_S1, Gy_S1]
                flattened_X_S1 = [item for sublist in val_junt_X_S1 for item in sublist]
                flattened_Y_S1 = [item for sublist in val_junt_Y_S1 for item in sublist]

                self.x_min_S1 = min(flattened_X_S1) - 5
                self.y_min_S1 = min(flattened_Y_S1) - 5
                self.x_max_S1 = max(flattened_X_S1) + 5
                self.y_max_S1 = max(flattened_Y_S1) + 5

                self.label4.configure(text="Finalizado")

                AngE = self.thetaI_S1[0]
                [A_S1, B_S1, C_S1, D_S1, E_S1, F_S1, G_S1, mi1_S1, mi2_S1, thetaO_S1] = self.Modelos_mecanismos('S1', AngE)

                marks_data = pd.DataFrame([{
                        'L1': round(self.L1_S1, 2),
                        'L2': round(self.L2_S1, 2),
                        'L3': round(self.L3_S1, 2),
                        'L4': round(self.L4_S1, 2),
                        'L5': round(self.L5_S1, 2),
                        'L6': round(self.L6_S1, 2),
                        'L8': round(self.L8_S1, 2),
                        'L9': round(self.L9_S1, 2),
                        'φ': round(math.degrees(self.phi_S1), 2),  # Phi symbol
                        'α': round(math.degrees(self.alpha1_S1), 2),  # Alpha symbol
                        'λ': round(math.degrees(self.lambda1_S1), 2),  # Lambda symbol
                        'μ1': np.round(mi11, 2).tolist(),  # Mu symbol
                        'μ2': np.round(mi22, 2).tolist(),  # Mu symbol
                        'θI': np.round(np.rad2deg(self.thetaI_S1), 2).tolist(),  # Theta symbol
                        'θOd': np.round(np.rad2deg(self.thetaOd_S1), 2).tolist(),  # Theta symbol
                        'θO': np.round(np.rad2deg(self.thetaO_S1), 2).tolist(),  # Theta symbol
                        'tempo otimizando': round(end - start, 2)

                }])

                file_name = 'MarksData_S1.xlsx'

                # saving the excel
                marks_data.to_excel(file_name)

                self.ax_S1.clear()
                self.ax_S1.plot([A_S1[0], B_S1[0]], [A_S1[1], B_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([A_S1[0], C_S1[0]], [A_S1[1], C_S1[1]], '-og', markersize=4, alpha=0.5)
                self.ax_S1.plot([A_S1[0], D_S1[0]], [A_S1[1], D_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([B_S1[0], E_S1[0]], [B_S1[1], E_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([B_S1[0], F_S1[0]], [B_S1[1], F_S1[1]], '-or', markersize=4, alpha=0.5)
                self.ax_S1.plot([F_S1[0], E_S1[0]], [F_S1[1], E_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([F_S1[0], G_S1[0]], [F_S1[1], G_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([E_S1[0], D_S1[0]], [E_S1[1], D_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([D_S1[0], C_S1[0]], [D_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S1.plot([G_S1[0], C_S1[0]], [G_S1[1], C_S1[1]], '-ok', markersize=4, alpha=0.5)
                points_S1 = {'A': A_S1, 'B': B_S1, 'C': C_S1, 'D': D_S1, 'E': E_S1, 'F': F_S1, 'G': G_S1}
                lines_S1 = [
                    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'E'), ('D', 'E'),
                    ('B', 'F'), ('C', 'D'), ('C', 'G'), ('G', 'F'), ('F', 'E')
                ]
                for letter, (x, y) in points_S1.items():
                    self.ax_S1.text(x, y, letter, fontsize=12, ha='right')

                if self.switches["Stephenson 1 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_S1):
                            # Label each line
                        mid_x_S1 = (points_S1[start][0] + points_S1[end][0]) / 2
                        mid_y_S1= (points_S1[start][1] + points_S1[end][1]) / 2
                        self.ax_S1.text(mid_x_S1, mid_y_S1, f'L{i+1}', fontsize=12, ha='center', va='center')
                    

                self.ax_S1.fill([A_S1[0], C_S1[0], D_S1[0]], [A_S1[1], C_S1[1], D_S1[1]], color='orange', alpha=0.5)
                self.ax_S1.fill([B_S1[0], E_S1[0], F_S1[0]], [B_S1[1], E_S1[1], F_S1[1]], color='gray', alpha=0.5)
                self.ax_S1.set_title("Mecanismo Stephenson 1")
                self.ax_S1.set_xlabel("Eixo X")   
                self.ax_S1.set_ylabel("Eixo Y")
                self.ax_S1.set_xlim(self.x_min_S1, self.x_max_S1)
                self.ax_S1.set_ylim(self.y_min_S1, self.y_max_S1)
                self.canvas_S1.draw()
                self.fig_S1.savefig('destination_path_S1.svg', format='svg')

                AngSaidaTex_S1 = ', '.join(str(x) for x in np.round(np.rad2deg(self.thetaO_S1), decimals = 3))
                self.label14_S1.configure(text=AngSaidaTex_S1)

                valoresotimizados_S1 = [round(self.L1_S1,3),round(self.L2_S1,3),round(self.L3_S1,3),round(self.L4_S1,3),round(self.L5_S1,3),round(self.L6_S1,3),round(self.L8_S1,3),round(self.L9_S1,3),round(math.degrees(self.phi_S1),3),round(math.degrees(self.alpha1_S1),3),round(math.degrees(self.lambda1_S1),3)]
                valoresotimizadosTex_S1 = ', '.join(str(x) for x in valoresotimizados_S1)
                self.label16_S1.configure(text=valoresotimizadosTex_S1)

            # -----------------------------
            # Caso Stephenson 2: leitura de pares de ângulos e preparação para otimização
            # Os pares são convertidos para radianos e armazenados em
            # `thetaI_S2` / `thetaOd_S2`.
            # -----------------------------
            elif self.combobox.get() == "Stephenson 2":

                self.thetaI_S2 = []
                self.thetaOd_S2 = []

                if ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S2 = np.array([math.radians(float(self.entries["Entrada 1"].get()))])
                    self.thetaOd_S2 = np.array([math.radians(float(self.entries["Saída 1"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S2 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get()))])
                    self.thetaOd_S2 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S2 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get()))])
                    self.thetaOd_S2 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S2 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get())), math.radians(float(self.entries["Entrada 4"].get()))])
                    self.thetaOd_S2 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get())), math.radians(float(self.entries["Saída 4"].get()))])
                
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() != "") & (self.entries["Saída 5"].get() != "")):
                    self.thetaI_S2 = np.array([math.radians(float(self.entries["Entrada 1"].get())), 
                                            math.radians(float(self.entries["Entrada 2"].get())), 
                                            math.radians(float(self.entries["Entrada 3"].get())), 
                                            math.radians(float(self.entries["Entrada 4"].get())), 
                                            math.radians(float(self.entries["Entrada 5"].get()))])
                    self.thetaOd_S2 = np.array([math.radians(float(self.entries["Saída 1"].get())), 
                                                math.radians(float(self.entries["Saída 2"].get())), 
                                                math.radians(float(self.entries["Saída 3"].get())), 
                                                math.radians(float(self.entries["Saída 4"].get())), 
                                                math.radians(float(self.entries["Saída 5"].get()))])

                elif ((self.entries["Entrada 1"].get() == "") & (self.entries["Saída 1"].get() == "") & 
                    (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI_S2 = np.array([
                        math.radians(0.181), math.radians(1.629), math.radians(4.513), math.radians(8.810),
                        math.radians(14.485), math.radians(21.493), math.radians(29.777), math.radians(39.270),
                        math.radians(49.897), math.radians(61.571), math.radians(74.199), math.radians(87.678),
                        math.radians(101.901), math.radians(116.753), math.radians(132.113), math.radians(147.860),
                        math.radians(163.865), math.radians(180.000), math.radians(196.135), math.radians(212.140),
                        math.radians(227.887), math.radians(243.247), math.radians(258.099), math.radians(272.322),
                        math.radians(285.801), math.radians(298.429), math.radians(310.103), math.radians(320.730),
                        math.radians(330.223), math.radians(338.507), math.radians(345.515), math.radians(351.190),
                        math.radians(355.487), math.radians(358.371), math.radians(359.819)
                    ])

                    self.thetaOd_S2 = np.array([
                        math.radians(0.153689), math.radians(1.345134), math.radians(3.515762), math.radians(6.205697),
                        math.radians(8.679246), math.radians(9.987203), math.radians(9.209976), math.radians(5.881364),
                        math.radians(0.386127), math.radians(-6.039273), math.radians(-11.887996), math.radians(-16.170413),
                        math.radians(-18.727994), math.radians(-19.945016), math.radians(-20.444563), math.radians(-21.031757),
                        math.radians(-22.460632), math.radians(-25.084347), math.radians(-29.019430), math.radians(-34.463506),
                        math.radians(-41.245032), math.radians(-48.207226), math.radians(-53.695682), math.radians(-56.635104),
                        math.radians(-56.763686), math.radians(-54.085410), math.radians(-48.645379), math.radians(-40.867413),
                        math.radians(-31.771521), math.radians(-22.682751), math.radians(-14.721443), math.radians(-8.496894),
                        math.radians(-4.123539), math.radians(-1.424592), math.radians(-0.154673)
                    ])
                elif ((self.entries["Entrada 1"].get() == "1") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI_S2 = np.array([
                        math.radians(0.37), math.radians(3.32), math.radians(9.13), math.radians(17.68),
                        math.radians(28.75), math.radians(42.07), math.radians(57.30), math.radians(74.08),
                        math.radians(91.99), math.radians(110.58), math.radians(129.42), math.radians(148.01),
                        math.radians(165.92), math.radians(182.70), math.radians(197.93), math.radians(211.25),
                        math.radians(222.32), math.radians(230.87), math.radians(236.68), math.radians(239.63)
                    ])

                    self.thetaOd_S2 = np.array([
                        math.radians(14.29), math.radians(15.73), math.radians(18.78), math.radians(23.73),
                        math.radians(30.74), math.radians(39.49), math.radians(48.85), math.radians(56.77),
                        math.radians(60.88), math.radians(59.71), math.radians(53.80), math.radians(45.60),
                        math.radians(38.16), math.radians(33.51), math.radians(31.92), math.radians(32.47),
                        math.radians(33.91), math.radians(35.33), math.radians(36.32), math.radians(36.81)
                    ])
                elif ((self.entries["Entrada 1"].get() == "11") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI_S2 = np.array([
                        math.radians(359.819), math.radians(358.371), math.radians(355.487), math.radians(351.190),
                        math.radians(345.515), math.radians(338.507), math.radians(330.223), math.radians(320.730),
                        math.radians(310.103), math.radians(298.429), math.radians(285.801), math.radians(272.322),
                        math.radians(258.099), math.radians(243.247), math.radians(227.887), math.radians(212.140),
                        math.radians(196.135), math.radians(180.000), math.radians(163.865), math.radians(147.860),
                        math.radians(132.113), math.radians(116.753), math.radians(101.901), math.radians(87.678),
                        math.radians(74.199), math.radians(61.571), math.radians(49.897), math.radians(39.270),
                        math.radians(29.777), math.radians(21.493), math.radians(14.485), math.radians(8.810),
                        math.radians(4.513), math.radians(1.629), math.radians(0.181)
                    ])

                    self.thetaOd_S2 = np.array([
                        math.radians(+0.003993), math.radians(+0.034021), math.radians(+0.083827), math.radians(+0.131962),
                        math.radians(+0.140663), math.radians(+0.041205), math.radians(-0.293884), math.radians(-1.085149),
                        math.radians(-2.660230), math.radians(-5.400312), math.radians(-9.577984), math.radians(-15.107274),
                        math.radians(-21.334624), math.radians(-27.071709), math.radians(-30.990287), math.radians(-32.244143),
                        math.radians(-30.929663), math.radians(-28.016479), math.radians(-24.746722), math.radians(-21.928729),
                        math.radians(-19.631086), math.radians(-17.428312), math.radians(-14.905608), math.radians(-12.000662),
                        math.radians(-8.994751), math.radians(-6.275680), math.radians(-4.109544), math.radians(-2.559295),
                        math.radians(-1.535663), math.radians(-0.892650), math.radians(-0.497793), math.radians(-0.258079),
                        math.radians(-0.116227), math.radians(-0.038214), math.radians(-0.004045)
                    ])
                elif ((self.entries["Entrada 1"].get() == "111") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI_S2 = np.array([
                        math.radians(359.819), math.radians(358.371), math.radians(355.487), math.radians(351.190),
                        math.radians(345.515), math.radians(338.507), math.radians(330.223), math.radians(320.730),
                        math.radians(310.103), math.radians(298.429), math.radians(285.801), math.radians(272.322),
                        math.radians(258.099), math.radians(243.247), math.radians(227.887), math.radians(212.140),
                        math.radians(196.135), math.radians(180.000), math.radians(163.865), math.radians(147.860),
                        math.radians(132.113), math.radians(116.753), math.radians(101.901), math.radians(87.678),
                        math.radians(74.199), math.radians(61.571), math.radians(49.897), math.radians(39.270),
                        math.radians(29.777), math.radians(21.493), math.radians(14.485), math.radians(8.810),
                        math.radians(4.513), math.radians(1.629), math.radians(0.181)
                    ])

                    self.thetaOd_S2 = np.array([
                        math.radians(-0.168853), math.radians(-1.561672), math.radians(-4.551444), math.radians(-9.443883),
                        math.radians(-16.420666), math.radians(-25.207716), math.radians(-34.784249), math.radians(-43.433399),
                        math.radians(-49.375104), math.radians(-51.736403), math.radians(-51.044852), math.radians(-48.711871),
                        math.radians(-46.198882), math.radians(-44.839344), math.radians(-45.579920), math.radians(-47.496290),
                        math.radians(-47.160457), math.radians(-41.783847), math.radians(-33.080108), math.radians(-25.771960),
                        math.radians(-22.285283), math.radians(-21.074605), math.radians(-19.758097), math.radians(-17.444599),
                        math.radians(-13.986443), math.radians(-9.097044), math.radians(-2.967841), math.radians(+3.158495),
                        math.radians(+7.628694), math.radians(+9.462576), math.radians(+8.790395), math.radians(+6.522731),
                        math.radians(+3.773340), math.radians(+1.459815), math.radians(+0.167591)
                    ])
                else:
                    self.label4.configure(text="ERRO: Revise os dados preenchidos")
                    return
                
                if self.entries["Padrão: 50"].get() == "":
                    self.Delta_mi_S2 = 50

                else:
                    self.Delta_mi_S2 = float(self.entries["Padrão: 50"].get())
                
                self.lb_S2 = math.radians(90-self.Delta_mi_S2)
                self.rb_S2 = math.radians(90 + self.Delta_mi_S2)

                self.label4.configure(text="Calculando...")

                self.n_S2 = len(self.thetaI_S2)
                self.bounds_S2 = [[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[0, math.radians(360)], [math.radians(0), math.radians(360)],[math.radians(0), math.radians(360)]]
                start = time.time()
                self.result_S2 = scipy.optimize.differential_evolution(App.funcx_S2, self.bounds_S2, args=(self.thetaI_S2, self.thetaOd_S2, self.n_S2, self.lb_S2, self.rb_S2), tol=1e-2, atol=1e-4, maxiter = 2000, callback = self.callbackAtualizacao, workers = -1, updating='deferred', popsize = 15, strategy='randtobest1bin')
                end = time.time()
                self.gammaVetor_S2 = []
                initial_guess = 1

                self.label4.configure(text="Conferindo ordem e ângulos de transmissão")

                self.L1_S2 = self.result_S2.x[0]
                self.L2_S2 = self.result_S2.x[1]
                self.L3_S2 = self.result_S2.x[2]
                self.L4_S2 = self.result_S2.x[3]
                self.L5_S2 = self.result_S2.x[4]
                self.L6_S2 = self.result_S2.x[5]
                self.L8_S2 = self.result_S2.x[6]
                self.L9_S2 = self.result_S2.x[7]
                self.phi_S2 = self.result_S2.x[8]
                self.alpha1_S2 = self.result_S2.x[9]
                self.lambda1_S2 = self.result_S2.x[10]

                for thetaIS2alpha in range(36000):
                    
                    try:
                        A_S2 = [0,0]
                        B_S2 = [self.L1_S2*math.cos(self.phi_S2),self.L1_S2*math.sin(self.phi_S2)]
                        C_S2 = [self.L3_S2*math.cos(np.deg2rad((thetaIS2alpha/100))+self.alpha1_S2),self.L3_S2*math.sin(np.deg2rad((thetaIS2alpha/100))+self.alpha1_S2)]
                        D_S2 = [self.L2_S2*math.cos(np.deg2rad((thetaIS2alpha/100))),self.L2_S2*math.sin(np.deg2rad((thetaIS2alpha/100)))]

                        def equation_to_solve(gamma_S2):
                            
                            E_S2 = [C_S2[0] + self.L4_S2 * math.cos(gamma_S2.item()), C_S2[1] + self.L4_S2 * math.sin(gamma_S2.item())]
                            e1_S2 = math.sqrt((E_S2[0] - D_S2[0]) ** 2 + (E_S2[1] - D_S2[1]) ** 2)
                            omega_S2 = math.atan2(E_S2[1] - D_S2[1], E_S2[0] - D_S2[0])
                            omega2_S2 = math.acos((e1_S2 ** 2 + self.L5_S2 ** 2 - self.L6_S2 ** 2) / (2 * e1_S2 * self.L5_S2))
                            F_S2 = [D_S2[0] + self.L5_S2 * math.cos(omega_S2 - omega2_S2), D_S2[1] + self.L5_S2 * math.sin(omega_S2 - omega2_S2)]
                            omega3_S2 = math.atan2(E_S2[1] - F_S2[1], E_S2[0] - F_S2[0])
                            G_S2 = [F_S2[0] + self.L8_S2 * math.cos(omega3_S2 - self.lambda1_S2), F_S2[1] + self.L8_S2 * math.sin(omega3_S2 - self.lambda1_S2)]

                            return self.L9_S2 - math.sqrt((G_S2[0] - B_S2[0]) ** 2 + (G_S2[1] - B_S2[1]) ** 2)

                        result = root(equation_to_solve, initial_guess, method='lm')
                        solution_gamma_S2 = result.x[0]        
                        initial_guess = solution_gamma_S2
                        self.gammaVetor_S2.append(solution_gamma_S2)
                    except:
                        self.gammaVetor_S2.append(0)
                    

                self.thetaO_S2 = []

                miok_S2 = 0
                mi11 = []
                mi22 = []
                for i in range(self.n_S2):

                    AngE = self.thetaI_S2[i]
                    [A_S2, B_S2, C_S2, D_S2, E_S2, F_S2, G_S2, mi1_S2, mi2_S2, thetaO_S2] = self.Modelos_mecanismos('S2', AngE)
                    self.thetaO_S2.append(thetaO_S2)
                    mi11.append(math.degrees(mi1_S2))
                    mi22.append(math.degrees(mi2_S2))

                    if abs(np.rad2deg(self.thetaO_S2[i]) - math.degrees(self.thetaOd_S2[i])) > 5:
                        self.label4.configure(text="Erro")
                    else: 
                        if i == 0:
                            self.label7.configure(text="Ok")
                        elif i == 1:
                            self.label8.configure(text="Ok")
                        elif i == 2:
                            self.label9.configure(text="Ok")
                        elif i == 3:
                            self.label10.configure(text="Ok")
                        elif i == 4:   
                            self.label11.configure(text="Ok")

                    if (mi1_S2>self.lb_S2) and (mi1_S2<self.rb_S2) and (mi2_S2>self.lb_S2) and (mi2_S2<self.rb_S2):
                        miok_S2 = miok_S2 +1
                        
                if miok_S2 == self.n_S2:
                    self.label11x.configure(text="Ok")
                else:
                    self.label4.configure(text="Erro")

                THEI_S2 = [i for i in range(math.ceil(max(np.rad2deg(self.thetaI_S2))))]
                Ax_S2, Bx_S2, Cx_S2, Dx_S2, Ex_S2, Fx_S2, Gx_S2 = [],[],[],[],[],[],[]
                Ay_S2, By_S2, Cy_S2, Dy_S2, Ey_S2, Fy_S2, Gy_S2 = [],[],[],[],[],[],[]

    
                for i in range(len(THEI_S2)):
                    try:    
                        AngE = math.radians(THEI_S2[i])
                        [A_S2, B_S2, C_S2, D_S2, E_S2, F_S2, G_S2, mi1_S2, mi2_S2, thetaO_S2] = self.Modelos_mecanismos('S2', AngE)

                        Ax_S2.append(A_S2[0]);Bx_S2.append(B_S2[0]);Cx_S2.append(C_S2[0]);Dx_S2.append(D_S2[0]);Ex_S2.append(E_S2[0]);Fx_S2.append(F_S2[0]);Gx_S2.append(G_S2[0])
                        Ay_S2.append(A_S2[1]);By_S2.append(B_S2[1]);Cy_S2.append(C_S2[1]);Dy_S2.append(D_S2[1]);Ey_S2.append(E_S2[1]);Fy_S2.append(F_S2[1]);Gy_S2.append(G_S2[1])
                    except:
                        a=0

                val_junt_X_S2 = [Ax_S2, Bx_S2, Cx_S2, Dx_S2, Ex_S2, Fx_S2, Gx_S2]
                val_junt_Y_S2 = [Ay_S2, By_S2, Cy_S2, Dy_S2, Ey_S2, Fy_S2, Gy_S2]
                flattened_X_S2 = [item for sublist in val_junt_X_S2 for item in sublist]
                flattened_Y_S2 = [item for sublist in val_junt_Y_S2 for item in sublist]
                self.x_min_S2 = min(flattened_X_S2) - 5
                self.y_min_S2 = min(flattened_Y_S2) - 5
                self.x_max_S2 = max(flattened_X_S2) + 5
                self.y_max_S2 = max(flattened_Y_S2) + 5

                self.label4.configure(text="Finalizado")

                AngE = self.thetaI_S2[0]
                [A_S2, B_S2, C_S2, D_S2, E_S2, F_S2, G_S2, mi1_S2, mi2_S2, thetaO_S2] = self.Modelos_mecanismos('S2', AngE)

                marks_data = pd.DataFrame([{
                        'L1': round(self.L1_S2, 2),
                        'L2': round(self.L2_S2, 2),
                        'L3': round(self.L3_S2, 2),
                        'L4': round(self.L4_S2, 2),
                        'L5': round(self.L5_S2, 2),
                        'L6': round(self.L6_S2, 2),
                        'L8': round(self.L8_S2, 2),
                        'L9': round(self.L9_S2, 2),
                        'φ': round(math.degrees(self.phi_S2), 2),  # Phi symbol
                        'α': round(math.degrees(self.alpha1_S2), 2),  # Alpha symbol
                        'λ': round(math.degrees(self.lambda1_S2), 2),  # Lambda symbol
                        'μ1': np.round(mi11, 2).tolist(),  # Mu symbol
                        'μ2': np.round(mi22, 2).tolist(),  # Mu symbol
                        'θI': np.round(np.rad2deg(self.thetaI_S2), 2).tolist(),  # Theta symbol
                        'θOd': np.round(np.rad2deg(self.thetaOd_S2), 2).tolist(),  # Theta symbol
                        'θO': np.round(np.rad2deg(self.thetaO_S2), 2).tolist(),  # Theta symbol
                        'tempo': round(end - start, 2)
                }])

                file_name = 'MarksData_S2.xlsx'

                # saving the excel
                marks_data.to_excel(file_name)

                self.ax_S2.clear()
                self.ax_S2.plot([A_S2[0], B_S2[0]], [A_S2[1], B_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([A_S2[0], C_S2[0]], [A_S2[1], C_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([A_S2[0], D_S2[0]], [A_S2[1], D_S2[1]], '-og', markersize=4, alpha=0.5)
                self.ax_S2.plot([B_S2[0], G_S2[0]], [B_S2[1], G_S2[1]], '-or', markersize=4, alpha=0.5)
                self.ax_S2.plot([G_S2[0], E_S2[0]], [G_S2[1], E_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([G_S2[0], F_S2[0]], [G_S2[1], F_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([E_S2[0], F_S2[0]], [E_S2[1], F_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([F_S2[0], D_S2[0]], [F_S2[1], D_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([D_S2[0], C_S2[0]], [D_S2[1], C_S2[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S2.plot([C_S2[0], E_S2[0]], [C_S2[1], E_S2[1]], '-ok', markersize=4, alpha=0.5)

                points_S2 = {'A': A_S2, 'B': B_S2, 'C': C_S2, 'D': D_S2, 'E': E_S2, 'F': F_S2, 'G': G_S2}
                lines_S2 = [
                    ('A', 'B'), ('A', 'D'), ('A', 'C'), ('C', 'E'), ('D', 'F'),
                    ('F', 'E'), ('C', 'D'), ('F', 'G'), ('G', 'B'), ('G', 'E')
                ]
                for letter, (x, y) in points_S2.items():
                    self.ax_S2.text(x, y, letter, fontsize=12, ha='right')

                if self.switches["Stephenson 2 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_S2):
                            # Label each line
                        mid_x_S2 = (points_S2[start][0] + points_S2[end][0]) / 2
                        mid_y_S2= (points_S2[start][1] + points_S2[end][1]) / 2
                        self.ax_S2.text(mid_x_S2, mid_y_S2, f'L{i+1}', fontsize=12, ha='center', va='center')
                    

                self.ax_S2.fill([A_S2[0], D_S2[0], C_S2[0]], [A_S2[1], D_S2[1], C_S2[1]],color='orange', alpha=0.5)
                self.ax_S2.fill([G_S2[0], E_S2[0], F_S2[0]], [G_S2[1], E_S2[1], F_S2[1]], color='gray', alpha=0.5)
                self.ax_S2.set_title("Mecanismo Stephenson 3")
                self.ax_S2.set_xlabel("Eixo X")   
                self.ax_S2.set_ylabel("Eixo Y")
                self.ax_S2.set_xlim(self.x_min_S2, self.x_max_S2)
                self.ax_S2.set_ylim(self.y_min_S2, self.y_max_S2)
                self.canvas_S2.draw()
                self.fig_S2.savefig('destination_path_S2.svg', format='svg')

                AngSaidaTex_S2 = ', '.join(str(x) for x in np.round(np.rad2deg(self.thetaO_S2), decimals = 3))
                self.label14_S2.configure(text=AngSaidaTex_S2)

                valoresotimizados_S2 = [round(self.L1_S2,3),round(self.L2_S2,3),round(self.L3_S2,3),round(self.L4_S2,3),round(self.L5_S2,3),round(self.L6_S2,3),round(self.L8_S2,3),round(self.L9_S2,3),round(math.degrees(self.phi_S2),3),round(math.degrees(self.alpha1_S2),3),round(math.degrees(self.lambda1_S2),3)]
                valoresotimizadosTex_S2 = ', '.join(str(x) for x in valoresotimizados_S2)
                self.label16_S2.configure(text=valoresotimizadosTex_S2)

            elif self.combobox.get() == "Stephenson 3":


                # Get the input values and store them in instance variables
                self.thetaI_S3 = []
                self.thetaOd_S3 = []

                if ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S3 = np.array([math.radians(float(self.entries["Entrada 1"].get()))])
                    self.thetaOd_S3 = np.array([math.radians(float(self.entries["Saída 1"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S3 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get()))])
                    self.thetaOd_S3 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S3 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get()))])
                    self.thetaOd_S3 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get()))])

                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                    self.thetaI_S3 = np.array([math.radians(float(self.entries["Entrada 1"].get())), math.radians(float(self.entries["Entrada 2"].get())), math.radians(float(self.entries["Entrada 3"].get())), math.radians(float(self.entries["Entrada 4"].get()))])
                    self.thetaOd_S3 = np.array([math.radians(float(self.entries["Saída 1"].get())), math.radians(float(self.entries["Saída 2"].get())), math.radians(float(self.entries["Saída 3"].get())), math.radians(float(self.entries["Saída 4"].get()))])
                
                elif ((self.entries["Entrada 1"].get() != "") & (self.entries["Saída 1"].get() != "") & 
                    (self.entries["Entrada 2"].get() != "") & (self.entries["Saída 2"].get() != "") & 
                    (self.entries["Entrada 3"].get() != "") & (self.entries["Saída 3"].get() != "") & 
                    (self.entries["Entrada 4"].get() != "") & (self.entries["Saída 4"].get() != "") & 
                    (self.entries["Entrada 5"].get() != "") & (self.entries["Saída 5"].get() != "")):
                    self.thetaI_S3 = np.array([math.radians(float(self.entries["Entrada 1"].get())), 
                                            math.radians(float(self.entries["Entrada 2"].get())), 
                                            math.radians(float(self.entries["Entrada 3"].get())), 
                                            math.radians(float(self.entries["Entrada 4"].get())), 
                                            math.radians(float(self.entries["Entrada 5"].get()))])
                    self.thetaOd_S3 = np.array([math.radians(float(self.entries["Saída 1"].get())), 
                                                math.radians(float(self.entries["Saída 2"].get())), 
                                                math.radians(float(self.entries["Saída 3"].get())), 
                                                math.radians(float(self.entries["Saída 4"].get())), 
                                                math.radians(float(self.entries["Saída 5"].get()))])

                elif ((self.entries["Entrada 1"].get() == "") & (self.entries["Saída 1"].get() == "") & 
                    (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") & 
                    (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") & 
                    (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") & 
                    (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):
                    self.thetaI_S3 = np.array([
                        math.radians(0.181), math.radians(1.629), math.radians(4.513), math.radians(8.810),
                        math.radians(14.485), math.radians(21.493), math.radians(29.777), math.radians(39.270),
                        math.radians(49.897), math.radians(61.571), math.radians(74.199), math.radians(87.678),
                        math.radians(101.901), math.radians(116.753), math.radians(132.113), math.radians(147.860),
                        math.radians(163.865), math.radians(180.000), math.radians(196.135), math.radians(212.140),
                        math.radians(227.887), math.radians(243.247), math.radians(258.099), math.radians(272.322),
                        math.radians(285.801), math.radians(298.429), math.radians(310.103), math.radians(320.730),
                        math.radians(330.223), math.radians(338.507), math.radians(345.515), math.radians(351.190),
                        math.radians(355.487), math.radians(358.371), math.radians(359.819)
                    ])

                    self.thetaOd_S3 = np.array([
                        math.radians(0.153689), math.radians(1.345134), math.radians(3.515762), math.radians(6.205697),
                        math.radians(8.679246), math.radians(9.987203), math.radians(9.209976), math.radians(5.881364),
                        math.radians(0.386127), math.radians(-6.039273), math.radians(-11.887996), math.radians(-16.170413),
                        math.radians(-18.727994), math.radians(-19.945016), math.radians(-20.444563), math.radians(-21.031757),
                        math.radians(-22.460632), math.radians(-25.084347), math.radians(-29.019430), math.radians(-34.463506),
                        math.radians(-41.245032), math.radians(-48.207226), math.radians(-53.695682), math.radians(-56.635104),
                        math.radians(-56.763686), math.radians(-54.085410), math.radians(-48.645379), math.radians(-40.867413),
                        math.radians(-31.771521), math.radians(-22.682751), math.radians(-14.721443), math.radians(-8.496894),
                        math.radians(-4.123539), math.radians(-1.424592), math.radians(-0.154673)
                    ])
                elif ((self.entries["Entrada 1"].get() == "1") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI_S3 = np.array([
                        math.radians(0.37), math.radians(3.32), math.radians(9.13), math.radians(17.68),
                        math.radians(28.75), math.radians(42.07), math.radians(57.30), math.radians(74.08),
                        math.radians(91.99), math.radians(110.58), math.radians(129.42), math.radians(148.01),
                        math.radians(165.92), math.radians(182.70), math.radians(197.93), math.radians(211.25),
                        math.radians(222.32), math.radians(230.87), math.radians(236.68), math.radians(239.63)
                    ])

                    self.thetaOd_S3 = np.array([
                        math.radians(14.29), math.radians(15.73), math.radians(18.78), math.radians(23.73),
                        math.radians(30.74), math.radians(39.49), math.radians(48.85), math.radians(56.77),
                        math.radians(60.88), math.radians(59.71), math.radians(53.80), math.radians(45.60),
                        math.radians(38.16), math.radians(33.51), math.radians(31.92), math.radians(32.47),
                        math.radians(33.91), math.radians(35.33), math.radians(36.32), math.radians(36.81)
                    ])
                elif ((self.entries["Entrada 1"].get() == "11") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI_S3 = np.array([
                        math.radians(359.819), math.radians(358.371), math.radians(355.487), math.radians(351.190),
                        math.radians(345.515), math.radians(338.507), math.radians(330.223), math.radians(320.730),
                        math.radians(310.103), math.radians(298.429), math.radians(285.801), math.radians(272.322),
                        math.radians(258.099), math.radians(243.247), math.radians(227.887), math.radians(212.140),
                        math.radians(196.135), math.radians(180.000), math.radians(163.865), math.radians(147.860),
                        math.radians(132.113), math.radians(116.753), math.radians(101.901), math.radians(87.678),
                        math.radians(74.199), math.radians(61.571), math.radians(49.897), math.radians(39.270),
                        math.radians(29.777), math.radians(21.493), math.radians(14.485), math.radians(8.810),
                        math.radians(4.513), math.radians(1.629), math.radians(0.181)
                    ])

                    self.thetaOd_S3 = np.array([
                        math.radians(+0.003993), math.radians(+0.034021), math.radians(+0.083827), math.radians(+0.131962),
                        math.radians(+0.140663), math.radians(+0.041205), math.radians(-0.293884), math.radians(-1.085149),
                        math.radians(-2.660230), math.radians(-5.400312), math.radians(-9.577984), math.radians(-15.107274),
                        math.radians(-21.334624), math.radians(-27.071709), math.radians(-30.990287), math.radians(-32.244143),
                        math.radians(-30.929663), math.radians(-28.016479), math.radians(-24.746722), math.radians(-21.928729),
                        math.radians(-19.631086), math.radians(-17.428312), math.radians(-14.905608), math.radians(-12.000662),
                        math.radians(-8.994751), math.radians(-6.275680), math.radians(-4.109544), math.radians(-2.559295),
                        math.radians(-1.535663), math.radians(-0.892650), math.radians(-0.497793), math.radians(-0.258079),
                        math.radians(-0.116227), math.radians(-0.038214), math.radians(-0.004045)
                    ])
                elif ((self.entries["Entrada 1"].get() == "111") & (self.entries["Saída 1"].get() == "") &
                (self.entries["Entrada 2"].get() == "") & (self.entries["Saída 2"].get() == "") &
                (self.entries["Entrada 3"].get() == "") & (self.entries["Saída 3"].get() == "") &
                (self.entries["Entrada 4"].get() == "") & (self.entries["Saída 4"].get() == "") &
                (self.entries["Entrada 5"].get() == "") & (self.entries["Saída 5"].get() == "")):

                # 20 pontos - valores inseridos de baixo para cima
                    self.thetaI_S3 = np.array([
                        math.radians(359.819), math.radians(358.371), math.radians(355.487), math.radians(351.190),
                        math.radians(345.515), math.radians(338.507), math.radians(330.223), math.radians(320.730),
                        math.radians(310.103), math.radians(298.429), math.radians(285.801), math.radians(272.322),
                        math.radians(258.099), math.radians(243.247), math.radians(227.887), math.radians(212.140),
                        math.radians(196.135), math.radians(180.000), math.radians(163.865), math.radians(147.860),
                        math.radians(132.113), math.radians(116.753), math.radians(101.901), math.radians(87.678),
                        math.radians(74.199), math.radians(61.571), math.radians(49.897), math.radians(39.270),
                        math.radians(29.777), math.radians(21.493), math.radians(14.485), math.radians(8.810),
                        math.radians(4.513), math.radians(1.629), math.radians(0.181)
                    ])

                    self.thetaOd_S3 = np.array([
                        math.radians(-0.168853), math.radians(-1.561672), math.radians(-4.551444), math.radians(-9.443883),
                        math.radians(-16.420666), math.radians(-25.207716), math.radians(-34.784249), math.radians(-43.433399),
                        math.radians(-49.375104), math.radians(-51.736403), math.radians(-51.044852), math.radians(-48.711871),
                        math.radians(-46.198882), math.radians(-44.839344), math.radians(-45.579920), math.radians(-47.496290),
                        math.radians(-47.160457), math.radians(-41.783847), math.radians(-33.080108), math.radians(-25.771960),
                        math.radians(-22.285283), math.radians(-21.074605), math.radians(-19.758097), math.radians(-17.444599),
                        math.radians(-13.986443), math.radians(-9.097044), math.radians(-2.967841), math.radians(+3.158495),
                        math.radians(+7.628694), math.radians(+9.462576), math.radians(+8.790395), math.radians(+6.522731),
                        math.radians(+3.773340), math.radians(+1.459815), math.radians(+0.167591)
                    ])
                else:
                    self.label4.configure(text="ERRO: Revise os dados preenchidos")
                    return
                
                if self.entries["Padrão: 50"].get() == "":
                    self.Delta_mi_S3 = 50

                else:
                    self.Delta_mi_S3 = float(self.entries["Padrão: 50"].get())
                
                self.lb_S3 = math.radians(90-self.Delta_mi_S3)
                self.rb_S3 = math.radians(90 + self.Delta_mi_S3)

                self.label4.configure(text="Calculando...")

                self.n_S3 = len(self.thetaI_S3)
                self.bounds_S3 = [[30, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[5, 100],[0, math.radians(360)], [math.radians(0), math.radians(360)],[math.radians(0), math.radians(360)]]
                start = time.time()
                self.result_S3 = scipy.optimize.differential_evolution(App.funcx_S3, self.bounds_S3, args=(self.thetaI_S3, self.thetaOd_S3, self.n_S3, self.lb_S3, self.rb_S3), tol=1e-2, atol=1e-4, maxiter = 2000, callback = self.callbackAtualizacao, workers = -1, updating='deferred', popsize = 15, strategy='randtobest1bin')
                end = time.time()

                self.label4.configure(text="Conferindo ordem e ângulos de transmissão")

                self.L1_S3 = self.result_S3.x[0]
                self.L2_S3 = self.result_S3.x[1]
                self.L3_S3 = self.result_S3.x[2]
                self.L4_S3 = self.result_S3.x[3]
                self.L5_S3 = self.result_S3.x[4]
                self.L6_S3 = self.result_S3.x[5]
                self.L8_S3 = self.result_S3.x[6]
                self.L9_S3 = self.result_S3.x[7]
                self.phi_S3 = self.result_S3.x[8]
                self.alpha1_S3 = self.result_S3.x[9]
                self.lambda1_S3 = self.result_S3.x[10]
                self.thetaO_S3 = []

                miok_S3 = 0
                mi11 =[]
                mi22=[]
                for i in range(self.n_S3):

                    AngE = self.thetaI_S3[i]
                    [A_S3, B_S3, C_S3, D_S3, E_S3, F_S3, G_S3, mi1_S3, mi2_S3, thetaO_S3] = self.Modelos_mecanismos('S3', AngE)
                    self.thetaO_S3.append(thetaO_S3)
                    mi11.append(math.degrees(mi1_S3))
                    mi22.append(math.degrees(mi2_S3))

                    if abs(np.rad2deg(self.thetaO_S3[i]) - math.degrees(self.thetaOd_S3[i])) > 5:
                        self.label4.configure(text="Erro")
                    else: 
                        if i == 0:
                            self.label7.configure(text="Ok")
                        elif i == 1:
                            self.label8.configure(text="Ok")
                        elif i == 2:
                            self.label9.configure(text="Ok")
                        elif i == 3:
                            self.label10.configure(text="Ok")
                        elif i == 4:   
                            self.label11.configure(text="Ok")

                    if (mi1_S3>self.lb_S3) and (mi1_S3<self.rb_S3) and (mi2_S3>self.lb_S3) and (mi2_S3<self.rb_S3):
                        miok_S3 = miok_S3 +1
                        
                if miok_S3 == self.n_S3:
                    self.label11x.configure(text="Ok")
                else:
                    self.label4.configure(text="Erro")

                THEI_S3 = [i for i in range(math.ceil(max(np.rad2deg(self.thetaI_S3))))]
                Ax_S3, Bx_S3, Cx_S3, Dx_S3, Ex_S3, Fx_S3, Gx_S3 = [],[],[],[],[],[],[]
                Ay_S3, By_S3, Cy_S3, Dy_S3, Ey_S3, Fy_S3, Gy_S3 = [],[],[],[],[],[],[]


                for i in range(len(THEI_S3)):
                    try:    
                        AngE = math.radians(THEI_S3[i])
                        [A_S3, B_S3, C_S3, D_S3, E_S3, F_S3, G_S3, mi1_S3, mi2_S3, thetaO_S3] = self.Modelos_mecanismos('S3', AngE)

                        Ax_S3.append(A_S3[0]);Bx_S3.append(B_S3[0]);Cx_S3.append(C_S3[0]);Dx_S3.append(D_S3[0]);Ex_S3.append(E_S3[0]);Fx_S3.append(F_S3[0]);Gx_S3.append(G_S3[0])
                        Ay_S3.append(A_S3[1]);By_S3.append(B_S3[1]);Cy_S3.append(C_S3[1]);Dy_S3.append(D_S3[1]);Ey_S3.append(E_S3[1]);Fy_S3.append(F_S3[1]);Gy_S3.append(G_S3[1])
                    except:
                        a=0

                val_junt_X_S3 = [Ax_S3, Bx_S3, Cx_S3, Dx_S3, Ex_S3, Fx_S3, Gx_S3]
                val_junt_Y_S3 = [Ay_S3, By_S3, Cy_S3, Dy_S3, Ey_S3, Fy_S3, Gy_S3]
                flattened_X_S3 = [item for sublist in val_junt_X_S3 for item in sublist]
                flattened_Y_S3 = [item for sublist in val_junt_Y_S3 for item in sublist]
                self.x_min_S3 = min(flattened_X_S3) - 5; self.y_min_S3 = min(flattened_Y_S3) - 5
                self.x_max_S3 = max(flattened_X_S3) + 5; self.y_max_S3 = max(flattened_Y_S3) + 5

                self.label4.configure(text="Finalizado")

                AngE = self.thetaI_S3[0]
                [A_S3, B_S3, C_S3, D_S3, E_S3, F_S3, G_S3, mi1_S3, mi2_S3, thetaO_S3] = self.Modelos_mecanismos('S3', AngE)

                marks_data = pd.DataFrame([{
                    'L1': round(self.L1_S3, 2),
                    'L2': round(self.L2_S3, 2),
                    'L3': round(self.L3_S3, 2),
                    'L4': round(self.L4_S3, 2),
                    'L5': round(self.L5_S3, 2),
                    'L6': round(self.L6_S3, 2),
                    'L8': round(self.L8_S3, 2),
                    'L9': round(self.L9_S3, 2),
                    'φ': round(math.degrees(self.phi_S3), 2),  # Phi symbol
                    'α': round(math.degrees(self.alpha1_S3), 2),  # Alpha symbol
                    'λ': round(math.degrees(self.lambda1_S3), 2),  # Lambda symbol
                    'μ1': np.round(mi11, 2).tolist(),  # Mu symbol
                    'μ2': np.round(mi22, 2).tolist(),  # Mu symbol
                    'θI': np.round(np.rad2deg(self.thetaI_S3), 2).tolist(),  # Theta symbol
                    'θOd': np.round(np.rad2deg(self.thetaOd_S3), 2).tolist(),  # Theta symbol
                    'θO': np.round(np.rad2deg(self.thetaO_S3), 2).tolist(),  # Theta symbol
                    'tempo': round(end - start, 2)
            }])

                file_name = 'MarksData_S3.xlsx'

                marks_data.to_excel(file_name)

                self.ax_S3.clear()
                self.ax_S3.plot([A_S3[0], B_S3[0]], [A_S3[1], B_S3[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S3.plot([A_S3[0], C_S3[0]], [A_S3[1], C_S3[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S3.plot([A_S3[0], D_S3[0]], [A_S3[1], D_S3[1]], '-og', markersize=4, alpha=0.5)
                self.ax_S3.plot([B_S3[0], C_S3[0]], [B_S3[1], C_S3[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S3.plot([C_S3[0], F_S3[0]], [C_S3[1], F_S3[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S3.plot([D_S3[0], F_S3[0]], [D_S3[1], F_S3[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S3.plot([D_S3[0], E_S3[0]], [D_S3[1], E_S3[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S3.plot([F_S3[0], E_S3[0]], [F_S3[1], E_S3[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S3.plot([G_S3[0], E_S3[0]], [G_S3[1], E_S3[1]], '-ok', markersize=4, alpha=0.5)
                self.ax_S3.plot([G_S3[0], B_S3[0]], [G_S3[1], B_S3[1]], '-or', markersize=4, alpha=0.5)

                points_S3 = {'A': A_S3, 'B': B_S3, 'C': C_S3, 'D': D_S3, 'E': E_S3, 'F': F_S3, 'G': G_S3}
                lines_S3 = [
                    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'F'), ('C', 'F'),
                    ('E', 'F'), ('D', 'E'), ('G', 'E'), ('G', 'B'), ('B', 'C')
                ]
                for letter, (x, y) in points_S3.items():
                    self.ax_S3.text(x, y, letter, fontsize=12, ha='right')

                if self.switches["Stephenson 3 Mostrar a numeração dos elos"].get() == 1:
                    for i, (start, end) in enumerate(lines_S3):
                            # Label each line
                        mid_x_S3 = (points_S3[start][0] + points_S3[end][0]) / 2
                        mid_y_S3= (points_S3[start][1] + points_S3[end][1]) / 2
                        self.ax_S3.text(mid_x_S3, mid_y_S3, f'L{i+1}', fontsize=12, ha='center', va='center')
                    

                self.ax_S3.fill([A_S3[0], B_S3[0], C_S3[0]], [A_S3[1], B_S3[1], C_S3[1]],color='orange', alpha=0.5)
                self.ax_S3.fill([D_S3[0], E_S3[0], F_S3[0]], [D_S3[1], E_S3[1], F_S3[1]], color='gray', alpha=0.5)
                self.ax_S3.set_title("Mecanismo Stephenson 3")
                self.ax_S3.set_xlabel("Eixo X")
                self.ax_S3.set_ylabel("Eixo Y")
                self.ax_S3.set_xlim(self.x_min_S3, self.x_max_S3)
                self.ax_S3.set_ylim(self.y_min_S3, self.y_max_S3)
                self.canvas_S3.draw()
                self.fig_S3.savefig('destination_path_S3.svg', format='svg')
                
                AngSaidaTex_S3 = ', '.join(str(x) for x in np.round(np.rad2deg(self.thetaO_S3), decimals = 3))
                self.label14_S3.configure(text=AngSaidaTex_S3)

                valoresotimizados_S3 = [round(self.L1_S3,3),round(self.L2_S3,3),round(self.L3_S3,3),round(self.L4_S3,3),round(self.L5_S3,3),round(self.L6_S3,3),round(self.L8_S3,3),round(self.L9_S3,3),round(math.degrees(self.phi_S3),3),round(math.degrees(self.alpha1_S3),3),round(math.degrees(self.lambda1_S3),3)]
                valoresotimizadosTex_S3 = ', '.join(str(x) for x in valoresotimizados_S3)
                self.label16_S3.configure(text=valoresotimizadosTex_S3)
            
            self.enable_interactives()
        except Exception as e:
            self.label4.configure(text="Erro: Tente novamente ou troque os valores")
            print(f"erro: {e}")
            self.enable_interactives()

    def callbackAtualizacao(self, xk, convergence):
        self.update()  # Atualização silenciosa, sem print

    def disable_interactives(self):
        # Disable all buttons
        for button in self.buttons.values():
            button.configure(state="disabled")

        # Disable all combo boxes
        self.combobox.configure(state="disabled")
        for combobox in self.combo_boxes.values():
            combobox.configure(state="disabled")

        # Disable all entries
        for entry in self.entries.values():
            entry.configure(state="disabled")

        # Disable all sliders
        for slider in self.sliders.values():
            slider.configure(state="disabled")

        # Disable all switches
        for switch in self.switches.values():
            switch.configure(state="disabled")

    def enable_interactives(self):
        # Enable all buttons
        for button in self.buttons.values():
            button.configure(state="normal")

        # Enable all combo boxes
        self.combobox.configure(state="normal")
        for combobox in self.combo_boxes.values():
            combobox.configure(state="normal")

        # Enable all entries
        for entry in self.entries.values():
            entry.configure(state="normal")

        # Enable all sliders
        for slider in self.sliders.values():
            slider.configure(state="normal")

        # Enable all switches
        for switch in self.switches.values():
            switch.configure(state="normal")

# Funções objetivo de otimização de cada mecanismo
    @staticmethod
    def funcx_W1(p_W1, thetaI_W1, thetaOd_W1, n_W1, lb_W1, rb_W1):
        """Função objetivo para otimização do mecanismo Watt 1.

        p_W1: vetor de parâmetros (elos e ângulos fixos)
        thetaI_W1: vetor de ângulos de entrada desejados (radianos)
        thetaOd_W1: vetor de ângulos de saída alvo (radianos)
        n_W1: número de pares
        lb_W1, rb_W1: limites (inferior/superior) de qualidade de transmissão

        Retorna a soma dos erros quadráticos entre thetaO calculado e
        thetaOd_W1. Penaliza configurações que violam restrições.
        """

        L1_W1, L2_W1, L3_W1, L4_W1, L5_W1, L6_W1, L8_W1, L9_W1, phi_W1, alpha_W1, lambda_W1 = p_W1
        # Inicialização de variável
        thetaO_W1 = []
        for i in range(n_W1):
            try:
                # Define as variáveis que serão modificadas até alcançar o objetivo da otimização
                
                # Cinemática do mecanismo
                B_W1 = [L1_W1*math.cos(phi_W1),L1_W1*math.sin(phi_W1)]
                C_W1 = [L2_W1*math.cos(thetaI_W1[i]),L2_W1*math.sin(thetaI_W1[i])]
                e1_W1 = math.sqrt((B_W1[0]-C_W1[0])**2 + (B_W1[1]-C_W1[1])**2)
                omega_W1 = math.atan2(B_W1[1]-C_W1[1], B_W1[0]-C_W1[0])
                delta_W1 = math.acos((L3_W1**2+e1_W1**2-L4_W1**2)/(2*e1_W1*L3_W1))
                D_W1 = [C_W1[0] + L3_W1*math.cos(delta_W1+omega_W1),C_W1[1] + L3_W1*math.sin(delta_W1+omega_W1)]
                E_W1 = [C_W1[0] + L5_W1*math.cos(delta_W1+omega_W1+alpha_W1),C_W1[1] + L5_W1*math.sin(delta_W1+omega_W1+alpha_W1)]

                beta1_W1 = math.atan2(D_W1[1]-B_W1[1], D_W1[0]-B_W1[0])
                thetaO = beta1_W1-lambda_W1
                
                G_W1  = [B_W1[0] + L6_W1*math.cos(thetaO),B_W1[1] + L6_W1*math.sin(thetaO)]
                e2_W1 = math.sqrt((E_W1[0]-G_W1[0])**2 + (E_W1[1]-G_W1[1])**2)
                
                L7_W1 = math.sqrt((D_W1[0]-E_W1[0])**2 + (D_W1[1]-E_W1[1])**2)
                # Cálculo dos ângulos de qualidade de transmissão

                mi1_W1 = math.acos((L4_W1**2+L3_W1**2-e1_W1**2)/(2*L4_W1*L3_W1))               
                mi2_W1 = math.acos((L8_W1**2+L9_W1**2-e2_W1**2)/(2*L8_W1*L9_W1))
                
                # Calcula a àrea dos dois elos ternários
                #AreaTri1_W1 = abs(L3_W1*math.sin(alpha_W1)*L5_W1)/(2)
                #AreaTri2_W1 = abs(L4_W1*math.sin(lambda_W1)*L6_W1)/(2)
                
                # Restrições da otimização. Caso os ângulos de qualidade de transmissão não estejam de acordo com o definido, ou se a 
                # àrea dos triângulos forem muito desproporcionais entre si, penaliza a função objetivo. Caso contrário, guarda em um vetor
                # o ângulo de saída calculado
                
                if (mi1_W1<lb_W1) or (mi1_W1>rb_W1) or (mi2_W1<lb_W1) or (mi2_W1>rb_W1):
                    thetaO_W1.append(999999999999)
                else:
                    thetaO_W1.append(thetaO)

            # Caso aconteça uma indeterminação matemática (Ex: divisão por zero no arco tangente), penaliza a função objetivo
            except:              
                thetaO_W1.append(999999999999)

        # Calcula a função objetivo como o erro ao quadrado de cada um dos ângulos de saída
        thetaO_W1 = np.array(thetaO_W1)
        thetaOd_W1 = np.array(thetaOd_W1)
        
        Fobj_W1 = np.sum((thetaO_W1-thetaOd_W1)**2)
        return Fobj_W1
    
        # Para os outros mecanismos desta função, o funcionamento segue o mesmo modelo deste.
    
    @staticmethod
    def funcx(p, thetaI, thetaOd, n, lb, rb):
        """Função objetivo genérica usada para Watt 2.

        Mesma ideia da função de Watt1: calcula thetaO para cada thetaI
        e retorna a soma dos erros quadráticos vs thetaOd. Aplica
        penalizações quando restrições não são atendidas.
        """

        # Use the stored values to perform a calculation
        thetaO = []
        for i in range(n):
            try:
                L1, L2, L3, L4, L5, L6, L8, L9, phi, alpha1, lambda1 = p

                B = [L1*math.cos(phi),L1*math.sin(phi)] 
                C = [L2*math.cos(phi+alpha1),L2*math.sin(phi+alpha1)]
                D = [L3*math.cos(thetaI[i]),L3*math.sin(thetaI[i])]
                x1 = math.sqrt((D[0]-C[0])**2 + (D[1]-C[1])**2)
                Beta1 = math.atan2(C[1]-D[1], C[0]-D[0])
                Beta2 = math.acos((L4**2+x1**2-L5**2)/(2*L4*x1))
                E = [D[0]+L4*math.cos(Beta1+Beta2),D[1]+L4*math.sin(Beta1+Beta2)]
                lambda0 = math.atan2(E[1]-C[1], E[0]-C[0])
                F = [C[0]+L6*math.cos(lambda0-lambda1),C[1]+L6*math.sin(lambda0-lambda1)]
                x2 = math.sqrt((F[0]-B[0])**2 + (F[1]-B[1])**2)
                psi = math.atan2(F[1]-B[1], F[0]-B[0])     
                omega2 = math.acos((x2**2+L9**2-L8**2)/(2*L9*x2))
                omega1 = psi-omega2-phi  
                mi1 = math.acos((L4**2+L5**2-x1**2)/(2*L4*L5))
                mi2 = math.acos((L8**2+L9**2-x2**2)/(2*L8*L9))

                AreaTri1 = abs(L1*math.sin(alpha1)*L2)/(2)
                AreaTri2 = abs(L5*math.sin(lambda1)*L6)/(2)

                if ((mi1<lb) or (mi1>rb) or (mi2<lb) or (mi2>rb)):
                    thetaO.append(999999999999)
                else:
                    thetaO.append(phi+omega1)

            except:                
                thetaO.append(999999999999)

        thetaO = np.array(thetaO)
        thetaOd = np.array(thetaOd)
        
        Fobj = np.sum((thetaO-thetaOd)**2)

        return Fobj

    @staticmethod
    def funcx_S1(p_S1, thetaI_S1, thetaOd_S1, n_S1, lb_S1, rb_S1):
        """Função objetivo para Stephenson 1.

        Implementa a cinemática e restrições específicas para S1 e
        retorna a soma dos erros quadrados entre thetaO_S1 e thetaOd_S1.
        """

        thetaO_S1 = []
        for i in range(n_S1):
            try:
                L1_S1, L2_S1, L3_S1, L4_S1, L5_S1, L6_S1, L8_S1, L9_S1, phi_S1, alpha1_S1, lambda1_S1 = p_S1

                B_S1 = [L1_S1*math.cos(phi_S1),L1_S1*math.sin(phi_S1)]
                C_S1 = [L2_S1*math.cos(thetaI_S1[i]+alpha1_S1),L2_S1*math.sin(thetaI_S1[i]+alpha1_S1)]
                D_S1 = [L3_S1*math.cos(thetaI_S1[i]),L3_S1*math.sin(thetaI_S1[i])]
                e1_S1 = math.sqrt((D_S1[0]-B_S1[0])**2 + (D_S1[1]-B_S1[1])**2)
                beta_S1 = math.atan2(B_S1[1]-D_S1[1], B_S1[0]-D_S1[0])
                omega_S1 = math.acos((e1_S1**2+L5_S1**2-L4_S1**2)/(2*e1_S1*L5_S1))
                E_S1 = [D_S1[0] + L5_S1*math.cos(beta_S1+omega_S1), D_S1[1] + L5_S1*math.sin(beta_S1+omega_S1)]
                ksi_S1 = math.atan2(E_S1[1]-B_S1[1], E_S1[0]-B_S1[0])
                thetaO = ksi_S1 - lambda1_S1
                F_S1 = [B_S1[0] + L6_S1*math.cos(ksi_S1-lambda1_S1), B_S1[1] + L6_S1*math.sin(ksi_S1-lambda1_S1)]
                e2_S1 = math.sqrt((C_S1[0]-F_S1[0])**2 + (C_S1[1]-F_S1[1])**2)

                mi1_S1 = math.acos((L5_S1**2+L4_S1**2-e1_S1**2)/(2*L5_S1*L4_S1))
                mi2_S1 = math.acos((L9_S1**2+L8_S1**2-e2_S1**2)/(2*L9_S1*L8_S1))

                AreaTri1_S1 = abs(L3_S1*math.sin(alpha1_S1)*L2_S1)/(2)
                AreaTri2_S1 = abs(L4_S1*math.sin(lambda1_S1)*L6_S1)/(2)
                
                if ((mi1_S1<lb_S1) or (mi1_S1>rb_S1) or (mi2_S1<lb_S1) or (mi2_S1>rb_S1)):
                    thetaO_S1.append(999999999999)
                else:
                    thetaO_S1.append(ksi_S1-lambda1_S1)
                
            except:              
                thetaO_S1.append(999999999999)

        thetaO_S1 = np.array(thetaO_S1)
        thetaOd_S1 = np.array(thetaOd_S1)
        
        Fobj_S1 = np.sum((thetaO_S1-thetaOd_S1)**2)
        return Fobj_S1

    @staticmethod
    def funcx_S2(p_S2, thetaI_S2, thetaOd_S2, n_S2, lb_S2, rb_S2):
        """Função objetivo para Stephenson 2.

        Observação: este caso resolve numericamente uma equação por ponto
        (usando `root`) para determinar um ângulo intermediário
        (`gamma_S2`) antes de calcular thetaO.
        """

        thetaO_S2 = []
        L1_S2, L2_S2, L3_S2, L4_S2, L5_S2, L6_S2, L8_S2, L9_S2, phi_S2, alpha1_S2, lambda1_S2 = p_S2

        B_S2 = [L1_S2*math.cos(phi_S2),L1_S2*math.sin(phi_S2)]
        initial_guess = 1

        for i in range(n_S2):

            try:
                
                C_S2 = [L3_S2*math.cos(thetaI_S2[i]+alpha1_S2),L3_S2*math.sin(thetaI_S2[i]+alpha1_S2)]
                D_S2 = [L2_S2*math.cos(thetaI_S2[i]),L2_S2*math.sin(thetaI_S2[i])]

                def equation_to_solve(gamma_S2):
                    # E_S2 as a function of gamma_S2
                    E_S2 = [C_S2[0] + L4_S2 * math.cos(gamma_S2.item()), C_S2[1] + L4_S2 * math.sin(gamma_S2.item())]
                    e1_S2 = math.sqrt((E_S2[0] - D_S2[0]) ** 2 + (E_S2[1] - D_S2[1]) ** 2)
                    omega_S2 = math.atan2(E_S2[1] - D_S2[1], E_S2[0] - D_S2[0])
                    omega2_S2 = math.acos((e1_S2 ** 2 + L5_S2 ** 2 - L6_S2 ** 2) / (2 * e1_S2 * L5_S2))
                    F_S2 = [D_S2[0] + L5_S2 * math.cos(omega_S2 - omega2_S2), D_S2[1] + L5_S2 * math.sin(omega_S2 - omega2_S2)]
                    omega3_S2 = math.atan2(E_S2[1] - F_S2[1], E_S2[0] - F_S2[0])
                    G_S2 = [F_S2[0] + L8_S2 * math.cos(omega3_S2 - lambda1_S2), F_S2[1] + L8_S2 * math.sin(omega3_S2 - lambda1_S2)]

                    # The equation to solve
                    return L9_S2 - math.sqrt((G_S2[0] - B_S2[0]) ** 2 + (G_S2[1] - B_S2[1]) ** 2)

                result = root(equation_to_solve, initial_guess, method='lm')
                solution_gamma_S2 = result.x[0]

                if solution_gamma_S2 < 0 or solution_gamma_S2 > 2 * math.pi:
                    solution_gamma_S2 = (solution_gamma_S2 % (2 * math.pi))

                E_S2 = [C_S2[0] + L4_S2*math.cos(solution_gamma_S2), C_S2[1] + L4_S2*math.sin(solution_gamma_S2)]
                e1_S2 = math.sqrt((E_S2[0]-D_S2[0])**2 + (E_S2[1]-D_S2[1])**2)
                omega_S2 = math.atan2(E_S2[1]-D_S2[1], E_S2[0]-D_S2[0])
                omega2_S2 = math.acos((e1_S2**2 + L5_S2**2 - L6_S2**2) / (2 * e1_S2 * L5_S2))
                F_S2 = [D_S2[0] + L5_S2*math.cos(omega_S2-omega2_S2), D_S2[1] + L5_S2*math.sin(omega_S2-omega2_S2)]
                omega3_S2 = math.atan2(E_S2[1]-F_S2[1], E_S2[0]-F_S2[0])
                G_S2 = [F_S2[0] + L8_S2*math.cos(omega3_S2-lambda1_S2), F_S2[1] + L8_S2*math.sin(omega3_S2-lambda1_S2)]

                thetaO_S2compl = math.atan2(G_S2[1]-B_S2[1], G_S2[0]-B_S2[0])

                e2_S2 = math.sqrt((F_S2[0]-B_S2[0])**2 + (F_S2[1]-B_S2[1])**2)
                
                e3_S2 = math.sqrt((F_S2[0]-C_S2[0])**2 + (F_S2[1]-C_S2[1])**2)

                mi1_S2 = math.acos((L4_S2**2 + L6_S2**2 - e3_S2**2) / (2 * L4_S2 * L6_S2))
                mi2_S2 = math.acos((L8_S2**2+L9_S2**2-e2_S2**2)/(2*L8_S2*L9_S2))

                AreaTri1_S2 = abs(L2_S2*math.sin(alpha1_S2)*L3_S2)/(2)
                AreaTri2_S2 = abs(L6_S2*math.sin(lambda1_S2)*L8_S2)/(2)

                if ((mi1_S2<lb_S2) or (mi1_S2>rb_S2) or (mi2_S2<lb_S2) or (mi2_S2>rb_S2)):
                    thetaO_S2.append(999999999999)
                else:
                    thetaO_S2.append(thetaO_S2compl)  

            except:            
                thetaO_S2.append(999999999999)
        
        thetaO_S2 = np.array(thetaO_S2)
        thetaOd_S2 = np.array(thetaOd_S2)
        
        Fobj_S2 = np.sum((thetaO_S2-thetaOd_S2)**2)
        return Fobj_S2

    @staticmethod
    def funcx_S3(p_S3, thetaI_S3, thetaOd_S3, n_S3, lb_S3, rb_S3):
        """Função objetivo para Stephenson 3.

        Implementa a cinemática de S3 e aplica as mesmas penalizações
        por violação de restrições ou inconsistências geométricas.
        """

        thetaO_S3 = []
        L1_S3, L2_S3, L3_S3, L4_S3, L5_S3, L6_S3, L8_S3, L9_S3, phi_S3, alpha1_S3, lambda1_S3 = p_S3

        A_S3 = [0,0]
        B_S3 = [L1_S3*math.cos(phi_S3),L1_S3*math.sin(phi_S3)]
        C_S3 = [L2_S3*math.cos(phi_S3+alpha1_S3),L2_S3*math.sin(phi_S3+alpha1_S3)]

        for i in range(n_S3):

            try:
                
                D_S3 = [L3_S3*math.cos(thetaI_S3[i]),L3_S3*math.sin(thetaI_S3[i])]
                e1_S3 = math.sqrt((D_S3[0]-C_S3[0])**2 + (D_S3[1]-C_S3[1])**2)
                omega_S3 = math.acos((e1_S3**2+L5_S3**2-L4_S3**2)/(2*e1_S3*L5_S3))
                beta_S3 = math.atan2(D_S3[1]-C_S3[1], D_S3[0]-C_S3[0])
                F_S3 = [C_S3[0] + L5_S3*math.cos(beta_S3-omega_S3), C_S3[1] + L5_S3*math.sin(beta_S3-omega_S3)]
                lambda0_S3 = math.atan2(D_S3[1]-F_S3[1], D_S3[0]-F_S3[0])
                E_S3 = [F_S3[0] + L6_S3*math.cos(lambda0_S3-lambda1_S3), F_S3[1] + L6_S3*math.sin(lambda0_S3-lambda1_S3)]
                e2_S3 = math.sqrt((E_S3[0]-B_S3[0])**2 + (E_S3[1]-B_S3[1])**2)
                gamma_S3 = math.acos((e2_S3**2+L9_S3**2-L8_S3**2)/(2*e2_S3*L9_S3))
                gamma1_S3 = math.atan2(E_S3[1]-B_S3[1], E_S3[0]-B_S3[0])
                thetaO_S3compl = gamma1_S3-gamma_S3

                mi1_S3 = math.acos((L5_S3**2+L4_S3**2-e1_S3**2)/(2*L5_S3*L4_S3))
                mi2_S3 = math.acos((L8_S3**2+L9_S3**2-e2_S3**2)/(2*L8_S3*L9_S3))

                AreaTri1_S3 = abs(L2_S3*math.sin(alpha1_S3)*L1_S3)/(2)
                AreaTri2_S3 = abs(L4_S3*math.sin(lambda1_S3)*L6_S3)/(2)
                
                if ((mi1_S3<lb_S3) or (mi1_S3>rb_S3) or (mi2_S3<lb_S3) or (mi2_S3>rb_S3)):
                    thetaO_S3.append(999999999999)
                else:
                    thetaO_S3.append(gamma1_S3-gamma_S3)  

            except:            
                thetaO_S3.append(999999999999)
        
        thetaO_S3 = np.array(thetaO_S3)
        thetaOd_S3 = np.array(thetaOd_S3)
        
        Fobj_S3 = np.sum((thetaO_S3-thetaOd_S3)**2)
        return Fobj_S3
       

if __name__ == "__main__":
    app = App()
    app.mainloop()
