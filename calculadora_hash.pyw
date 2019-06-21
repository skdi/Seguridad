import math
from tkinter import *
from operator import xor

cant_rotaciones = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
 
constants = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
#vector ABCD
Valores_ABCD = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
 
functions = 16*[lambda b, c, d: (b & c) | (~b & d)] + \
            16*[lambda b, c, d: (d & b) | (~d & c)] + \
            16*[lambda b, c, d: b ^ c ^ d] + \
            16*[lambda b, c, d: c ^ (b | ~d)]

def md5(mensaje):
    #convertimos el mensaje a un array de bytes
    mensaje = bytearray(mensaje) #copy our input into a mutable buffer
    #tamaño del mensaje
    orig_len_in_bits = (8 * len(mensaje)) & 0xffffffffffffffff

    mensaje.append(0x80)
    #padding
    while len(mensaje)%64 != 56:
        mensaje.append(0)
    mensaje += orig_len_in_bits.to_bytes(8, byteorder='little')
    
    #array ABCD
    hash_pieces = Valores_ABCD[:]
    #print(len(mensaje))
    for bloque_ofst in range(0, len(mensaje), 64):
        a, b, c, d = hash_pieces
        n_bloques = mensaje[bloque_ofst:bloque_ofst+64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(n_bloques[4*g:4*g+4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, cant_rotaciones[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF
 
    return sum(x<<(32*i) for i, x in enumerate(hash_pieces))
 
def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))
index_functions = 16*[lambda i: i] + \
                  16*[lambda i: (5*i + 1)%16] + \
                  16*[lambda i: (3*i + 5)%16] + \
                  16*[lambda i: (7*i)%16]
 

def leftRotate(n_bloques, long_rotacion):
    return ((n_bloques << long_rotacion) | (n_bloques >> (32 - long_rotacion))) &  0xffffffff 
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF
def md5_(mensaje):
    #inicializacion de los buffers 5x32bits = 160
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    
    long_mensaje = ""
    copy = ""
    #preprocesamiento - conversion a bits
    for char in range(len(mensaje)):
        long_mensaje += '{0:08b}'.format(ord(mensaje[char]))

    #Little endian
    for inv in range(len(long_mensaje)):
        copy += long_mensaje[len(long_mensaje)-inv-1]

    #print(long_mensaje)
    temp = copy   
    long_mensaje += '1'
    
    #padding - rellenado    
    while(len(long_mensaje) % 512 != 448):
        long_mensaje += '0'

    #agregando longitud del mensaje al mensaje
    long_mensaje += '{0:064b}'.format(len(temp))
    #Creando los sub bloques a partir del mensaje en tam = 512 bits
    n_bloques = bloques(long_mensaje, 512)
    hash_pieces = [A,B,C,D]
    #Inicio del tratamiento 
    for sub_bloque in n_bloques:
        #separamos los subbloques en bloques de 32 bits
        words = bloques(sub_bloque, 32)
        w = [0] * 80
        for n in range(0, 16):
            w[n] = int(words[n], 2)
        #Initialize hash value for this n_bloques:
        a = A
        b = B
        c = C
        d = D

        #Bucle principal 80 vueltas:
        for i in range(0, 64):
            if 0 <= i <= 15:
                f = (b & c) | ((~b) & d)
                g = i
                k = 0x5A827999

            elif 16 <= i <= 31:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
                k = 0x6ED9EBA1

            elif 32 <= i <= 47:
                f = xor(b,bool(xor(bool(c), bool(d))))
                g = (3 * i + 5) % 16
                k = 0x8F1BBCDC

            elif 48 <= i <= 63:
                f = xor(bool(c),bool(b | ~d))
                g = (7 * i) % 16
                k = 0xCA62C1D6
            f = f + a + constants[i] + w[g]
            a = d
            d = c
            c = b
            b = b + leftRotate(f,cant_rotaciones[i])
            #a, b, c, d = ((leftRotate(a, 5) + f + k + w[i]) & 0xffffffff, a, leftRotate(b, 30), c)
        #Agregando el bloque hash resultante
        A = A + a & 0xffffffff
        B = B + b & 0xffffffff
        C = C + c & 0xffffffff
        D = D + d & 0xffffffff
        #for i, val in enumerate([a, b, c, d]):
        #   hash_pieces[i] += val
        #   hash_pieces[i] &= 0xFFFFFFFF

    #salida en 128bits
    return ('%08x%08x%08x%08x' % (A, B, C, D))
    #return sum(x<<(32*i) for i, x in enumerate(hash_pieces))


def bloques(long_mensaje, tam_bloque):
        val_bloque = []
        for i in range(0, len(long_mensaje), tam_bloque):
            val_bloque.append(long_mensaje[i:i+tam_bloque])

        return val_bloque

def sha1Function(mensaje):
    #inicializacion de los buffers 5x32bits = 160
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    E = 0xC3D2E1F0
    
    long_mensaje = ""

    #preprocesamiento - conversion a bits
    for char in range(len(mensaje)):
        long_mensaje += '{0:08b}'.format(ord(mensaje[char]))
    #print(long_mensaje)
    temp = long_mensaje    
    long_mensaje += '1'

    #padding - rellenado    
    while(len(long_mensaje) % 512 != 448):
        long_mensaje += '0'
    #agregando longitud del mensaje al mensaje
    long_mensaje += '{0:064b}'.format(len(temp))
    #Creando los sub bloques a partir del mensaje en tam = 512 bits
    n_bloques = bloques(long_mensaje, 512)

    #Inicio del tratamiento 
    for sub_bloque in n_bloques:
        #separamos los subbloques en bloques de 32 bits
        words = bloques(sub_bloque, 32)
        w = [0] * 80
        for n in range(0, 16):
            w[n] = int(words[n], 2)

        #Extension de las 16 palabras de 32 bits en 80 palabras de 32bits
        for i in range(16, 80):
            w[i] = leftRotate((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]), 1)  
        
        #Initialize hash value for this n_bloques:
        a = A
        b = B
        c = C
        d = D
        e = E

        #Bucle principal 80 vueltas:
        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999

            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1

            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC

            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b, c, d, e = ((leftRotate(a, 5) + f + e + k + w[i]) & 0xffffffff, a, leftRotate(b, 30), c, d)
        #Agregando el bloque hash resultante
        A = A + a & 0xffffffff
        B = B + b & 0xffffffff
        C = C + c & 0xffffffff
        D = D + d & 0xffffffff
        E = E + e & 0xffffffff
    #salida en 160bits
    #return hh = (A leftshift 128) or (B leftshift 96) or (C leftshift 64) or (D leftshift 32) or E
    return '%08x%08x%08x%08x%08x' % (A, B, C, D, E)



def _md5_(name):
    return md5_to_hex(md5(name.encode('utf-8')))




#name = "saif"
#print("MD5 is:", md5_to_hex(md5(name)))

# OUTPUT: 
# MD5 is: 44c099ff522cd529ade21a9c7aa54ebf



#0xffffffff is used to make sure numbers dont go over 32


#************** INTERFAZ ****************#
def interfaz():
    #inicializacion de la interfaz con tkinter
    gui = Tk()
    gui.title("Calculadora de hashes op 5000k")
    gui.resizable(True,True)
    gui.iconbitmap("")
    #gui.geometry("720x480")
    gui.config(bg="#282827")
    #Canvas
    canvas = Frame()
    canvas.pack(side="left", anchor="n")
    canvas.config(width="720",height="480")
    canvas.config(bg="#282827")

    #Menu
    counter = 0

    def update():
        global counter
        counter = counter + 1
        menu.entryconfig(0, label=str(counter))

    def hello():
        print ("hello!")
    menu = Menu(gui)
    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menu, tearoff=0)
    filemenu.add_command(label="Abrir", command=hello)
    filemenu.add_command(label="Guardar", command=hello)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=gui.quit)
    menu.add_cascade(label="File", menu=filemenu)

    # create more pulldown menus
    editmenu = Menu(menu, tearoff=0)
    editmenu.add_command(label="Cortar", command=hello)
    editmenu.add_command(label="Copiar", command=hello)
    editmenu.add_command(label="Pegar", command=hello)
    menu.add_cascade(label="Editar", menu=editmenu)

    helpmenu = Menu(menu, tearoff=0)
    helpmenu.add_command(label="About", command=hello)
    menu.add_cascade(label="Help", menu=helpmenu)
    def popup(event):
        menu.post(event.x_root, event.y_root)
    # attach popup to canvas
    canvas.bind("<Button-3>", popup)
    # display the menu
    gui.config(menu=menu)

    def hashes():

        name = entrada1.get()
        suma =  CheckVar0.get()+CheckVar1.get()+CheckVar2.get()+CheckVar3.get()+CheckVar4.get()
        if(suma>1):
            return texto.set("Porfavor solo seleccione una opcion")
        elif(suma==0):
            return texto.set("Porfavor seleccione una opcion")
        else:
            if(CheckVar0.get()):
                return texto.set("no hay md4 aun ;c")
            elif(CheckVar1.get()):
                return texto.set(_md5_(name))
            elif(CheckVar2.get()):
                return texto.set(sha1Function(name))
            elif(CheckVar3.get()):
                return texto.set("no hay sha256 aun ;c")
            elif(CheckVar4.get()):
                return texto.set("no hay Hmac aun ;c")

    
    #BOTONES
    texto = StringVar()
    clave = StringVar()
    etiqueta1 = Label(canvas,text="Ingrese el texto plano en ascii o hex:",bg="#282827",fg="white")
    etiqueta1.pack(padx=5,pady=4,ipadx=5,ipady=5)
    entrada1 = Entry(canvas)
    entrada1.pack(padx=5,pady=5,ipadx=5,ipady=5)
    
    etiqueta2 = Label(canvas,text="Ingrese la clave en ascii o hex \n(al dejar vacio este campo la clave será generada por defecto):",bg="#282827",fg="white")
    etiqueta2.pack(padx=5,pady=4,ipadx=5,ipady=5)
    entrada2 = Entry(canvas)
    entrada2.pack(padx=5,pady=5,ipadx=5,ipady=5)
    CheckVar0 = IntVar()
    CheckVar1 = IntVar()
    CheckVar2 = IntVar()
    CheckVar3 = IntVar()
    CheckVar4 = IntVar()
    C0 = Checkbutton(canvas, text = "MD4:", variable = CheckVar0,onvalue = 1, offvalue = 0, height=2, width = 5,bg="#282827",fg="white")
    C1 = Checkbutton(canvas, text = "MD5:", variable = CheckVar1,onvalue = 1, offvalue = 0, height=2, width = 5,bg="#282827",fg="white")
    C2 = Checkbutton(canvas, text = "Sha-1:", variable = CheckVar2,onvalue = 1, offvalue = 0, height=2, width = 5,bg="#282827",fg="white")
    C3 = Checkbutton(canvas, text = "Sha-256:", variable = CheckVar3,onvalue = 1, offvalue = 0, height=2, width = 5,bg="#282827",fg="white")
    C4 = Checkbutton(canvas, text = "HMac:", variable = CheckVar4,onvalue = 1, offvalue = 0, height=2, width = 5,bg="#282827",fg="white")
    C0.pack()
    C1.pack()
    C2.pack()
    C3.pack()
    C4.pack()

    boton1 = Button(canvas,text="Ejecutar",fg="#282827",command=hashes)
    boton1.pack(side=TOP)
    etiqueta3 = Label(canvas,text="Texto encriptado:",bg="#282827",fg="white")
    etiqueta3.pack(padx=5,pady=4,ipadx=5,ipady=5)
    resultado = Label(canvas,bg="#282827",fg="white",textvariable=texto,padx=5,pady=5,width=50)
    resultado.pack()


    #bucle infinito
    gui.mainloop()


interfaz()
#print(md5dos("hola"))
