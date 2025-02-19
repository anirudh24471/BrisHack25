from flask import Flask, render_template, jsonify
import random
import pandas as pd

app = Flask(__name__)

# Predefined circle positions
circle_positions = [[590, 800], [350, 400], [1100, 550], [210, 120], [0, 0]]

@app.route("/")
def home():
    return render_template("index.html", circles=circle_positions)

@app.route("/get_sizes")
def get_sizes():

    data = pd.read_csv("people_count.csv")
    get_size_latest = data.shape[0]
    size_one = int(data.iloc[get_size_latest-1, 1])

    # Generate random sizes (0-40)
    circle_sizes = [0,size_one+10,0,0,0]
    
    # Determine colors based on size (Red if >30, else Green)
    circle_colors = ["green" if size <= 20 else "red" for size in circle_sizes]

    return jsonify(sizes=circle_sizes, colors=circle_colors)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000,debug=True)
