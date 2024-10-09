from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
   return "Hello. I am alive!"



def keep_alive():
   t = Thread(target=run)
   t.start()
   
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
