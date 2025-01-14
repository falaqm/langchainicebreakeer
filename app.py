from dotenv import load_dotenv
from flask import Flask,render_template,request,jsonify
from icebreaker import ice_break_with
load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/process",methods=["POST"])
def process():
    name = request.form["name"]
    summary,profile_pic  = ice_break_with(name)
    return jsonify({
        "summary_and_facts": summary.to_dict(),
        "picture_url": profile_pic
    })

if __name__=="__main__":
    app.run(debug=True)