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
        1: "Ingresar figura ➕",
        2: "Traslacion ↔",
        3: "Homotecia 🔍",
        4: "Rotacion 🔄",
        5: "Reflexion 🪞",
        6: "Salir 🚪"
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
            eje = input("\tIngrese eje (x, y, d para diagonal y=x): ")
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
    elif op == 4:
        while True:
            try:
                angulo = float(input("\tIngrese angulo de rotacion (grados): "))
                break
            except ValueError:
                print("\t !!! Ingresa un valor numerico.")
        return rotacion(puntos, angulo)
    elif op == 5:
        while True:
            eje = input("\tIngrese eje (x, y, d para diagonal y=x): ")
            if eje in ['x','y','d']:
                break
            print("\t !! Solo se permite x, y o d.")
        return reflexion(puntos, eje)
    else:
        print("\n🔹 Saliendo del menu...")
        return None

def graficar(original, transformada):
    plt.figure(figsize=(6, 6))
    plt.axis('equal')
    plt.plot(original[:,0], original[:,1], 'bo-', label="Original")
    plt.plot(transformada[:,0], transformada[:,1], 'ro-', label="Transformada")
    plt.axhline(0, color='gray', linewidth=0.5)
    plt.axvline(0, color='gray', linewidth=0.5)
    plt.legend()
    plt.title("Transformaciones Lineales")
    plt.grid(True)
    plt.show()

def main():
    print("\n\t" + "="*60)
    print("\t\t✨ BIENVENIDO A TRANSFORMACIONES LINEALES ✨")
    print("\t" + "="*60)

    while True:
        try:
            n = int(input("\n\t¿Cuántos puntos tiene la figura?: "))
            if n < 1:
                print("\t !! Debe haber al menos 1 punto.")
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
        
        seguir = input("\n¿Quieres aplicar otra transformación? (s/n): ")
        if seguir.lower() != 's':
            break

if __name__ == "__main__":
    main()