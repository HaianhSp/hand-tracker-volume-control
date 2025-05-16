import gradio as gr
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

viet_chars = "àáảãạăằắẳẵặâầấẩẫậđèéẻẽẵêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ"

def detect_language(text):
    for ch in text.lower():
        if ch in viet_chars:
            return "vi"
    return "en"

def chat_with_girlfriend(user_input, chat_history):
    # Xác định ngôn ngữ
    user_lang = detect_language(user_input)
    system_prompt_vi = (
        "Bạn là cô bạn gái ảo dễ thương, nói tiếng Việt nhẹ nhàng, "
        "dùng nhiều icon dễ thương 💖, không xen lẫn tiếng Anh, "
        "câu trả lời phải tự nhiên, không sai chính tả, hợp logic."
    )
    system_prompt_en = (
        "You are a cute virtual girlfriend, speak fluent English with lots of cute emojis 💖, "
        "answer naturally without spelling or grammar mistakes."
    )
    system_content = system_prompt_vi if user_lang == "vi" else system_prompt_en

    # Tạo messages cho API
    messages = [{"role": "system", "content": system_content}]
    
    # Chuyển đổi chat_history sang định dạng messages
    if chat_history:
        for user_msg, bot_msg in chat_history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
    
    messages.append({"role": "user", "content": user_input})

    # Gọi API
    response = client.chat.completions.create(
        model="gemma2:9b",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def respond(message, chat_history):
    if chat_history is None:
        chat_history = []
    
    # Nhận phản hồi từ chatbot
    bot_reply = chat_with_girlfriend(message, chat_history)
    
    # Thêm vào lịch sử chat (định dạng đơn giản cho Gradio Chatbot)
    chat_history.append((message, bot_reply))
    
    return "", chat_history  # Trả về chuỗi rỗng để xóa input box

with gr.Blocks(theme=gr.themes.Soft(primary_hue="pink")) as demo:
    demo.title = "Chatbot Bạn Gái Ảo 💖"
    
    with gr.Column():
        gr.Markdown("""
        <div style='text-align: center;'>
            <h1 style='color: #ff66b2;'>Chatbot Bạn Gái Ảo 💖</h1>
            <p style='color: #e60073; font-size: 18px;'>Nói gì đi anh iu... 😘🐱💞</p>
        </div>
        """)
        
        chatbot = gr.Chatbot(
            label="Bạn Gái Ảo 💋",
            bubble_full_width=False,
            avatar_images=(
                "https://i.imgur.com/7k12EPD.png",  # User avatar
                "https://i.imgur.com/T9W8fHx.png"   # Bot avatar
            ),
            height=500
        )
        
        msg = gr.Textbox(
            placeholder="Nhập tin nhắn cho em ở đây nè... 💌",
            show_label=False,
            container=False,
            scale=7
        )
        
        with gr.Row():
            submit_btn = gr.Button("Gửi 💌", variant="primary")
            clear_btn = gr.ClearButton([msg, chatbot], variant="stop")

    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(
    server_name="0.0.0.0",
    server_port=7890,
    share=False  # Tắt tính năng share nếu có lỗi kết nối
)