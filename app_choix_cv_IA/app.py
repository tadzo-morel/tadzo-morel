# ========================================================================
# APPLICATION WEB COMPLÈTE - BACKEND FLASK
# Système d'analyse de CV avec Dataset intégré
# ========================================================================

from flask import Flask, request, jsonify, render_template_string # Framework web Flask pour Python et gestion des requêtes 
from flask_cors import CORS # Pour gérer les CORS 
import pandas as pd # Pour la manipulation des données
import numpy as np # Pour les opérations numériques
import pickle # Pour sauvegarder et charger les modèles
import os # Pour la gestion des fichiers
from sklearn.feature_extraction.text import TfidfVectorizer # Pour la vectorisation TF-IDF 
from sklearn.preprocessing import LabelEncoder # Pour l'encodage des labels 
from sklearn.ensemble import RandomForestClassifier # Modèle Random Forest 
from sklearn.model_selection import train_test_split # Pour diviser les données en ensembles d'entraînement et de test
import re # Pour le nettoyage du texte 

app = Flask(__name__) # Initialisation de l'application Flask 
CORS(app) # Activer CORS pour toutes les routes

# ========================================================================
# CONFIGURATION
# ========================================================================

DATASET_PATH = 'C:/Users/morel/Desktop/Resume1.csv' # Chemin vers le dataset CSV 
MODELS_DIR = 'models' # Dossier pour sauvegarder les modèles entraînés 
UPLOAD_FOLDER = 'uploads' # Dossier pour les CVs uploadés 

os.makedirs(MODELS_DIR, exist_ok=True) # Crée le dossier des modèles s'il n'existe pas 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)# Crée le dossier des uploads s'il n'existe pas 

# Variables globales
df = None # DataFrame du dataset
vectorizer = None # TF-IDF Vectorizer 
label_encoder = None # Encodeur de labels initialisé au démarrage  avec aucun modèle chargé
best_model = None # Meilleur modèle ML
dataset_stats = None # Statistiques du dataset 


# ========================================================================
# FONCTIONS UTILITAIRES
# ========================================================================

def clean_text(text):
    """Nettoie le texte des CV"""
    text = str(text).lower() # Convertir en minuscules 
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # Supprimer la ponctuation 
    text = re.sub(r'\s+', ' ', text) # Supprimer les espaces multiples 
    return text.strip() # Supprimer les espaces en début/fin 


def load_and_prepare_dataset(): 
    """Charge et prépare le dataset"""
    global df, vectorizer, label_encoder, best_model, dataset_stats # Variables globales
    
    print("Chargement du dataset...") 
    df = pd.read_csv(DATASET_PATH) # Charger le dataset CSV
    
    # Nettoyage
    df['cleaned_text'] = df['Resume_str'].apply(clean_text) # Nettoyer les CVs
    df_clean = df[df['cleaned_text'] != ''].copy() # Supprimer les CVs vides 
    
    # Encodage
    label_encoder = LabelEncoder() # Initialiser l'encodeur de labels
    y = label_encoder.fit_transform(df_clean['Category']) # Encoder les catégories et obtenir y
    
    # Vectorisation
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english') # Initialiser le vectorizer TF-IDF 
    X = vectorizer.fit_transform(df_clean['cleaned_text']) # Vectoriser les CVs et obtenir X entrainement des données
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Entraîner le meilleur modèle (Random Forest)
    best_model = RandomForestClassifier(n_estimators=100 , random_state=42) # Initialiser le modèle Random Forest
    best_model.fit(X_train, y_train)
    
    accuracy = best_model.score(X_test, y_test) # Évaluer la précision sur l'ensemble de test
    
    # Statistiques du dataset
    category_counts = df_clean['Category'].value_counts()
    
    # Extraction des compétences
    skills_keywords = [
        'ai', 'management', 'excel', 'communication', 'leadership',
        'python', 'java', 'javascript', 'sql', 'machine learning'
    ]
    
    skill_counts = {}
    for skill in skills_keywords:
        count = df_clean['cleaned_text'].str.contains(skill, na=False).sum() # Compter les CVs contenant la compétence recherchée
        if count > 0:
            skill_counts[skill] = int(count)
    
    dataset_stats = {
        'total_cvs': len(df_clean),
        'categories': len(label_encoder.classes_),
        'top_categories': [
            {'name': cat, 'count': int(count), 'percentage': round(count/len(df_clean)*100, 2)}
            for cat, count in category_counts.head(10).items()
        ],
        'top_skills': [
            {'name': skill, 'count': count}
            for skill, count in sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ],
        'model_accuracy': round(accuracy * 100, 2),
        'model_name': 'Random Forest'
    }
    
    # Sauvegarder les modèles
    with open(os.path.join(MODELS_DIR, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f) # Sauvegarder le vectorizer
    with open(os.path.join(MODELS_DIR, 'label_encoder.pkl'), 'wb') as f:
        pickle.dump(label_encoder, f) # Sauvegarder l'encodeur de labels
    with open(os.path.join(MODELS_DIR, 'best_model.pkl'), 'wb') as f:
        pickle.dump(best_model, f) # Sauvegarder le meilleur modèle
    
    print(f"✓ Dataset chargé: {len(df_clean)} CV") 
    print(f"✓ Modèle entraîné: Accuracy {accuracy*100:.2f}%") # Afficher la précision du modèle 02 décimales
    
    return dataset_stats


def predict_cv(cv_text):
    """Prédit la catégorie d'un CV"""
    if not best_model or not vectorizer or not label_encoder:
        return None
    
    # Nettoyer et vectoriser
    cleaned = clean_text(cv_text)
    vectorized = vectorizer.transform([cleaned])
    
    # Prédire
    prediction = best_model.predict(vectorized)[0] # Obtenir la prédiction
    category = label_encoder.inverse_transform([prediction])[0] # Décoder la catégorie prédite
    
    # Probabilités
    try:
        probas = best_model.predict_proba(vectorized)[0] # Obtenir les probabilités pour chaque catégorie
        top_indices = probas.argsort()[-3:][::-1] # Indices des 3 meilleures prédictions
        top_categories = [
            {
                'category': label_encoder.inverse_transform([i])[0],
                'probability': round(float(probas[i]) * 100, 2)
            }
            for i in top_indices
        ]
    except:
        top_categories = [{'category': category, 'probability': 100.0}]
    
    return {
        'predicted_category': category,
        'top_predictions': top_categories
    }


def analyze_cv_detailed(cv_text):
    """Analyse détaillée d'un CV"""
    # Prédiction
    prediction = predict_cv(cv_text)
    
    if not prediction:
        return None
    
    # Extraction de compétences
    skills_keywords = [
        'ai', 'management', 'excel', 'communication', 'leadership',
        'python', 'java', 'javascript', 'sql', 'machine learning',
        'teamwork', 'problem solving', 'marketing', 'sales'
    ]
    
    cv_lower = cv_text.lower() # Convertir en minuscules pour la recherche de compétences 
    found_skills = [skill for skill in skills_keywords if skill in cv_lower] # Trouver les compétences présentes dans le CV    
    # Estimation de l'expérience
    experience_patterns = [
        r'(\d+)\s*(?:ans?|years?)\s*(?:d\')?(?:expérience|experience)',
        r'(\d+)\+?\s*years?'
    ]
    
    years = []
    for pattern in experience_patterns: # Chercher les années d'expérience
        matches = re.findall(pattern, cv_lower) # Trouver toutes les correspondances
        years.extend([int(m) for m in matches]) # Ajouter les années trouvées
    
    experience = max(years) if years else 0
    
    # Analyse du texte
    word_count = len(cv_text.split())
    char_count = len(cv_text)
    
    return {
        'prediction': prediction,
        'skills': found_skills,
        'skills_count': len(found_skills),
        'experience_years': experience,
        'word_count': word_count,
        'char_count': char_count,
        'quality_score': calculate_quality_score(word_count, len(found_skills), experience)
    }


def calculate_quality_score(word_count, skills_count, experience):
    """Calcule un score de qualité du CV"""
    score = 0
    
    # Longueur du CV (max 30 points)
    if 300 <= word_count <= 800:
        score += 30
    elif 200 <= word_count < 300 or 800 < word_count <= 1000:
        score += 20
    else:
        score += 10
    
    # Compétences (max 40 points)
    score += min(skills_count * 5, 40)
    
    # Expérience (max 30 points)
    score += min(experience * 6, 30)
    
    return min(score, 100)


# ========================================================================
# ROUTES API
# ========================================================================

@app.route('/') # Page d'accueil chemein racine
def home():  
    """Page d'accueil"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Système d'Analyse de CV par IA</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
            }
            h1 {
                color: #667eea;
                text-align: center;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .stat-card {
                background: #f7fafc;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border-left: 4px solid #667eea;
            }
            .stat-value {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }
            .stat-label {
                color: #718096;
                margin-top: 10px;
            }
            .api-docs {
                background: #edf2f7;
                padding: 20px;
                border-radius: 8px;
                margin-top: 30px;
            }
            .endpoint {
                background: white;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
            }
            .method {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 3px;
                color: white;
                font-weight: bold;
                margin-right: 10px;
            }
            .get { background: #48bb78; }
            .post { background: #4299e1; }
            code {
                background: #2d3748;
                color: #68d391;
                padding: 2px 6px;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Système d'Analyse de CV par IA</h1>
            <p style="text-align: center; color: #718096;">
                TPE - Morel Tadzo | Niveau 3 Informatique
            </p>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">""" + str(dataset_stats['total_cvs'] if dataset_stats else 0) + """</div> # Nombre total de CVs
                    <div class="stat-label">CV Analysés</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">""" + str(dataset_stats['categories'] if dataset_stats else 0) + """</div>
                    <div class="stat-label">Catégories</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">""" + str(dataset_stats['model_accuracy'] if dataset_stats else 0) + """%</div>
                    <div class="stat-label">Précision du Modèle</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">Random Forest</div>
                    <div class="stat-label">Meilleur Algorithme</div>
                </div>
            </div>
            
            <div class="api-docs">
                <h2>📡 API Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <code>/api/stats</code>
                    <p>Récupère les statistiques du dataset</p>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <code>/api/predict</code>
                    <p>Prédit la catégorie d'un CV</p>
                    <pre>Body: { "cv_text": "votre CV ici..." }</pre>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <code>/api/analyze</code>
                    <p>Analyse détaillée d'un CV (catégorie + compétences + score)</p>
                    <pre>Body: { "cv_text": "votre CV ici..." }</pre>
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <code>/api/compare</code>
                    <p>Compare plusieurs CV et les classe</p>
                    <pre>Body: { "cvs": ["cv1", "cv2", "cv3"] }</pre>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px; color: #718096;">
                <p>✨ Application développée avec Flask + Machine Learning</p>
                <p>Algorithmes: Random Forest, SVM, Logistic Regression, Naive Bayes</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html) # Rendre le HTML 


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retourne les statistiques du dataset"""
    if not dataset_stats:
        return jsonify({'error': 'Dataset non chargé'}), 500
    
    return jsonify(dataset_stats)


@app.route('/api/predict', methods=['POST'])
def predict():
    """Prédit la catégorie d'un CV"""
    data = request.json
    cv_text = data.get('cv_text')
    
    if not cv_text:
        return jsonify({'error': 'cv_text manquant'}), 400
    
    result = predict_cv(cv_text)
    
    if not result:
        return jsonify({'error': 'Modèle non disponible'}), 500
    
    return jsonify(result)


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyse détaillée d'un CV"""
    data = request.json
    cv_text = data.get('cv_text')
    
    if not cv_text:
        return jsonify({'error': 'cv_text manquant'}), 400
    
    result = analyze_cv_detailed(cv_text)
    
    if not result:
        return jsonify({'error': 'Erreur d\'analyse'}), 500
    
    return jsonify(result)


@app.route('/api/compare', methods=['POST'])
def compare():
    """Compare plusieurs CV"""
    data = request.json
    cvs = data.get('cvs', [])
    
    if not cvs or len(cvs) == 0:
        return jsonify({'error': 'Liste de CV vide'}), 400
    
    results = []
    
    for idx, cv_text in enumerate(cvs):
        analysis = analyze_cv_detailed(cv_text)
        if analysis:
            results.append({
                'cv_id': idx + 1,
                'category': analysis['prediction']['predicted_category'],
                'confidence': analysis['prediction']['top_predictions'][0]['probability'],
                'quality_score': analysis['quality_score'],
                'skills_count': analysis['skills_count'],
                'experience_years': analysis['experience_years']
            })
    
    # Trier par score de qualité
    results.sort(key=lambda x: x['quality_score'], reverse=True)
    
    # Ajouter le rang
    for idx, result in enumerate(results, 1):
        result['rank'] = idx
    
    return jsonify({
        'total_cvs': len(results),
        'results': results
    })


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Liste toutes les catégories disponibles"""
    if not label_encoder:
        return jsonify({'error': 'Modèle non chargé'}), 500
    
    categories = label_encoder.classes_.tolist()
    
    return jsonify({
        'total': len(categories),
        'categories': categories
    })


# ========================================================================
# DÉMARRAGE
# ========================================================================

if __name__ == '__main__':
    print("="*80)
    print("DÉMARRAGE DU SERVEUR")
    print("="*80)
    
    # Charger le dataset
    try:
        load_and_prepare_dataset()
        print("\n✅ Serveur prêt!")
        print("="*80)
        print("\nAccédez à l'application:")
        print("  → http://localhost:5000")
        print("\nAPI disponibles:")
        print("  → GET  http://localhost:5000/api/stats")
        print("  → POST http://localhost:5000/api/predict")
        print("  → POST http://localhost:5000/api/analyze")
        print("  → POST http://localhost:5000/api/compare")
        print("="*80)
    except Exception as e:
        print(f"\n❌ Erreur lors du chargement: {e}")
        print("Vérifiez le chemin du fichier CSV")
    
    app.run(debug=True, host='0.0.0.0', port=5000)