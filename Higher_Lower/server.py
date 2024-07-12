from flask import Flask, request  # type: ignore
import random


app = Flask(__name__)


@app.route("/")
def start():
    global answer
    answer = random.randint(0, 9)
    return (
        "<h1>Guess the number between 0 and 9</h1>"
        '<img src="https://media.giphy.com/media/oS8QRKMc1SFVNuUMrG/giphy.gif?cid=790b7611ocprvuakuv1g4lz5raya01u42dve59bxe3plzek5&ep=v1_gifs_search&rid=giphy.gif&ct=g" width=400 height=400><br><br>'
        '<form action="/play" method="get"><label for="guess">Your guess:</label><input type="text" id="guess" name="guess"><br><br><input type="submit" value="Submit"></form>'
    )


@app.route("/play")
def play():
    try:
        num = int(request.args.get("guess"))
    except (TypeError, ValueError):
        return (
            '<h1><font color="red">Invalid input. Please enter a number between 0 and 9.</font></h1>'
            '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdzA4emg5NGNrNGhxajJzNDM5bmZhaG1pbG52ejU5Ym50N3RwZDU2biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FY8c5SKwiNf1EtZKGs/giphy.gif" width=400 height=400><br><br>'
            '<form action="/play" method="get"><label for="guess">Your guess:</label><input type="text" id="guess" name="guess"><br><br><input type="submit" value="Submit"></form>'
        )
    if num < answer:
        return (
            '<h1><font color="red">Too low.</h1></font></h1>'
            '<img src="https://media.giphy.com/media/SvEcevmYgdFztW976R/giphy.gif?cid=790b7611fyf46yrr8a34u313vfdilzzmntmzoet7jlkmyi02&ep=v1_gifs_search&rid=giphy.gif&ct=g" width=400 height=400><br><br>'
            '<form action="/play" method="get"><label for="guess">Your guess:</label><input type="text" name="guess"><br><br><input type="submit" value="Submit"></form>'
        )
    elif num > answer:
        return (
            '<h1><font color="purple">Too high.</font></h1>'
            '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnhwcWJ5OXJpbmNsd241NGF4ZDA0MTJsaWt0bmlkdHNhbXdmNXM3YyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xT3JvPQibFu3C/giphy.gif" width=400 height=400><br><br>'
            '<form action="/play" method="get"><label for="guess">Your guess:</label><input type="text" name="guess"><br><br><input type="submit" value="Submit"></form>'
        )
    else:
        return (
            '<h1><font color="green">Correct!</font></h1>'
            '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGwxMjNoc3lkMjh2eDh1dzV1c2s0dm93eTg4M3p5OXhneHB4NmpjbSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3ndAvMC5LFPNMCzq7m/giphy.gif" width=400 height=400>'
            '<br><br><h2><a href="/">Press HERE to play again.</a></h2>'
        )


if __name__ == "__main__":
    app.run()
