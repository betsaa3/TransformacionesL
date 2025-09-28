import numpy as np
import matplotlib.pyplot as plt
import math

def rotacion(puntos, angulo):
    rad = math.radians(angulo)
    R = np.array([[math.cos(rad), -math.sin(rad)],
                [math.sin(rad), math.cos(rad)]])
    return puntos @ R.T

def reflexion(puntos, eje):
    if eje =='x':
        R = np.array([[1, 0],
                     [0, -1]])
    elif eje == 'y':
        R = np.array([[-1, 0],
                     [0, 1]])
    else:
        R = np.array([[0, 1],
                     [1, 0]])
    return puntos @ R.T

def homotecia(puntos, kx, ky):
    S = np.array([[kx, 0],
                  [0, ky]])
    return puntos @ S.T

def menu_transformaciones(puntos):
    print("\n\t" + "="*60)
    print("\t\t\t✨ MENU DE TRANSFORMACIONES ✨")
    print("\t" + "="*60)

    opciones = {
        1: "Rotacion",
        2: "Reflexion",
        3: "Homotecia",
        4: "Salir"
    }

    for num, texto in opciones.items():
        print(f"\t  [{num}] {texto}")
    print("\t" + "="*60)

    while True:
        try:
            op = int(input("\tOpción: "))
            if op in opciones:
                break
            else:
                print("\t !! Ingresa un numero valido (1-6).")
        except ValueError:
            print("\t !!! Debes ingresar un numero entero.")
    if op == 1:
        while True:
            try:
                angulo = float(input("\tIngrese angulo de rotacion (grados): "))
                break
            except ValueError:
                print("\t !!! Ingresa un valor numerico.")
        return rotacion(puntos, angulo)
    elif op == 2:
        while True:
            eje = input("\tIngrese eje (x, y, d para diagonal y=x): ").strip().lower()
            if eje in ['x','y','d']:
                break
            print("\t !! Solo se permite x, y o d.")
        return reflexion(puntos, eje)
    elif op == 3:
        while True:
            try:
                kx = float(input("\tFactor en X: "))
                ky = float(input("\tFactor en Y: "))
                if kx == 0 or ky == 0:
                    print("\t !! Los factores no pueden ser cero.")
                    continue
                break
            except ValueError:
                print("\t !!! Ingresa valores numericos validos.")
        return homotecia(puntos, kx, ky)
    else:
        print("\n\t🔹 Saliendo del menu...")
        return None

def graficar(original, transformada):
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('#f5f5fa')
    ax.set_facecolor('#eaf6ff')
    ax.axis('equal')
    # Original con sombra y marcadores grandes
    ax.plot(original[:,0], original[:,1], color='#0077b6', marker='o', markersize=8, linewidth=2.5, alpha=0.85, label="Original", zorder=2)
    # Etiquetas de puntos originales
    for (x, y) in original:
        ax.text(x, y, f'({x:.1f},{y:.1f})', fontsize=10, color='#0077b6', ha='right', va='bottom', zorder=3)
    # Transformada con otro estilo
    ax.plot(transformada[:,0], transformada[:,1], color='#d90429', marker='s', markersize=8, linewidth=2.5, alpha=0.85, label="Transformada", zorder=2)
    for (x, y) in transformada:
        ax.text(x, y, f'({x:.1f},{y:.1f})', fontsize=10, color='#d90429', ha='left', va='top', zorder=3)
    # Ejes
    ax.axhline(0, color='#22223b', linewidth=1.2, linestyle='--', alpha=0.7, zorder=1)
    ax.axvline(0, color='#22223b', linewidth=1.2, linestyle='--', alpha=0.7, zorder=1)
    # Leyenda y título
    legend = ax.legend(fontsize=13, loc='upper right', frameon=True, facecolor='#f5f5fa', edgecolor='#22223b')
    ax.set_title("✨ Transformaciones Lineales ✨", fontsize=18, color='#22223b', pad=20)
    ax.grid(True, color='#b5b5b5', linestyle=':', linewidth=1, alpha=0.5)
    plt.tight_layout()
    plt.show()

def main():
    print("\n\t" + "="*60)
    print("\t\t✨ BIENVENIDO A TRANSFORMACIONES LINEALES ✨")
    print("\t" + "="*60)

    while True:
        try:
            n = int(input("\n\t¿Cuántos puntos tiene la figura?: "))
            if n < 2:
                print("\t !! Debe haber al menos 2 puntos minimo.")
                continue
            break
        except ValueError:
            print("\t !!! Ingresa un número entero válido.")
    puntos = []

    for i in range(n):
        while True:
            try:
                x = float(input(f"\tIngrese x{i+1}: "))
                y = float(input(f"\tIngrese y{i+1}: "))
                puntos.append([x, y])
                break
            except ValueError:
                print("\t !!! Ingresa valores numéricos válidos.")

    puntos.append(puntos[0])
    puntos = np.array(puntos)

    while True:
        puntos_transf = menu_transformaciones(puntos)
        if puntos_transf is None:
            break

        graficar(puntos, puntos_transf)

        puntos = puntos_transf
        
        while True:
            seguir = input("\n¿Quieres aplicar otra transformacion? (s/n): ").strip().lower()
            if seguir in ['s', 'n']:
                break
            else:
                print("\t !! Responde con 's' para si o 'n' para no.")

if __name__ == "__main__":
    main()