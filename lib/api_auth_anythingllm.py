import requests

# 🔧 Configuration de l'API AnythingLLM
ANYTHINGLLM_API_URL = "http://localhost:3001/api/v1"
ANYTHINGLLM_API_KEY = "0M6D0DJ-QVDMFQB-KNZMBH3-16F5KXH"  # Remplace par ta vraie API Key

# 🔍 Vérifier l'authentification
def test_auth():
    headers = {"Authorization": f"Bearer {ANYTHINGLLM_API_KEY}"}
    response = requests.get(f"{ANYTHINGLLM_API_URL}/auth", headers=headers)

    try:
        auth_data = response.json()
        print("🔍 Réponse de l'API:", auth_data)

        if response.status_code == 200 and auth_data.get("authenticated") == True:
            print("✅ Authentification réussie ! L'API Key est valide.")
        else:
            print(f"❌ Échec de l'authentification. Réponse : {auth_data}")

    except requests.exceptions.JSONDecodeError:
        print(f"❌ Erreur : la réponse de l'API n'est pas du JSON !\nRéponse brute : {response.text}")

# 🚀 Exécuter le test
if __name__ == "__main__":
    test_auth()
