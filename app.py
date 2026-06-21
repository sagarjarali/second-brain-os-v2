from flask import Flask, request
from translator import translate_to_english, translate_to_kannada
from assistant import FarmerAssistant

app = Flask(__name__)
@app.route('/webhook',methods=['POST'])
def webhook():
    incoming_msg = request.form.get('Body','')
    english_response = translate_to_english(incoming_msg)

    assistant = FarmerAssistant()
    response = assistant.ask_llama(english_response)
    kannada_response = translate_to_kannada(response)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{kannada_response}</Message>
</Response>"""


if __name__ == '__main__':
    app.run(debug=True)


