import tkinter as tk
from tkinter import messagebox
import requests


def buscar_clima():
    cidade = entrada_cidade.get()
    api_key = "78192a2b6e43c04b8cf1dc24be0dd5e6"

    url = "https://api.openweathermap.org/data/2.5/weather"

    parametros = {
        "q": cidade,
        "appid": api_key,
        "units": "metric",
        "lang": "pt_br"
    }

    try:

        requisicao = requests.get(url, params=parametros)
        dados = requisicao.json()

        if requisicao.status_code == 200:
            temperatura = dados['main']['temp']
            descricao = dados['weather'][0]['description']
            umidade = dados['main']['humidity']
            cidade_nome = dados['name']
            pais = dados['sys']['country']

            label_resultado['text'] = f"{cidade_nome}, {pais}"
            label_temp['text'] = f"{temperatura:.1f}°C"
            label_desc['text'] = descricao.capitalize()
            label_detalhes['text'] = f"Umidade: {umidade}%"

        else:

            mensagem_erro = dados.get("message", "Erro desconhecido")
            print(f"Erro detalhado: {dados}")

            if dados.get("cod") == 401:
                messagebox.showerror(
                    "Erro de Autenticação", "Sua API Key é inválida ou ainda não foi ativada. Espere alguns minutos.")
            elif dados.get("cod") == "404":
                messagebox.showerror(
                    "Erro", "Cidade não encontrada. Verifique a digitação.")
            else:
                messagebox.showerror("Erro API", f"Erro: {mensagem_erro}")

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro", "Verifique sua conexão com a internet.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


root = tk.Tk()
root.title("Dashboard de Clima")
root.geometry("350x400")
root.configure(bg="#f0f8ff")


titulo = tk.Label(root, text="Previsão do Tempo", font=(
    "Helvetica", 18, "bold"), bg="#f0f8ff", fg="#333")
titulo.pack(pady=20)


entrada_cidade = tk.Entry(root, font=("Helvetica", 12),
                          width=20, justify='center')
entrada_cidade.pack(pady=5)

entrada_cidade.bind('<Return>', lambda event: buscar_clima())


botao_buscar = tk.Button(root, text="Buscar", command=buscar_clima, font=(
    "Helvetica", 10, "bold"), bg="#4a90e2", fg="white")
botao_buscar.pack(pady=10)


tk.Frame(root, height=2, bg="#ccc", width=300).pack(pady=10)


label_resultado = tk.Label(root, text="", font=(
    "Helvetica", 16, "bold"), bg="#f0f8ff", fg="#333")
label_resultado.pack()

label_temp = tk.Label(root, text="", font=(
    "Helvetica", 35, "bold"), bg="#f0f8ff", fg="#ff6b6b")
label_temp.pack(pady=10)

label_desc = tk.Label(root, text="", font=(
    "Helvetica", 12), bg="#f0f8ff", fg="#555")
label_desc.pack()

label_detalhes = tk.Label(root, text="", font=(
    "Helvetica", 10), bg="#f0f8ff", fg="#777")
label_detalhes.pack(pady=5)


root.mainloop()
