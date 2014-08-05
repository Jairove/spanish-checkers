#Damas Espanolas
#Jairo Velasco Martin
#05/2014

import pygtk
import gtk

#Clase de la interfaz grafica
class Interfaz:
    
    def __init__(self):
        
        #Inicializamos atributos
        self.click1 = None
        self.tablero = Tablero()
        self.turno = True
        self.pila = []
        self.num = (str(self.tablero.num_piezas(self.turno)))
        self.numpiezas = ("Te quedan "+self.num +" pieza/s restantes")
        print self.numpiezas

        #Creamos un contenedor horizontal para las damas, otro para la informacion de turno, y un contenedor vertical principal
        self.damas_box = gtk.HBox(False, 0)
        self.turno_box = gtk.VBox(False, 0)
        self.main_box = gtk.VBox(False, 0)
        
        #Creamos la ventana, le damos titulo, e indicamos el metodo que maneja su cierre:
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Damas')
        self.window.connect("delete_event", gtk.main_quit)
        
        #Creamos los botones, la imagen del turno y los textos
        self.boton1 = gtk.Button("Deshacer jugada")
        self.boton2 = gtk.Button("Guardar partida")
        self.boton3 = gtk.Button("Cargar partida")
        self.boton4 = gtk.Button("Nueva partida")
        self.boton1.connect("clicked", self.deshacer)
        self.boton2.connect("clicked", self.guardar_partida)
        self.boton3.connect("clicked", self.cargar_partida)
        self.boton4.connect("clicked", self.on_click_boton_nueva_partida)
        self.imagen_turno = gtk.image_new_from_file('images/turno_blanco.png')
        self.texto_piezas = gtk.Label(str(self.numpiezas))
        self.texto_turno = gtk.Label("Es turno de jugador BLANCO")
        
        #Creamos la tabla que contendra las event box del tablero, y una lista que contendra referencias a cada event box
        self.table = gtk.Table(8, 8, True)
        self.lista = range(64)
        
        contador = -1
        negras = [1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23]
        blancas = [40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]
        fondo_claro = True
        fondo_negro = False
        i=7
        
        while(i>=0):
            fondo_claro = not fondo_claro
            for j in range(8):
                contador = contador +1
                #Creamos la caja de eventos y le fijamos atributos fila y columna
                self.lista[contador] = gtk.EventBox()
                self.lista[contador].fila = i
                self.lista[contador].columna = j

                #Le asignamos una imagen a la caja de eventos, dependiendo de su posicion (mas tarde, al refrescar el tablero, dependera tambien de su contenido)
                if contador in negras:
                    if fondo_claro == True:
                        self.lista[contador].add(gtk.image_new_from_file('images/dama_negra.png'))
                        self.lista[contador].color = 'negro'
                elif contador in blancas:
                    if fondo_claro == True:
                        self.lista[contador].add(gtk.image_new_from_file('images/dama_blanca.png'))
                        self.lista[contador].color = 'blanco'
                else:
                    if fondo_claro == True:
                        self.lista[contador].add(gtk.image_new_from_file('images/casillablanca.png'))
                        self.lista[contador].color = 'claro'
                    else:
                        self.lista[contador].add(gtk.image_new_from_file('images/casillanegra.png'))
                        self.fondo_negro = True
                        self.lista[contador].color = 'oscuro'
                self.lista[contador].fondo_claro = fondo_claro
                fondo_claro = not fondo_claro

                self.lista[contador].connect("button_press_event", self.casilla_pulsada)
                #Metemos la caja de eventos con la que hemos trabajado en una celda de la tabla e iteramos hasta acabar
                self.table.attach(self.lista[contador], j, j+1, i, i+1)
            i = i-1

        #Posicionamos los elementos en sus contenedores, la tabla dentro de damas_box, damas_box dentro de main_box... etc
        self.turno_box.pack_start(self.texto_turno, False, False, 0)
        self.turno_box.pack_start(self.texto_piezas, False, False, 0)
        self.turno_box.add(self.imagen_turno)
        self.damas_box.pack_start(self.boton1, True, True, 0)
        self.damas_box.pack_start(self.boton2, True, True, 0)
        self.damas_box.pack_start(self.boton3, True, True, 0)
        self.damas_box.pack_start(self.boton4, True, True, 0)
        self.main_box.pack_start(self.turno_box, True, True, 0)
        self.main_box.pack_start(self.table, True, True, 0)
        self.main_box.pack_start(self.damas_box, True, True, 0)

        #Lo metemos en la ventana y mostramos
        self.window.add(self.main_box)
        self.window.show_all()      

    def casilla_pulsada(self, widget, data=None):
        
        
        #Si es el primer click lo guardamos en una tupla
        if self.click1 == None:
            self.click1 = (abs(widget.fila-7), widget.columna)
            
            #Marcamos la primera casilla seleccionada cambiando su imagen
            i = abs(widget.fila-7)
            j = widget.columna
            cas = self.tablero.tablero[i][j]
            celda = self.table.get_children()[((7-i)*8)+(7-j)]

            if cas == (False,True,False):
                celda.get_child().set_from_file("images/dama_blanca_activa.png")
            if cas == (False,False,False):
                celda.get_child().set_from_file("images/dama_negra_activa.png")
            if cas == (False,True,True):
                celda.get_child().set_from_file("images/reina_blanca_activa.png") 
            if cas == (False,False,True):
                celda.get_child().set_from_file("images/reina_negra_activa.png") 
       
        else:
            self.click2 = (abs(widget.fila-7), widget.columna)
            #Si es el segundo click empaquetamos el primero y el segundo en una tupla
            self.pulsacion = (self.click1[0], self.click1[1], self.click2[0], self.click2[1])
            print ('Comando introducido: ')
            print self.pulsacion
            #Verificamos la jugada y la ejecutamos si es correcta
            res = self.tablero.verificar_jugada(self.turno,self.pulsacion)
            if (res < 0):
                self.tablero.jugar(self.pulsacion,self.turno,self.pila)
                #Detectamos si ha finalizado la partida
                self.numpiezas = self.tablero.num_piezas(not self.turno)
                if self.numpiezas == 0:
                    mensaje = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE) #Emplearemos este dialogo de mensaje para ser mostrado si se gana el juego
                    if self.turno:
                        self.refrescar_tablero()
                        mensaje.set_markup("Enhorabuena jugador BLANCO de la casa Stark, has ganado la partida. Se va a iniciar una nueva partida")
                        mensaje.run()
                        mensaje.destroy()
                        self.nueva_partida()
                    else:
                        self.refrescar_tablero()
                        mensaje.set_markup("Enhorabuena jugador NEGRO de la casa Lannister, has ganado la partida. Se va a iniciar una nueva partida")
                        mensaje.run()
                        mensaje.destroy()
                        self.nueva_partida()
                self.cambiar_turno()
            else:
                mensaje_error = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
                error = self.tablero.msg_status[res]
                print error
                mensaje_error.set_markup(error)
                mensaje_error.run()
                mensaje_error.destroy() 
            #Una vez hecha la jugada, actualizamos como se ve el tablero de la interfaz
            self.refrescar_tablero()
            
            #Reseteamos variables para recibir nuevos clicks
            self.click1 = None
            self.click2 = None 

    #Metodo que nos permite cambiar de turno, modificando no solo este, si no tambien los textos e imagen asociados a el
    def cambiar_turno(self):
            self.turno = not self.turno  
            self.num = str(self.tablero.num_piezas(self.turno))
            self.numpiezas = ("Te quedan "+self.num +" pieza/s restantes")
            self.texto_piezas.set_text(str(self.numpiezas))
            if self.turno:
                self.texto_turno.set_text("Es turno de jugador BLANCO")
                self.imagen_turno.set_from_file("images/turno_blanco.png") 
            else:
                self.texto_turno.set_text("Es turno de jugador NEGRO")
                self.imagen_turno.set_from_file("images/turno_negro.png") 
            print self.numpiezas    

    #Metodo que nos permite actualizar las imagenes del tablero en funcion de su contenido
    def refrescar_tablero(self):
        contador = -1
        for i in range(8):
            for j in range(8):
                contador = contador+1
                cas = self.tablero.tablero[i][j]
                celda = self.table.get_children()[((7-i)*8)+(7-j)]
                if cas == (False,True,False):
                    celda.get_child().set_from_file("images/dama_blanca.png")
                if cas == (False,False,False):
                    celda.get_child().set_from_file("images/dama_negra.png") 
                if cas == (False,True,True):
                    celda.get_child().set_from_file("images/reina_blanca.png") 
                if cas == (False,False,True):
                    celda.get_child().set_from_file("images/reina_negra.png") 
                if cas == (True,False,False):
                    if not self.lista[contador].color == 'oscuro':
                        celda.get_child().set_from_file("images/casillablanca.png")

    #Este metodo permite deshacer jugadas
    def deshacer(self, widget, data=None):     
        try:
            self.tablero.deshacer_movimiento(self.pila)
            self.cambiar_turno()
            self.refrescar_tablero()
        except IndexError:
            mensaje_error = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
            mensaje_error.set_markup("No quedan jugadas por deshacer.")
            mensaje_error.run()
            mensaje_error.destroy() 
            print "No quedan jugadas por deshacer."

    #Metodo que toma de la pila de jugadas los comandos que se han ido introduciendo en la partida, los traduce y los guarda en un fichero.
    #Es llamado al pulsar el boton "guardar partida"
    #Guarda en un fichero savegame.txt y en formato coordenadas (ej: A4B5)
    def guardar_partida(self, widget, data=None):
    	
    	cont=0
    	fich = open("savegame.txt", 'w')
        dic = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    	for i in self.pila:
    		cad = []
    		cad.append(str(dic[self.pila[cont][0]]))
    		cad.append(str(self.pila[cont][1]+1))
    		cad.append(str(dic[self.pila[cont][2]]))
    		cad.append(str(self.pila[cont][3]+1))
    		comando = "".join(cad)
    		fich.write(comando)
    		fich.write("\n")
    		cont = cont+1
    	fich.close()
        
        #Informamos de que se ha guardado
        mensaje = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE)
        mensaje.set_markup("Se ha guardado la partida.")
        mensaje.run()
        mensaje.destroy()

    #Metodo que lee las jugadas de un fichero en el mismo formato en que se guardan (por coordenadas)
    def cargar_partida(self, widget, data=None):

        #Reseteamos variables de la partida en curso, para cargar la partida guardada
        self.tablero = Tablero()
        self.turno = True
        self.pila = []

        mensaje = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE)
        
        #Leemos los comandos que contiene el archivo de partida guardada y ejecutamos las jugadas
        try:
            fich = open("savegame.txt", 'r')
            dic = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
            cad = fich.readline(4)
            fich.readline()
            
            #En caso de que la primera linea del fichero este vacia, no hay partida guardada
            if cad == '':
                mensaje = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE)
                mensaje.set_markup("No existen partidas guardadas, se ha cargado una nueva partida.")
                mensaje.run()
                mensaje.destroy()
                return
            #Mientras no se lea una linea vacia se realiza jugada y se lee otra.
            #No verificamos la jugada porque esta se guardo tras ser verificada, por tanto todas las del fichero son correctas.
            while not (cad == ''):
                jugada = (int(dic[cad[0]]),(int(cad[1])-1),int(dic[cad[2]]),(int(cad[3])-1))
                print "Comandos cargados:"
                print jugada
                self.tablero.jugar(jugada,self.turno,self.pila)
                self.cambiar_turno() 
                cad = fich.readline(4)
                fich.readline()
            self.refrescar_tablero()
            
            #Informamos de que se ha cargado
            mensaje.set_markup("Se ha cargado la ultima partida guardada.")
            mensaje.run()
            mensaje.destroy()
        
        except IOError:
            mensaje_error = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
            mensaje_error.set_markup("No hay partidas guardadas.")
            mensaje_error.run()
            mensaje_error.destroy() 

    #Metodo que permite resetear variables para empezar otra partida
    def nueva_partida(self):
        #Reseteamos variables de la partida en curso, para iniciar una nueva
        self.tablero = Tablero()
        self.pila = []
        self.refrescar_tablero()

        #Si es turno negro, cambiamos, en caso de ser blanco resetamos el numero de piezas
        if not self.turno:
            self.cambiar_turno()
        else:
            self.num = str(self.tablero.num_piezas(self.turno))
            self.numpiezas = ("Te quedan "+self.num +" pieza/s restantes")
            self.texto_piezas.set_text(str(self.numpiezas))

        #Informamos de que se ha creado
        mensaje = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE)
        mensaje.set_markup("Se ha creado una nueva partida.")
        mensaje.run()
        mensaje.destroy()

    def on_click_boton_nueva_partida(self, widget, data=None):
    	self.nueva_partida()

class Tablero:


    # Constructor del tablero
    def __init__(self):
        self.tablero = [[],[],[],[],[],[],[],[]]
        for fil in range(8):
            for col in range(8):
                if (fil+col) % 2 == 1:
                    if fil < 3:
                        c = self.llenar_casilla(2)
                        self.tablero[fil].append(c)
                    elif fil > 4:
                        c = self.llenar_casilla(1)
                        self.tablero[fil].append(c)
                    else:
                        c = self.llenar_casilla(5)
                        self.tablero[fil].append(c)
                else:
                    c = self.llenar_casilla(5)
                    self.tablero[fil].append(c)

        self.sel_vacia = 0
        self.sel_color = 1
        self.sel_reina = 2

        # Las 5 posibilidades para cada casilla:
        self.peon_blanco   = (False,True,False)
        self.peon_negro    = (False,False,False)
        self.reina_blanca  = (False,True,True)
        self.reina_negra   = (False,False,True)
        self.casilla_vacia = (True,False,False)

        # Para pasar de coordenadas numericas a caracteres
        self.nom_fil = "ABCDEFGH"
        self.nom_col = "12345678"

        # Mensajes asociados al valor devuelto por verificar_jugada
        self.msg_status = [
            "Sintaxis no valida",
            "Casilla origen vacia",
            "Casilla origen no contiene pieza del color correspondiente al turno actual",
            "Movimiento no diagonal",
            "Existen piezas intermedias en el movimiento",
            "Casilla de destino no es adyacente",
            "Casilla de destino ocupada por pieza del mismo color",
            "No se puede capturar una pieza en el borde del tablero",
            "Captura bloqueada por otra pieza adyacente"]

        # self.DIRS es una lista con las direcciones de las 4 diagonales
        self.DIRS = [(-1,-1),(-1,1),(1,-1),(1,1)]

    # Metodo que rellena una tupla de una manera u otra dependiendo del tipo de casilla que se desee
    def llenar_casilla(self, tipo):
        if tipo==1: 
            casilla = (False,True,False)  
            return casilla #PEON BLANCO
        if tipo==2: 
            casilla = (False,False,False) 
            return casilla #PEON NEGRO
        if tipo==3: 
            casilla = (False,True,True)   
            return casilla #REINA BLANCA
        if tipo==4: 
            casilla = (False,False,True)  
            return casilla #REINA NEGRA
        if tipo==5: 
            casilla = (True,False,False)  
            return casilla #CASILLA VACIA

    # Devuelve +1 si x > 0, -1 si x < 0, 0 si x == 0
    def signo(self, x):
        return 1 if x > 0 else (-1 if x < 0 else 0)

    # Verifica si una jugada es correcta dado un tablero y el turno actual
    # Devuelve un entero indicando el estado:
    # -1  : Movimiento correcto, no hay captura
    # -2  : Movimiento correcto con captura de pieza
    # >=0 : Movimiento incorrecto, la lista self.msg_status informa del tipo de error
    def verificar_jugada(self, turno, jugada):
        # Sintaxis valida
        for i in jugada:
            if i < 0 or i > 7:
                return 0
        
        (f0,c0,f1,c1) = jugada
        # Casilla de origen vacia
        print('Contenido de origenes: ')
        print self.tablero[f0][c0]
        if self.tablero[f0][c0] == self.casilla_vacia:
            return 1
        # Casilla de origen con pieza de color distinto al turno
        if self.tablero[f0][c0][self.sel_color] != turno:
            return 2
        # Movimiento diagonal
        # Nota: No es necesario comprobar que d > 0, error captura pieza propia
        d = abs(f1-f0)
        if d != abs(c1-c0):
            return 3
        sf, sc = self.signo(f1-f0), self.signo(c1-c0)
        # Movimiento adyacente si es un peon o libre de obstaculos si reina
        if self.tablero[f0][c0][self.sel_reina]:
            for i in range(1,d):
                if self.tablero[f0+i*sf][c0+i*sc] != self.casilla_vacia:
                    return 4
        else:
            if d != 1:
                return 5
        # Casilla de destino vacia (resultado correcto, no hay captura)
        if self.tablero[f1][c1] == self.casilla_vacia:
            return -1
        # Casilla de destino ocupada:
        # Comprobar que es pieza de distinto color al del turno
        if self.tablero[f1][c1][self.sel_color] == turno:
            return 6
        # Captura: Calcular celda de destino tras captura
        f2, c2 = f1+sf, c1+sc
        # Comprobar que este en rango y vacia
        if f2 < 0 or f2 > 7 or c2 < 0 or c2 > 7:
            return 7
        if self.tablero[f2][c2] != self.casilla_vacia:
            return 8
        # Movimiento correcto y se produce captura
        return -2

    # Realiza un movimiento (debe verificarse previamente que es correcto)
    # Almacena todos los datos del movimiento en una pila
    # No solo posiciones de origen y destino sino informacion de pieza
    # capturada y si se ha producido promocion a reina
    # Formato: (f0,c0,f1,c1,f2,c2,casilla capturada,promocion)
    # Deteccion de captura: f1 != f2
    # Devuelve True si se ha realizado una captura

    def hacer_movimiento(self, jugada, pila):
        (f0,c0,f1,c1) = jugada
        # Detectar si es captura y calcular posicion final
        captura = self.tablero[f1][c1] != self.casilla_vacia
        if captura:
            f2,c2 = f1+self.signo(f1-f0), c1+self.signo(c1-c0)
        else:
            f2,c2 = f1,c1
        # Detectar si es promocion a reina
        color = self.tablero[f0][c0][self.sel_color]
        if self.tablero[f0][c0][self.sel_reina]:
            promocion = False
        else:
            promocion = (color and f2 == 0) or (not color and f2 == 7)
        # Incluir movimiento en pila
        pila.append((f0,c0,f1,c1,f2,c2,self.tablero[f1][c1],promocion))
        # Actualizar tablero
        if promocion:
            self.tablero[f2][c2] = (False, color, True)
        else:
            self.tablero[f2][c2] = self.tablero[f0][c0]
        if captura:
            self.tablero[f1][c1] = self.casilla_vacia
        self.tablero[f0][c0] = self.casilla_vacia
        return captura

    # Deshace el ultimo movimiento realizado (almacenado en la pila)
    # Es el inverso del procedimiento anterior
    def deshacer_movimiento(self, pila):
        (f0,c0,f1,c1,f2,c2,casilla,promocion) = pila.pop()
        color = self.tablero[f2][c2][self.sel_color]
        if promocion:
            self.tablero[f0][c0] = (False, color, False)
        else:
            self.tablero[f0][c0] = self.tablero[f2][c2]
        self.tablero[f2][c2] = self.casilla_vacia
        if f1 != f2: # Captura
            self.tablero[f1][c1] = casilla

    # Realiza una jugada completa (maximo numero de capturas)
    # Supone que la jugada es correcta
    # Adapta el tablero a la nueva posicion
    # No cambia el turno
    def jugar(self, jugada, turno, pila):
        if self.hacer_movimiento(jugada, pila):
            # Se ha producido una captura: Explorar posibles nuevas capturas
            (_,_,_,_,f0,c0,_,_) = pila[-1]
            (n,f1,c1) = self.explorar(f0, c0, turno, pila)
            if n > 0: # Existen nuevas capturas, la optima comienza por (f1,c1)
                self.jugar((f0,c0,f1,c1), turno, pila)

    # Explora las posibles capturas de la pieza en posicion (f0,c0) y devuelve
    # una tupla (n,f1,c1) con el movimiento que produce un mayor numero de
    # capturas (n). Si no hay ninguna captura posible entonces n = 0
    def explorar(self, f0, c0, turno, pila):
       nmax = 0 # Numero maximo de capturas
       fmax = cmax = -1 # Movimiento con mayor numero de capturas
       reina = self.tablero[f0][c0][self.sel_reina]
       # Examinar las 4 diagonales
       for (sf,sc) in self.DIRS:
           f1, c1 = f0+sf, c0+sc
           # Si es reina, avanzar por la diagonal hasta encontrar una pieza
           if reina:
               while 0 <= f1 <= 7 and 0 <= c1 <= 7 and self.tablero[f1][c1][self.sel_vacia]:
                   f1 += sf
                   c1 += sc
           # Si el movimiento es valido y es una captura..
           if self.verificar_jugada(turno, (f0,c0,f1,c1)) == -2:
               # Hacer movimiento
               self.hacer_movimiento((f0,c0,f1,c1), pila)
               # Explorar a partir del movimiento
               (_,_,_,_,f2,c2,_,_) = pila[-1]
               (n,_,_) = self.explorar(f2, c2, turno, pila)
               # Deshacer movimiento
               self.deshacer_movimiento(pila)
               # Comprobar si las capturas superan el maximo
               n += 1
               if n > nmax:
                   nmax, fmax, cmax = n, f1, c1
       # Devolver el resultado
       return (nmax,fmax,cmax)

    # Numero de piezas del color del turno
    def num_piezas(self, turno):
        n = 0
        for fila in self.tablero:
            for (vacia,color,_) in fila:
                if not vacia and color == turno:
                    n += 1
        return n

def main():  
    Interfaz()
    gtk.main()      

if __name__=='__main__':
    main()
