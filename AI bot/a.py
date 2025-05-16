from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Danh sách lưu lịch sử hội thoại
messages = [
    {"role": "system", "content": "Ngươi là một tiên hiệp hài hước, xưng hô kiểu 'sư huynh', 'sư đệ', nói chuyện như người trong truyện tiên hiệp tu chân, thường cảm thán như 'ây da', 'thiên địa ơi', 'sư đệ à'."}
]

while True:
    user_input = input("Bạn (sư đệ): ")
    if user_input.lower() in ["exit", "quit"]:
        print("Tạm biệt, sư đệ! Hẹn tái ngộ trên đỉnh Côn Luân!")
        break

    # Thêm câu hỏi vào lịch sử
    messages.append({"role": "user", "content": user_input})

    # Gọi API
    response = client.chat.completions.create(
        model="gemma2:9b",
        messages=messages
    )

    bot_reply = response.choices[0].message.content.strip()

    # In ra câu trả lời ngắn gọn
    print("Sư Huynh Bot:", bot_reply)

    # Lưu câu trả lời vào lịch sử
    messages.append({"role": "assistant", "content": bot_reply})
