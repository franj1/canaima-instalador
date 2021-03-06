# -*- coding: utf-8 -*-
#
# Copyright 2012 Erick Birbe <erickcion@gmail.com>
#
# TablaParticiones is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ucumari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ucumari; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

import gtk
import clases.general as gen

program = {
	'name'	: 'Particiones',
	'version':'1.0',
}

class TablaParticiones (gtk.TreeView):

    liststore = None
    columnas = {}
    ultima_fila_seleccionada = None

    def __init__(self):

        # Tipos de valores a mostrar en la tabla
        self.liststore = gtk.ListStore(str, str, str, str, str, int, int)

        gtk.TreeView.__init__(self, model=self.liststore)
        self.set_headers_clickable(False)
        #self.connect("row-activated", self._accion_doble_click)
        #self.connect("cursor-changed", self._accion_seleccionar)

        self.armar_tabla()

    def set_seleccionar(self, callback):
        'Determina la funcion que se ejecutará al hacer click'
        self.seleccionar = callback

    def _accion_seleccionar(self, treeview):
        '''Hace el llamado a la funcion indicada en set_seleccionar, pasandole
        los parametros correspondientes'''
        fila = self.get_fila_seleccionada()
        if fila != self.ultima_fila_seleccionada:
            self.ultima_fila_seleccionada = fila
            self.seleccionar(fila)

    def set_doble_click(self, callback):
        self.doble_click = callback

    def _accion_doble_click(self, treeview, path, column):
        modelo = treeview.get_model()
        iter = modelo.get_iter(path)
        fila = modelo.get(iter, 0, 1, 2, 3, 4, 5, 6)

        self.doble_click(fila)

    def get_fila_seleccionada(self):
        '''Obtiene la fila que esta seleccionada al momento de su llamado, si no
        hay filas seleccionadas retornará None'''

        obj_seleccion = self.get_selection().get_selected()
        modelo = obj_seleccion[0]
        iterador = obj_seleccion[1]

        if iterador != None:
            return modelo.get(iterador, 0, 1, 2, 3, 4, 5, 6)
        else:
            return None

    def armar_tabla(self):
        'Crea la tabla'

        # Columnas
        self.nueva_columna_texto("Dispositivo", 0)
        self.nueva_columna_texto("Tipo", 1)
        self.nueva_columna_texto("Formato", 2)
        self.nueva_columna_texto("Punto de Montaje", 3)
        self.nueva_columna_texto("Tamaño", 4)
        self.nueva_columna_texto("Inicio", 5)
        self.nueva_columna_texto("Fin", 6)

        # Ocultar las columnas que no se desean mostrar
        #self.columnas[7].set_visible(False)
        #self.columnas[8].set_visible(False)
        #self.columnas[9].set_visible(False)

    def nueva_columna_color(self, title, index):
        'Crea nueva columna de color en el TreeView'

        celda = gtk.CellRendererText()

        self.columnas[index] = gtk.TreeViewColumn(title, celda, text=index)
        self.columnas[index].set_reorderable(False)
        self.columnas[index].set_min_width(40)
        self.columnas[index].set_cell_data_func(celda, self.colorear_celda)

        self.insert_column(self.columnas[index], index)

    def nueva_columna_texto(self, title, index):
        'Crea nueva columna de texto en el TreeView'

        celda = gtk.CellRendererText()
        celda.set_property('cell-background-gdk', gtk.gdk.color_parse("#FFF"))

        self.columnas[index] = gtk.TreeViewColumn(title, celda, text=index)
        self.columnas[index].set_resizable(True)
        self.columnas[index].set_reorderable(False)

        #columna.connect("clicked", self.on_column_clicked, index)
        self.insert_column(self.columnas[index], index)

    def nueva_columna_check(self, title, index):
        'Crea nueva columna de seleccion en el TreeView'

        celda = gtk.CellRendererToggle()

        self.columnas[index] = gtk.TreeViewColumn(title, celda, active=index)
        self.columnas[index].set_resizable(False)
        self.columnas[index].set_reorderable(False)

        self.insert_column(self.columnas[index], index)

    def colorear_celda(self, columna, celda, modelo, iter):
        color = modelo.get_value(iter, 0)
        celda.set_property('background', color)
        celda.set_property('text', None)
        return

    #def agregar_fila(self, color='', dispositivo='', tipo='', formato='', montaje='', tamano='', formatear=False, inicio='', fin='', num=''):
    def agregar_fila(self, lista):
        'Agrega los datos a las filas'
        self.liststore.append([lista[0],
                               lista[1],
                               lista[2],
                               lista[3],
                               lista[4],
                               lista[5],
                               lista[6]])
        #self.liststore.append([color, 
        #                       dispositivo, 
        #                       tipo, 
        #                       formato, 
        #                       montaje, 
        #                       gen.hum(gen.kb(tamano)), 
        #                       formatear, 
        #                       inicio, 
        #                       fin])

datos_ejemplo = [
    ['#ff0000', '/dev/sda1', 'Primaria', 'fat32', '', '32 GB', False, 1],
    ['#00ff00', '/dev/sdb1', 'Primaria', 'ext2', '/boot', '512 MB', True, 1],
    ['#0000ff', 'Nueva', 'Extendida', '', '', '100 GB', False, 30],
    ['#0f0f0f', 'Nueva', 'Logica', 'ext4', '/', '20 GB', True, 45],
    ['#f0f0f0', 'Nueva', 'Logica', 'ext4', '/home', '78 GB', True, 70],
    ['#0f00f0', 'Nueva', 'Logica', 'Swap', '', '1.8 GB', True, 100],
]

class Ventana:

    def __init__(self):

        self.tabla = TablaParticiones()
        self.llenar_tabla(datos_ejemplo)
        self.tabla.set_doble_click(self.funcion_prueba);
        self.tabla.show()

        # Marco para la tabla
        self.marco = gtk.Frame()
        self.marco.add(self.tabla)
        self.marco.show()

        # Contenedor VBox
        self.vbox = gtk.VBox(False, 0)
        self.vbox.pack_start(self.marco, True, True, 0)
        self.vbox.show()

        # Crea una ventana
        self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.ventana.set_title(program['name'] + " " + program['version'])
        self.ventana.add(self.vbox)
        self.ventana.connect("destroy", self.destroy)
        self.ventana.show()

    def llenar_tabla(self, data=None):
        assert isinstance(data, list) or isinstance(data, tuple)

        for fila in datos_ejemplo:
            self.tabla.agregar_fila(fila[0], fila[1], fila[2], fila[3], \
                                    fila[4], fila[5], fila[6], fila[7], fila[8])

    def funcion_prueba(self, tupla):
        print "Hola, acabas de accionar una fila:";
        print "\t", tupla

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        'Funcion Principal'
        gtk.main()


if __name__ == "__main__":
    v = Ventana()
    v.main()
