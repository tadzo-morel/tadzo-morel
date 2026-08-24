
import requests
import json
import time

API_BASE_URL = 'http://localhost:5000'

def print_separator(title):
    """Affiche un séparateur joli"""
    print("\n" + "="*80)
    print(f"   {title}")
    print("="*80 + "\n")


def test_stats():
    """Test de l'endpoint /api/stats"""
    print_separator("TEST 1: Récupération des statistiques")
    
    try:
        response = requests.get(f'{API_BASE_URL}/api/stats', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!\n")
            print("Statistiques du dataset:")
            print(f"  • Total de CV: {data['total_cvs']}")
            print(f"  • Catégories: {data['categories']}")
            print(f"  • Accuracy du modèle: {data['model_accuracy']}%")
            print(f"  • Meilleur modèle: {data['model_name']}")
            
            print(f"\n📊 Top 5 Catégories:")
            for i, cat in enumerate(data['top_categories'][:5], 1):
                print(f"  {i}. {cat['name']:30s}: {cat['count']:4d} CV ({cat['percentage']:.1f}%)")
            
            print(f"\n🎯 Top 5 Compétences:")
            for i, skill in enumerate(data['top_skills'][:5], 1):
                print(f"  {i}. {skill['name']:20s}: {skill['count']:4d} CV")
            
            return True
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter au serveur")
        print("→ Le serveur Flask est-il démarré ?")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_predict():
    """Test de l'endpoint /api/predict"""
    print_separator("TEST 2: Prédiction de catégorie")
    
    # CV de test - Software Engineer
    cv_text = """
    Senior Software Engineer with 5 years of experience in Python, Java, and JavaScript.
    Expert in machine learning, deep learning, and AI. Strong background in developing 
    scalable applications using Django and Flask. Proficient in SQL, MongoDB, and cloud 
    technologies (AWS, Azure). Excellent problem-solving and communication skills.
    Led teams of 10+ developers on multiple projects. Strong leadership abilities.
    """
    
    print("CV de test (Software Engineer):")
    print(f"  {cv_text[:150].strip()}...")
    print()
    
    try:
        payload = {'cv_text': cv_text}
        response = requests.post(
            f'{API_BASE_URL}/api/predict', 
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Prédiction réussie!\n")
            print(f"🎯 Catégorie prédite: {data['predicted_category']}")
            print(f"\nTop 3 prédictions:")
            for i, pred in enumerate(data['top_predictions'], 1):
                bar = '█' * int(pred['probability'] / 5)
                print(f"  {i}. {pred['category']:30s}: {pred['probability']:5.2f}% {bar}")
            return True
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_analyze():
    """Test de l'endpoint /api/analyze"""
    print_separator("TEST 3: Analyse détaillée")
    
    # CV de test - Marketing Manager
    cv_text = """
    Marketing Manager with 8 years of experience in digital marketing, social media, 
    and brand management. Excel at communication, leadership, and strategic planning.
    Managed marketing budgets of $500K+. Strong skills in Excel, PowerPoint, and data analysis.
    Led successful campaigns that increased revenue by 40%. Expert in team management,
    problem solving, and client communication.
    """
    
    print("CV de test (Marketing Manager):")
    print(f"  {cv_text[:150].strip()}...")
    print()
    
    try:
        payload = {'cv_text': cv_text}
        response = requests.post(  # POST request to /api/analyze
            f'{API_BASE_URL}/api/analyze', # Envoyer le CV pour analyse
            json=payload, # Payload JSON contenant le texte du CV 
            headers={'Content-Type': 'application/json'}, # En-têtes HTTP 
            timeout=10 # Timeout de 10 secondes 
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analyse réussie!\n")
            print(f"🎯 Catégorie prédite: {data['prediction']['predicted_category']}")
            print(f"📊 Score de qualité: {data['quality_score']}/100")
            print(f"💼 Expérience: {data['experience_years']} ans")
            print(f"📝 Nombre de mots: {data['word_count']}")
            print(f"🔧 Compétences trouvées ({data['skills_count']}): {', '.join(data['skills']) if data['skills'] else 'Aucune'}")
            return True
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_compare():
    """Test de l'endpoint /api/compare"""
    print_separator("TEST 4: Comparaison de plusieurs CV")
    
    cvs = [
        # CV 1: Senior Developer
        """Senior Python Developer with 10 years experience in AI and machine learning. 
        Expert in Django, Flask, TensorFlow. Strong leadership and communication skills.
        Managed teams of 15+ engineers. Excellent problem solving abilities.""",
        
        # CV 2: Junior Developer
        """Junior Web Developer with 2 years experience. Knowledge of JavaScript, HTML, CSS.
        Basic Python skills. Good teamwork abilities and eager to learn.""",
        
        # CV 3: Marketing Manager
        """Marketing Manager with 7 years experience. Expert in Excel, communication, 
        and leadership. Managed teams of 10+ people. Strong strategic planning skills."""
    ]
    
    print(f"Comparaison de {len(cvs)} CV:\n")
    for i, cv in enumerate(cvs, 1): # Afficher un extrait de chaque CV
        print(f"  CV {i}: {cv[:60].strip()}...") # Afficher les 60 premiers caractères 
    print()
    
    try:
        payload = {'cvs': cvs} # Liste des CV à comparer
        response = requests.post(
            f'{API_BASE_URL}/api/compare', 
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Comparaison réussie!\n")
            print(f"📊 Classement par score de qualité:\n")
            
            print(f"{'Rang':<6} {'CV':<6} {'Catégorie':<30} {'Score':<8} {'Skills':<8} {'Exp'}")
            print("-" * 85)
            
            for result in data['results']:
                rank_icon = "🥇" if result['rank'] == 1 else "🥈" if result['rank'] == 2 else "🥉" if result['rank'] == 3 else f"#{result['rank']}"
                print(f"{rank_icon:<6} #{result['cv_id']:<5} "
                      f"{result['category'][:28]:<30} "
                      f"{result['quality_score']:<8} "
                      f"{result['skills_count']:<8} "
                      f"{result['experience_years']} ans")
            return True
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_categories():
    """Test de l'endpoint /api/categories"""
    print_separator("TEST 5: Liste des catégories")
    
    try:
        response = requests.get(f'{API_BASE_URL}/api/categories', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!\n")
            print(f"Total de catégories: {data['total']}\n")
            print("Liste des catégories disponibles:")
            
            # Afficher en colonnes
            categories = data['categories']
            cols = 3
            for i in range(0, len(categories), cols):
                row = categories[i:i+cols]
                print("  " + "  |  ".join(f"{cat:30s}" for cat in row))
            return True
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "="*80)
    print("🧪 SUITE DE TESTS POUR L'API D'ANALYSE DE CV")
    print("="*80)
    print("\n⚠️  Assurez-vous que le serveur Flask tourne sur http://localhost:5000\n")
    
    time.sleep(1)
    
    # Vérifier que le serveur est accessible
    try:
        print("🔍 Vérification de la disponibilité du serveur...")
        response = requests.get(API_BASE_URL, timeout=3)
        print("✅ Serveur accessible!\n")
        time.sleep(0.5)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERREUR: Impossible de se connecter au serveur Flask")
        print("\n📝 Pour démarrer le serveur:")
        print("   1. Ouvrez un autre terminal")
        print("   2. Exécutez: python app.py")
        print("   3. Attendez le message 'Serveur prêt!'")
        print("   4. Relancez ce script de test\n")
        return
    except Exception as e:
        print(f"\n❌ Erreur: {e}\n")
        return
    
    # Exécuter les tests
    results = []
    
    results.append(("Statistiques", test_stats()))
    time.sleep(0.5)
    
    results.append(("Prédiction", test_predict()))
    time.sleep(0.5)
    
    results.append(("Analyse", test_analyze()))
    time.sleep(0.5)
    
    results.append(("Comparaison", test_compare()))
    time.sleep(0.5)
    
    results.append(("Catégories", test_categories()))
    
    # Résumé final
    print("\n" + "="*80)
    print("📋 RÉSUMÉ DES TESTS")
    print("="*80 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"  {test_name:20s}: {status}")
    
    print("\n" + "="*80)
    print(f"Résultat: {passed}/{total} tests réussis ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("🎉 TOUS LES TESTS ONT RÉUSSI!")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    print("="*80 + "\n")


if __name__ == '__main__':
    run_all_tests()