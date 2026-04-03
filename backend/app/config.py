from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://dashboard:password@localhost:5432/market_dashboard"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # KIS API
    kis_app_key: str = ""
    kis_app_secret: str = ""
    kis_account_no: str = ""
    kis_is_real: bool = True

    # Finnhub
    finnhub_api_key: str = ""

    # ECOS
    ecos_api_key: str = ""

    # AI
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # App
    tz: str = "Asia/Seoul"

    @property
    def kis_base_url(self) -> str:
        if self.kis_is_real:
            return "https://openapi.koreainvestment.com:9443"
        return "https://openapivts.koreainvestment.com:29443"


settings = Settings()
