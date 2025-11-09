import tkinter as tk

window = tk.Tk()
window.title('Ventana principal')
window.geometry('800x600')
icon = tk.PhotoImage(file='db_icon.png')
barra_menus = tk.Menu(window)
window.iconphoto(True,icon)
window.config(menu=barra_menus)
menu = tk.Menu(barra_menus, tearoff=False)
barra_menus.add_cascade(label='menu', menu=menu)
menu.add_command(label='Opción 1', command=print("hola mundo"))
menu.add_command(label='Opción 2', command=print("Adios"))


window.mainloop()


