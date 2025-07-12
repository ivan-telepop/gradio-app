import gradio as gr
import subprocess


# ollama run llama3.2
OLLAMA_MODELS = ["llama3.2","mistral","llama2", "gemma", "phi3"]


# Stop all processed ollamas instances


def stop_all_models():
    #subprocess.run(["ollama", "stop", "--all"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run("ollama ps | awk 'NR>1 {print $1}' | xargs -L 1 -I {} ollama stop {}",shell=True)

def start_model(model_name):
    stop_all_models()
    result = subprocess.run(["ollama", "run", model_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return f"Модель {model_name} запущена." if result.returncode == 0 else f"Ошибка запуска: {result.stderr.decode()}"

def chat_with_model(user_input, history):
    try:
        process = subprocess.run(
            ["ollama", "run", selected_model, user_input],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20
        )
        response = process.stdout.decode().strip()
        history.append((user_input, response))
    except Exception as e:
        history.append((user_input, f"[Ошибка]: {str(e)}"))
    return "", history

selected_model = OLLAMA_MODELS[0]  # по умолчанию ollama3.2

def on_model_change(model):
    global selected_model
    selected_model = model
    return f"Выбрана модель: {model}"


with gr.Blocks() as actualChat:
    gr.Markdown("🖥 Чат с Ollama - приложение [ Ivan Goncharov ]")
    with gr.Row():
        model_dropdown = gr.Dropdown(choices=OLLAMA_MODELS, value=selected_model, label="Выбор модели")
        model_dropdown.change(on_model_change, inputs=[model_dropdown], outputs=gr.Textbox(visible=False))
        start_button = gr.Button("Запуск модели Ollama")
    status = gr.Textbox(label="Статус запуска", interactive=False)
    start_button.click(fn=start_model, inputs=[model_dropdown], outputs=[status])
    chatbot = gr.Chatbot(label="Чат с моделью")
    user_input = gr.Textbox(label="Ваш вопрос", placeholder="Введите сообщение...")
    send_btn = gr.Button("Отправить")
    send_btn.click(fn=chat_with_model, inputs=[user_input, chatbot], outputs=[user_input, chatbot])

if __name__ == "__main__":
    actualChat.launch(server_name="0.0.0.0", server_port=8000)