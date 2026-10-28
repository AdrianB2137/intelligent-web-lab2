
from flask import Flask, jsonify, request
from recommender import recommend

app = Flask(__name__)


@app.route("/api/recommend")
def api_recommend():
    # Pobranie tytulu filmu
    title = request.args.get("title", "").strip()

    if not title:
        return jsonify({"error": "podaj parametr ?title=..."}), 400

    # Pobranie i sprawdzenie liczby rekomendacji
    raw_n = request.args.get("top_n", "5")

    try:
        n = int(raw_n)
    except ValueError:
        return jsonify({"error": "top_n musi byc liczba od 1 do 10"}), 400

    if not 1 <= n <= 10:
        return jsonify({"error": "top_n musi byc z zakresu 1-10"}), 400

    # Opcjonalny gatunek
    genre = request.args.get("genre", "").strip().lower() or None

    # Wywolanie silnika rekomendacji
    recs = recommend(title, top_n=n, genre=genre)

    if recs is None:
        return jsonify({"error": "nie znam takiego filmu"}), 404

    return jsonify({
        "title": title,
        "count": len(recs),
        "recommendations": recs
    })


if __name__ == "__main__":
    app.run(debug=True)
