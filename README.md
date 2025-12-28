📘 Projet RAG – Traitement intelligent de documents PDF

Ce projet met en œuvre un pipeline RAG (Retrieval-Augmented Generation) permettant d’extraire, structurer et interroger des documents PDF à l’aide de techniques d’OCR, d’indexation sémantique et d’un modèle de langage (LLM).

🎯 Objectif du projet

L’objectif est de concevoir un système capable de :

transformer des documents PDF en données exploitables,

indexer leur contenu de manière sémantique,

permettre une interrogation intelligente via un modèle de langage.

Ce projet s’inscrit dans une démarche d’analyse documentaire et de valorisation automatique de l’information.

🧠 Principe général (RAG)

Le pipeline repose sur quatre étapes principales :

OCR : extraction du texte à partir de documents PDF

Structuration : découpage du texte en blocs exploitables (chunks)

Indexation sémantique : transformation des textes en embeddings stockés dans FAISS

Interrogation (RAG) : recherche des passages pertinents + génération de réponse par un LLM (Mistral)

🧰 Technologies utilisées

Python

OCR : Tesseract, OCRmyPDF, Mistral OCR

Indexation vectorielle : FAISS

LLM : Mistral

Gestion du projet : Git / GitHub

📁 Structure du projet
rag_project/
│
├── data/                  # Données traitées (PDF, JSON, index FAISS)
├── scripts/
│   ├── 01_ocr_processing.py
│   ├── 02_embedding_index.py
│   └── 03_rag_query_mistral.py
│
├── requirements.txt
├── service_account.json
└── README.md

⚙️ Installation

Installer les dépendances :

pip install -r requirements.txt


Vérifier que la variable d’environnement est définie :

MISTRAL_API_KEY=your_api_key

▶️ Exécution du pipeline
1️⃣ OCR des documents
python scripts/01_ocr_processing.py

2️⃣ Création des embeddings et indexation
python scripts/02_embedding_index.py

3️⃣ Interrogation du système RAG
python scripts/03_rag_query_mistral.py

🧪 Fonctionnalités principales

Extraction automatique du texte

Gestion de documents volumineux

Recherche sémantique via FAISS

Réponses générées à partir du contenu réel des documents

Compatible avec des questions en français ou en anglais

👤 Auteur

Mariama Amadou Abdou
Projet de stage – 2024/2025

📌 Remarque

Ce dépôt contient uniquement la partie technique du projet.
Les explications détaillées, schémas, choix méthodologiques et analyses figurent dans le rapport associé.
