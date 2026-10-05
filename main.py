from tkinter import Tk, Button, Label, Entry, filedialog, messagebox, Text, END, Frame
from gtts import gTTS
import PyPDF2
import os
import uuid

def seleccionar_pdf():
    archivo = filedialog.askopenfilename(
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Selecciona un archivo PDF"
    )
    entry_pdf.delete(0, END)
    entry_pdf.insert(0, archivo)

def convertir_mp3():
    ruta_pdf = entry_pdf.get()
    texto_input = text_box.get("1.0", END).strip()
    nombre_audio = entry_nombre.get().strip()
    texto = ""

    if ruta_pdf:
        try:
            with open(ruta_pdf, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    texto += page.extract_text() + "\n"
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el PDF: {e}")
            return
    elif texto_input:
        texto = texto_input
    else:
        messagebox.showwarning("Advertencia", "Debes seleccionar un archivo PDF o ingresar texto.")
        return

    if texto.strip():
        if not nombre_audio:
            nombre_audio = f"audio_{uuid.uuid4().hex[:8]}.mp3"
        else:
            if not nombre_audio.lower().endswith(".mp3"):
                nombre_audio += ".mp3"
        try:
            tts = gTTS(text=texto, lang='es')
            tts.save(nombre_audio)
            messagebox.showinfo("Éxito", f"¡Audio generado como {nombre_audio}!")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el audio: {e}")
    else:
        messagebox.showwarning("Advertencia", "No se encontró texto para convertir.")

root = Tk()
root.title("Narrador PDF/Text a MP3")
root.geometry("500x420")

# Sección PDF
frame_pdf_section = Frame(root)
frame_pdf_section.pack(fill="x", pady=5)

Label(frame_pdf_section, text="Selecciona un archivo PDF:").pack(pady=5)
entry_pdf = Entry(frame_pdf_section, width=40)
entry_pdf.pack(side="left", padx=10)
Button(frame_pdf_section, text="Buscar PDF", command=seleccionar_pdf).pack(side="left", padx=5)

# Separador visual
Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", padx=10, pady=10)

# Input nombre de audio
Label(root, text="Nombre del archivo de audio (opcional):").pack(pady=5)
entry_nombre = Entry(root, width=40)
entry_nombre.pack(padx=10)

# Input texto
Label(root, text="O ingresa el texto a convertir:").pack(pady=5)
text_box = Text(root, height=8, width=55)
text_box.pack(padx=10)

Button(root, text="Convertir MP3", command=convertir_mp3, bg="#4CAF50", fg="white").pack(pady=20)

root.mainloop()
