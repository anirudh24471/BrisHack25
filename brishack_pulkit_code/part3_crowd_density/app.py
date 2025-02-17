from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Predefined circle positions
circle_positions = [[590, 600], [250, 370], [1100, 550], [210, 120], [0, 0]]

@app.route("/")
def home():
    return render_template("index.html", circles=circle_positions)

@app.route("/get_sizes")
def get_sizes():
    # Generate random sizes (0-40)
    circle_sizes = [random.randint(0, 40) for _ in range(len(circle_positions))]
    
    # Determine colors based on size (Red if >30, else Green)
    circle_colors = ["green" if size <= 30 else "red" for size in circle_sizes]

    return jsonify(sizes=circle_sizes, colors=circle_colors)

if __name__ == "__main__":
    app.run(debug=True)
