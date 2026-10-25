import os
import sqlite3

from flask import Flask, jsonify, request

from auth import utilisateur_connecte

app = Flask(__name__)
DB = "notes.db"


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id INTEGER PRIMARY KEY, etudiant TEXT, module TEXT, note REAL)"
        )
        if con.execute("SELECT COUNT(*) FROM notes").fetchone()[0] == 0:
            con.executemany(
                "INSERT INTO notes (etudiant, module, note) VALUES (?, ?, ?)",
                [("Amina", "DevSecOps", 15.5), ("Youssef", "DevSecOps", 12.0)],
            )


init_db()


@app.route("/")
def accueil():
    return (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
        "<title>Notes des etudiants</title></head><body>"
        "<h1>Consultation des notes</h1>"
        "<p><a href='/notes'>Voir les notes</a></p></body></html>"
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": "1.0"})


@app.route("/notes")
def lister_notes():
    etudiant = request.args.get("etudiant", "")
    with sqlite3.connect(DB) as con:
        rows = con.execute(
            "SELECT id, etudiant, module, note FROM notes WHERE etudiant LIKE ?",
            (f"%{etudiant}%",),
        ).fetchall()
    return jsonify(
        [{"id": r[0], "etudiant": r[1], "module": r[2], "note": r[3]} for r in rows]
    )


# Modification d'une note par l'enseignant du module
@app.route("/notes/<int:note_id>", methods=["PUT"])
def modifier_note(note_id):
    utilisateur = utilisateur_connecte()
    if utilisateur is None:
        return jsonify({"erreur": "Identification requise"}), 401
    if utilisateur["role"] != "enseignant":
        return jsonify({"erreur": "Accès refusé"}), 403

    donnees = request.get_json(silent=True) or {}
    note = donnees.get("note")
    if isinstance(note, bool) or not isinstance(note, (int, float)) or not 0 <= note <= 20:
        return jsonify({"erreur": "La note doit être un nombre entre 0 et 20"}), 400

    try:
        con = sqlite3.connect(DB)
        try:
            ligne = con.execute(
                "SELECT module, note FROM notes WHERE id = ?", (note_id,)
            ).fetchone()
            if ligne is None:
                return jsonify({"erreur": "Note introuvable"}), 404
            module, ancienne_note = ligne
            if module != utilisateur["module"]:
                return jsonify({"erreur": "Accès refusé"}), 403
            con.execute("UPDATE notes SET note = ? WHERE id = ?", (note, note_id))
            con.commit()
        finally:
            con.close()
    except sqlite3.Error:
        app.logger.exception("Erreur lors de la modification de la note %s", note_id)
        return jsonify({"erreur": "Erreur interne"}), 500

    app.logger.info(
        "Note %s modifiée par %s : %s -> %s",
        note_id, utilisateur["nom"], ancienne_note, note,
    )
    return jsonify({"message": "Note modifiée"}), 200


# Démarrage du service des notes
if __name__ == "__main__":
    app.run(host=os.environ.get("APP_HOST", "127.0.0.1"), port=5000)