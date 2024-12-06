from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# Base de données simulée
fake_users_db: Dict[str, str] = {}
user_preferences_db: Dict[str, Dict[str, str]] = {}

# Modèle pour les préférences
class Preferences(BaseModel):
    theme: str
    notifications: bool

# Initialiser FastAPI
app = FastAPI()

# Fonction d'inscription
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    password = context.args[0] if context.args else None

    if username in fake_users_db:
        await update.message.reply_text("Ce nom d'utilisateur est déjà enregistré.")
        return
    
    if password:
        fake_users_db[username] = password  # Stocker le mot de passe (à éviter en production)
        await update.message.reply_text("Inscription réussie !")
    else:
        await update.message.reply_text("Veuillez fournir un mot de passe.")

# Fonction de connexion
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    password = context.args[0] if context.args else None

    if username not in fake_users_db or fake_users_db[username] != password:
        await update.message.reply_text("Identifiants invalides.")
        return
    
    await update.message.reply_text("Connexion réussie !")

# Fonction pour gérer les préférences
async def set_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    
    if username not in fake_users_db:
        await update.message.reply_text("Utilisateur non trouvé. Veuillez vous inscrire d'abord.")
        return
    
    theme = context.args[0] if context.args else "default"
    notifications = True if len(context.args) > 1 and context.args[1].lower() == "true" else False
    
    user_preferences_db[username] = {"theme": theme, "notifications": notifications}
    await update.message.reply_text("Préférences mises à jour.")

# Fonction pour récupérer les préférences
async def get_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    
    preferences = user_preferences_db.get(username)
    
    if preferences:
        await update.message.reply_text(f"Vos préférences : {preferences}")
    else:
        await update.message.reply_text("Aucune préférence trouvée.")

# Configurer le bot Telegram
def main():
    application = ApplicationBuilder().token('YOUR_TELEGRAM_BOT_TOKEN').build()

    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("set_preferences", set_preferences))
    application.add_handler(CommandHandler("get_preferences", get_preferences))

    application.run_polling()

if __name__ == "__main__":
    main()