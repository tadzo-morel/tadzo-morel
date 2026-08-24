"""
Script pour vérifier que tout est bien installé
"""

print("Vérification de l'installation...\n")

# Vérifier les bibliothèques
libraries = [
    'numpy', 'pandas', 'sklearn', 'matplotlib', 
    'seaborn', 'wordcloud'
]

missing = []
for lib in libraries:
    try:
        __import__(lib)
        print(f"✓ {lib}")
    except ImportError:
        print(f"✗ {lib} - MANQUANT")
        missing.append(lib)

if missing:
    print(f"\n❌ Bibliothèques manquantes: {', '.join(missing)}")
    print("\nInstalle-les avec:")
    print(f"pip install {' '.join(missing)}")
else:
    print("\n✅ Toutes les bibliothèques sont installées!")
    print("Tu peux commencer à utiliser le système.")