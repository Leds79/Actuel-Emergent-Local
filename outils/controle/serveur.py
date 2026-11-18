# -*- coding: utf-8 -*-
"""Serveur local de contrôle : sert le dépôt à la racine, et ce dossier d'outils sous /__o/.

Usage : python outils/controle/serveur.py [port]      (8765 par défaut)

Les autres outils de ce dossier le lancent eux-mêmes s'il ne tourne pas.
"""
import http.server
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(os.path.dirname(ICI))


class Service(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        propre = path.split("?", 1)[0].split("#", 1)[0]
        if propre.startswith("/__o/"):
            return os.path.join(ICI, os.path.basename(propre))
        # ce qui n'est pas publié n'est pas servi non plus : l'historique git et le dossier privé
        if propre.lstrip("/").split("/", 1)[0].lower() in (".git", "prive"):
            return os.path.join(ICI, "absent")
        self.directory = DEPOT
        return super().translate_path(path)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print("Site servi sur http://127.0.0.1:%d/ (Ctrl+C pour arrêter)" % port, flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Service).serve_forever()
