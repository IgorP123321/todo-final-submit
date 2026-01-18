# Minimalistyczny Menedżer Zadań (Full-Stack Python App)

Projekt aplikacji typu To-Do stworzony w ramach zaliczenia, łączący nowoczesny backend w Pythonie z przejrzystym interfejsem frontendowym.

## 🏗️ Struktura Projektu
Aplikacja została podzielona na moduły zgodnie z najlepszymi praktykami:
- `main.py` - Serwer backendowy FastAPI z logiką bazy danych.
- `/js` - Logika frontendu (komunikacja z API, obsługa DOM).
- `/css` - Style wizualne aplikacji.
- `index.html` - Główny widok aplikacji.

## 🛠️ Stos Technologiczny
* **Backend:** Python + FastAPI
* **Baza danych:** SQLite + SQLAlchemy (Mapowanie obiektowo-relacyjne)
* **Uwierzytelnianie:** Bezpieczne haszowanie haseł (PBKDF2)
* **Frontend:** Vanilla JavaScript, CSS3, HTML5

## ✨ Kluczowe Funkcjonalności
* **Zarządzanie Użytkownikami:** Rejestracja (login + email) oraz logowanie.
* **Prywatność:** Każdy użytkownik zarządza wyłącznie własną listą zadań.
* **Operacje CRUD:** Dodawanie, wyświetlanie oraz usuwanie zadań bezpośrednio w bazie danych.
* **Persystencja danych:** Dzięki SQLite dane nie znikają po zamknięciu serwera.

## 🚦 Jak uruchomić projekt?

1. **Instalacja bibliotek:**
   Upewnij się, że masz Pythona, a następnie zainstaluj zależności:
   ```bash
   pip install fastapi uvicorn sqlalchemy passlib cryptography
