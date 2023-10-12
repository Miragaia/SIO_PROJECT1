from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def returnHTML():
    return render_template('reg_log.html')      # o flask para detetar as paginas html precisa de ser corrido da root do projeto
                                                # (fora de qqr pasta) e os html têm que estar numa pasta chamada 'templates'
app.run()