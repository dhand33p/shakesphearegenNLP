
# import requirements needed
import os

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
import requests

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url + 'static')

app.secret_key = os.urandom(64)

@app.route(f'{base_url}')
def home():
    return render_template('index.html', generated=None)

@app.route(f'{base_url}', methods=['POST'])
def home_post():
    return redirect(url_for('results'))

@app.route(f'{base_url}/results/')
def results():
  if 'data' in session:
      data = session['data']
      return render_template('results.html', generated=data)
  else:
      return render_template('results.html', generated=None)

"""
Finish the two functions below to complete the website's backend.
"""

API_URL = "https://api-inference.huggingface.co/models/dhand33p/gpt2-sonnet-generators"
headers = {"Authorization": "Bearer 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"}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()
    
  """
    Can you write a function that sends a prompt to the Hugging Face endpoint and
    returns the model's output as a string?
  """
	
  
@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
  prompt = request.form["prompt"]
  generated = query(prompt)
  if 'error' in generated:
    generated = 'Model not loading! Try again!'
    return render_template('results.html', generated = generated)
  else:
    return render_template('results.html', generated = generated[0]['generated_text'])
  
  """
    Can you write the code for a page that takes the prompt from a form
    called 'prompt', uses the query function to make an inference with the prompt,
    and returns the output back to an HTML file called results.html?

    If stuck, look back to how you created the backend for the CV module.
    """
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)