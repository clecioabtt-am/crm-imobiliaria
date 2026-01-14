from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    APP_NAME: str = "CRM Imobiliária + WhatsApp + IA"
    ENV: str = "dev"
    FRONTEND_ORIGIN: str = "*"  # em produção, ajuste para seu domínio

    # Database
    DATABASE_URL: str = "postgresql://crm_user:crm_pass@localhost:5432/crm_db"

    # Auth/JWT
    JWT_SECRET: str = "CHANGE_ME_SUPER_SECRET"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_MINUTES: int = 60 * 24  # 24h

    # Admin seed (cria usuário admin se não existir)
    ADMIN_EMAIL: str = "admin@imobiliaria.com"
    ADMIN_PASSWORD: str = "Admin@123"
    ADMIN_NAME: str = "Administrador"

    # WhatsApp Cloud API (Meta)
    WHATSAPP_VERIFY_TOKEN: str = "CHANGE_ME_VERIFY_TOKEN"
    WHATSAPP_TOKEN: str = ""  # token do app (permissão whatsapp_business_messaging)
    WHATSAPP_PHONE_NUMBER_ID: str = ""  # phone_number_id
    WHATSAPP_API_VERSION: str = "v20.0"

    # AI
    AI_MODE: str = "rules"  # "rules" | "openai"
    OPENAI_API_KEY: str = ""  # se usar openai
    AI_SYSTEM_PROMPT: str = "Você é um assistente de atendimento de uma imobiliária. Seja objetivo e educado."

settings = Settings()
