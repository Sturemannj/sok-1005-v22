from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pandas")
def get_pandas():
    return render_template("pandas.html")


@app.route("/pygame")
def get_pygame():
    return render_template("pygame.html")


@app.route("/numpy")
def get_numpy():
    return render_template("numpy.html")


@app.route("/scapy")
def get_scapy():
    return render_template("scapy.html")


@app.route("/scikit")
def get_scikit():
    return render_template("scikit.html")


@app.route("/pyspark")
def get_spark():
    return render_template("spark.html")


@app.route("/matlab")
def get_mat():
    return render_template("lab.html")


if __name__ == "__main__":
    #it runs on any ip address available on the machine
    app.run(debug=True, host="0.0.0.0", port=8080)
