from flask import Flask, request, render_template, json
from rec import recommend
from movDet import get_movDet

app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def get_rec():
      if request.method == "POST":
         name = request.form.get("name")
         l = recommend(name)
      #    result = json.dumps(l)
      #    print(result)
         newList = []
         for i in l:
              s='-'.join([k.lower() for k in i.split(' ')])
              x = get_movDet(str(s[:-1]))
              newList.append(x)
         return render_template("res.html", result=newList)
      else:
         return render_template("form.html")

if __name__ == '__main__':
	app.run(debug=True)
