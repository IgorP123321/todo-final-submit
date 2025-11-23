# ToDo Application

T# 📝 TODO API - Menedżer Zadań (Python + FastAPI)
**Autor:** [Igor Pawłowski]
**Grupa:** [ININ4 (hybryda)]
**Data:** [23.11.2025]

**Projekt:** Backend REST API dla listy zadań z trwałą pamięcią (JSON).

### Opis projektu
Projekt implementuje kompletny **REST API** (CRUD) dla zarządzania zadaniami. Wszystkie operacje (tworzenie, modyfikacja, usuwanie) są trwałe dzięki zapisowi danych do lokalnego pliku **`tasks.json`**. Projekt zawiera również testy jednostkowe do weryfikacji logiki serwera.

### Technologie
* **Język programowania:** Python
* **Framework:** FastAPI
* **Serwer:** Uvicorn
* **Pamięć:** Plik JSON (`tasks.json`)
* **Testowanie:** Pytest, HTTPX

---

## 🚀 Instalacja i Uruchomienie

### Wymagania
* Python 3.8+

### Krok po kroku

1.  **Przejdź do folderu projektu** (np. `todo-app`):
    ```bash
    cd [nazwa-projektu]
    ```

2.  **Zainstaluj zależności** (w tym środowisko wirtualne, jeśli nie było tworzone):
    ```bash
    python -m pip install fastapi uvicorn 'python-multipart' pytest httpx
    ```

3.  **Uruchom serwer API** (w trybie stabilnym):
    ```bash
    python -m uvicorn main:app
    ```
    Serwer będzie dostępny pod adresem: `http://localhost:8000`

---

## 🔗 Endpointy API (REST)

| Metoda | Endpoint | Opis | Wymagania |
| :--- | :--- | :--- | :--- |
| **GET** | `/health` | Sprawdza status działania API. | Brak |
| **GET** | `/tasks` | Pobiera listę wszystkich zadań. | Brak |
| **POST** | `/tasks` | Tworzy nowe zadanie. | Wymagane pole `title`. |
| **PUT** | `/tasks/{id}` | Modyfikuje istniejące zadanie (np. status `completed`). | Wymaga ID zadania. |
| **DELETE** | `/tasks/{id}` | Usuwa zadanie. | Wymaga ID zadania. |

### Przykład użycia POST (Thunder Client / cURL)

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Testowanie API","description":"Weryfikacja POST i zapisu do pliku"}'