
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Wczytanie filmow z pliku CSV
df = pd.read_csv("movies.csv")
df["overview"] = df["overview"].fillna("")

print("Rozmiar bazy:", df.shape)
print(df.head(3))

# Zamiana opisow filmow na wektory liczb
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])

print("Rozmiar macierzy TF-IDF:", tfidf_matrix.shape)

# Obliczenie podobienstwa miedzy wszystkimi filmami
sim_matrix = cosine_similarity(tfidf_matrix)


def recommend(title, top_n=5, genre=None):
    # Szukanie filmu po tytule
    match = df[df["title"].str.lower() == title.strip().lower()]

    if match.empty:
        return None

    idx = match.index[0]

    # Posortowanie filmow od najbardziej podobnych
    scores = sorted(
        enumerate(sim_matrix[idx]),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for i, score in scores:
        # Nie polecamy filmu, ktory uzytkownik juz wybral
        if i == idx:
            continue

        # Opcjonalny filtr gatunku
        if genre:
            genres = str(df.iloc[i]["genres"]).lower().split("|")
            if genre.lower() not in genres:
                continue

        results.append({
            "title": df.iloc[i]["title"],
            "genres": df.iloc[i]["genres"],
            "rating": round(float(df.iloc[i]["rating"]), 1),
            "score": round(float(score), 3)
        })

        if len(results) >= top_n:
            break

    return results


# Test funkcji po uruchomieniu pliku
if __name__ == "__main__":
    print("\nFilmy podobne do Inception:")
    print(recommend("Inception"))

    print("\nFilmy podobne do The Matrix:")
    print(recommend("The Matrix"))
