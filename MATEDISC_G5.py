import tkinter as tk
from tkinter import font as tkFont, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# ==============================================================================
# 🧭 1. FUNCIONES MATEMÁTICAS DE TRANSFORMACIÓN
# ==============================================================================

# (Las funciones matemáticas de rotacion, reflexion y homotecia permanecen iguales)

def rotacion(puntos, angulo, origen):
    rad = math.radians(angulo)
    R = np.array([[math.cos(rad), -math.sin(rad)],
                  [math.sin(rad),  math.cos(rad)]])
    
    puntos_centrados = puntos - origen
    transformados = (R @ puntos_centrados.T).T
    return transformados + origen

def reflexion(puntos, eje=None, m=None, origen=np.array([0, 0])):
    origen = np.array(origen, dtype=float)
    puntos_trasladados = puntos - origen
    if eje == 'x': R = np.array([[1, 0], [0, -1]])
    elif eje == 'y': R = np.array([[-1, 0], [0, 1]])
    elif eje == 'y=x': R = np.array([[0, 1], [1, 0]])
    elif eje == 'y=-x': R = np.array([[0, -1], [-1, 0]])
    elif m is not None:
        theta = np.arctan(m)
        R = np.array([[np.cos(2*theta), np.sin(2*theta)],
                      [np.sin(2*theta), -np.cos(2*theta)]])
    else: raise ValueError("Eje o pendiente no válida para la reflexión.")
    reflejados = (R @ puntos_trasladados.T).T
    return reflejados + origen

def homotecia(puntos, kx, ky, origen):
    S = np.array([[kx, 0], [0, ky]])
    puntos_centrados = puntos - origen
    transformados = (S @ puntos_centrados.T).T
    return transformados + origen


# ==============================================================================
# 🎨 2. CLASE DE LA INTERFAZ GRÁFICA (GUI) CON TKINTER
# ==============================================================================

# --- Paleta de Colores COTTON CANDY (Algodón de Azúcar) ---
BG_COLOR = "#292138"         # Fondo Principal (Púrpura muy oscuro)
PANEL_COLOR = "#3A314D"      # Paneles y Cajas (Púrpura más claro, "elevado")
PRIMARY_COLOR = "#FF69B4"    # Botón Principal / Transformada (Rosa Caliente Brillante)
SECONDARY_COLOR = "#8A2BE2"  # Botón Secundario / Original (Azul Violeta Profundo)
ACCENT_COLOR = "#FFD700"     # Origen / Énfasis (Dorado/Amarillo Brillante)
TEXT_COLOR = "#F0F0F0"       # Texto para el modo oscuro (Blanco muy suave)

FONT_STYLE = 'Century Gothic' 
TITLE_FONT_STYLE = 'Century Gothic'

class SetupWindow:
    """Ventana inicial para ingresar los vértices de la figura y el origen."""
    def __init__(self, master):
        self.master = master
        self.master.title("Configuración Inicial")
        self.master.geometry("500x550")
        self.master.configure(bg=BG_COLOR)
        
        self.title_font = tkFont.Font(family=TITLE_FONT_STYLE, size=16, weight="bold")
        self.pixel_font = tkFont.Font(family=FONT_STYLE, size=11)

        # Panel principal con borde suave
        main_frame = tk.Frame(self.master, bg=PANEL_COLOR, bd=0, relief="flat", padx=20, pady=20)
        main_frame.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)

        # Campos de entrada con acento de color
        self.points_text = tk.Text(main_frame, height=10, width=40, bg=BG_COLOR, fg=TEXT_COLOR, 
                                   font=self.pixel_font, relief="flat", bd=1, highlightbackground=PRIMARY_COLOR, highlightthickness=1, insertbackground=TEXT_COLOR)
        self.origin_entry = tk.Entry(main_frame, bg=BG_COLOR, fg=TEXT_COLOR, 
                                     font=self.pixel_font, width=15, relief="flat", bd=1, highlightbackground=PRIMARY_COLOR, highlightthickness=1, insertbackground=TEXT_COLOR)
        
        self.points_text.insert(tk.END, "1,1\n4,1\n4,4\n1,4") 
        self.origin_entry.insert(0, "3,3")
        
        self._setup_layout(main_frame)

    def _setup_layout(self, frame):
        tk.Label(frame, text="CONFIGURACIÓN INICIAL", bg=PANEL_COLOR, fg=PRIMARY_COLOR, 
                 font=self.title_font).pack(pady=10)
        
        tk.Label(frame, text="Vértices (x,y) - Uno por línea. NO repitas el 1ro:", 
                 bg=PANEL_COLOR, fg=TEXT_COLOR, font=self.pixel_font).pack()
        self.points_text.pack(pady=5)
        
        tk.Label(frame, text="Origen de Transformación (x,y):", 
                 bg=PANEL_COLOR, fg=TEXT_COLOR, font=self.pixel_font).pack(pady=5)
        self.origin_entry.pack(pady=5)
        
        # Botones planos y brillantes
        tk.Button(frame, text="INICIAR TRANSFORMACIONES", command=self.start_app, 
                  bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=self.pixel_font, width=30, 
                  pady=10, bd=0, relief="flat", activebackground=SECONDARY_COLOR).pack(pady=20)
        
        tk.Button(frame, text="SALIR", command=self.master.quit, 
                  bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=self.pixel_font, 
                  width=15, pady=5, bd=0, relief="flat", activebackground=PRIMARY_COLOR).pack(pady=5)

    def start_app(self):
        # (La lógica de validación y transición es la misma)
        try:
            points_str = self.points_text.get("1.0", tk.END).strip().split('\n')
            puntos_list = [list(map(float, line.split(','))) for line in points_str if line]
            puntos_array = np.array(puntos_list, dtype=float)
            
            if len(puntos_array) < 2: raise ValueError("Se necesitan al menos dos puntos.")
            if not np.array_equal(puntos_array[0], puntos_array[-1]):
                 puntos_array = np.append(puntos_array, [puntos_array[0]], axis=0)

            origin_str = self.origin_entry.get().strip()
            origen_array = np.array(list(map(float, origin_str.split(','))), dtype=float)
            
            self.master.destroy()
            root = tk.Tk()
            TransformacionesGUI(root, puntos_array, origen_array)
            root.mainloop()
        except Exception as e:
            messagebox.showerror("Error de Entrada", f"Formato inválido. Asegúrate de usar 'x,y'.\nDetalle: {e}")


class TransformacionesGUI:
    """Ventana principal con el menú Cotton Candy y el área de la gráfica."""
    def __init__(self, master, puntos_originales, origen_inicial):
        self.master = master
        self.puntos_originales = puntos_originales.copy()
        self.puntos_actuales = puntos_originales.copy()
        self.origen = origen_inicial
        
        master.title("Transformaciones Lineales Cotton Candy")
        master.geometry("1100x750")
        master.configure(bg=BG_COLOR)
        
        self.transform_var = tk.StringVar(value="Rotación")
        self.param1_str = tk.StringVar(value="90")
        self.param2_str = tk.StringVar(value="1.5")
        self.reflection_axis_var = tk.StringVar(value="y=mx")

        self.pixel_font = tkFont.Font(family=FONT_STYLE, size=11)
        self.title_font = tkFont.Font(family=TITLE_FONT_STYLE, size=16, weight="bold")
        
        self._setup_menu_panel()
        self._setup_plot_panel()
        self.update_plot(self.puntos_actuales, self.puntos_actuales, self.origen)

    def _setup_menu_panel(self):
        menu_frame = tk.Frame(self.master, bg=PANEL_COLOR, padx=20, pady=20, width=350)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        menu_frame.pack_propagate(False)

        tk.Label(menu_frame, text="TRANSFORMACIONES", bg=PANEL_COLOR, fg=PRIMARY_COLOR, 
                 font=self.title_font).pack(pady=10)
        
        def create_soft_panel(parent, text):
            # Usamos el color de fondo más oscuro para el LabelFrame
            lf = tk.LabelFrame(parent, text=text, bg=PANEL_COLOR, fg=TEXT_COLOR, font=self.pixel_font, 
                               padx=15, pady=15, bd=0, relief="flat")
            lf.pack(fill=tk.X, pady=10)
            return lf

        option_frame = create_soft_panel(menu_frame, " 1. TIPO DE OPERACIÓN ")
        options = ["Rotación", "Reflexión", "Homotecia"]
        for op in options:
            rb = tk.Radiobutton(option_frame, text=op, variable=self.transform_var, value=op,
                                command=self._update_parameters_panel, bg=PANEL_COLOR, fg=TEXT_COLOR, 
                                selectcolor=BG_COLOR, font=self.pixel_font, indicatoron=0,
                                relief="flat", bd=2, width=20, pady=5,
                                activebackground=PRIMARY_COLOR, activeforeground=TEXT_COLOR)
            rb.pack(anchor="center", pady=3)

        self.param_frame = create_soft_panel(menu_frame, " 2. PARÁMETROS ")
        self._update_parameters_panel()

        # Botones de acción
        tk.Button(menu_frame, text="APLICAR TRANSFORMACIÓN", command=self._apply_transformation, 
                  bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=self.pixel_font, width=25, pady=10, bd=0, relief="flat", activebackground=SECONDARY_COLOR).pack(pady=20)
        
        tk.Button(menu_frame, text="REINICIAR FIGURA", command=self._reset_figure, 
                  bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=self.pixel_font, width=25, pady=5, bd=0, relief="flat", activebackground=PRIMARY_COLOR).pack(pady=5)
        
        tk.Button(menu_frame, text="SALIR", command=self.master.quit, 
                  bg=BG_COLOR, fg=TEXT_COLOR, font=self.pixel_font, width=25, pady=5, bd=0, relief="flat").pack(side=tk.BOTTOM, pady=20)
        
    def _update_parameters_panel(self):
        for widget in self.param_frame.winfo_children(): widget.destroy()
        opcion = self.transform_var.get()
        entry_kwargs = dict(bg=BG_COLOR, fg=TEXT_COLOR, font=self.pixel_font, width=15, relief="flat", bd=1, highlightbackground=PRIMARY_COLOR, highlightthickness=1, insertbackground=TEXT_COLOR)

        if opcion == "Rotación":
            tk.Label(self.param_frame, text="Ángulo (°):", bg=PANEL_COLOR, fg=TEXT_COLOR, font=self.pixel_font).pack(pady=5)
            tk.Entry(self.param_frame, textvariable=self.param1_str, **entry_kwargs).pack(pady=5)
        elif opcion == "Reflexión":
            axes = {"Eje X": "x", "Eje Y": "y", "Recta y=x": "y=x", "Recta y=mx": "y=mx"}
            for text, val in axes.items():
                rb = tk.Radiobutton(self.param_frame, text=text, variable=self.reflection_axis_var, value=val,
                                    command=self._toggle_m_entry, bg=PANEL_COLOR, fg=TEXT_COLOR, 
                                    selectcolor=SECONDARY_COLOR, font=self.pixel_font)
                rb.pack(anchor="w")
            self.m_label = tk.Label(self.param_frame, text="Valor de m:", bg=PANEL_COLOR, fg=TEXT_COLOR, font=self.pixel_font)
            self.m_entry = tk.Entry(self.param_frame, textvariable=self.param1_str, **entry_kwargs)
            self._toggle_m_entry()
        elif opcion == "Homotecia":
            tk.Label(self.param_frame, text="Factor X (Kx):", bg=PANEL_COLOR, fg=TEXT_COLOR, font=self.pixel_font).pack(pady=5)
            tk.Entry(self.param_frame, textvariable=self.param1_str, **entry_kwargs).pack(pady=5)
            tk.Label(self.param_frame, text="Factor Y (Ky):", bg=PANEL_COLOR, fg=TEXT_COLOR, font=self.pixel_font).pack(pady=5)
            tk.Entry(self.param_frame, textvariable=self.param2_str, **entry_kwargs).pack(pady=5)
    
    def _toggle_m_entry(self):
        if self.reflection_axis_var.get() == "y=mx": self.m_label.pack(pady=5); self.m_entry.pack(pady=5)
        else: self.m_label.pack_forget(); self.m_entry.pack_forget()

    def _apply_transformation(self):
        try:
            opcion, puntos_transf = self.transform_var.get(), None
            if opcion == "Rotación": puntos_transf = rotacion(self.puntos_actuales, float(self.param1_str.get()), self.origen)
            elif opcion == "Reflexión":
                axis = self.reflection_axis_var.get()
                puntos_transf = reflexion(self.puntos_actuales, m=float(self.param1_str.get()), origen=self.origen) if axis == "y=mx" else reflexion(self.puntos_actuales, eje=axis, origen=self.origen)
            elif opcion == "Homotecia": puntos_transf = homotecia(self.puntos_actuales, float(self.param1_str.get()), float(self.param2_str.get()), self.origen)
            
            if puntos_transf is not None: self.update_plot(self.puntos_actuales, puntos_transf, self.origen); self.puntos_actuales = puntos_transf
        except Exception as e: messagebox.showerror("Error", f"Error en los parámetros: {e}")
    
    def _reset_figure(self):
        self.puntos_actuales = self.puntos_originales.copy()
        self.update_plot(self.puntos_originales, self.puntos_actuales, self.origen)

    def _setup_plot_panel(self):
        plot_frame = tk.Frame(self.master, bg=BG_COLOR)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Estilos de la Gráfica
        self.ax.figure.patch.set_facecolor(PANEL_COLOR) # Fondo del contenedor grande
        self.ax.set_facecolor(BG_COLOR) # Fondo del área de trazado
        for spine in ['top', 'right', 'bottom', 'left']: self.ax.spines[spine].set_color(TEXT_COLOR)
        self.ax.tick_params(axis='x', colors=TEXT_COLOR); self.ax.tick_params(axis='y', colors=TEXT_COLOR)
        
    def update_plot(self, original, transformada, origen):
        self.ax.clear()
        
        # Original (Azul Violeta Profundo)
        self.ax.plot(original[:,0], original[:,1], color=SECONDARY_COLOR, marker='o', markersize=6, linewidth=2, label="Original")
        for x, y in original[:-1]: self.ax.text(x, y, f'({x:.1f},{y:.1f})', fontsize=9, color=SECONDARY_COLOR, ha='right', va='bottom', fontname=FONT_STYLE)
        
        # Transformada (Rosa Caliente Brillante)
        self.ax.plot(transformada[:,0], transformada[:,1], color=PRIMARY_COLOR, marker='s', markersize=6, linewidth=2, label="Transformada")
        for x, y in transformada[:-1]: self.ax.text(x, y, f'({x:.1f},{y:.1f})', fontsize=9, color=PRIMARY_COLOR, ha='left', va='top', fontname=FONT_STYLE)
        
        # Origen (Amarillo Brillante)
        self.ax.scatter(origen[0], origen[1], color=ACCENT_COLOR, s=100, edgecolor=TEXT_COLOR, label='Origen', zorder=5)
        self.ax.axhline(0, color=TEXT_COLOR, linewidth=1, linestyle='--', alpha=0.3)
        self.ax.axvline(0, color=TEXT_COLOR, linewidth=1, linestyle='--', alpha=0.3)
        
        self.ax.set_title("Resultados de la Transformación", color=TEXT_COLOR, fontname=TITLE_FONT_STYLE)
        self.ax.legend(loc='upper right', prop={'family': FONT_STYLE}, facecolor=PANEL_COLOR, edgecolor=TEXT_COLOR, labelcolor=TEXT_COLOR)
        self.ax.axis('equal'); self.ax.grid(True, color=TEXT_COLOR, linestyle=':', linewidth=0.5, alpha=0.2)
        self.canvas.draw()


# ==============================================================================
# 🚀 3. BLOQUE DE EJECUCIÓN PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    SetupWindow(root)
    root.mainloop()