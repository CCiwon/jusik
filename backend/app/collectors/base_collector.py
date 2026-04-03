"""공통 수집기 베이스 클래스."""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0  # seconds

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "BaseCollector":
        self._client = httpx.AsyncClient(timeout=10.0)
        return self

    async def __aexit__(self, *_: Any) -> None:
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        if not self._client:
            raise RuntimeError("Collector not initialized. Use async with.")
        return self._client

    async def get(self, url: str, **kwargs: Any) -> dict:
        last_error: Exception | None = None
        for attempt in range(self.MAX_RETRIES):
            try:
                response = await self.client.get(url, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP {e.response.status_code} from {url} (attempt {attempt+1})")
                last_error = e
                if e.response.status_code in (401, 403, 404):
                    break  # 재시도해도 의미없는 에러
            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.warning(f"Request error for {url} (attempt {attempt+1}): {e}")
                last_error = e

            if attempt < self.MAX_RETRIES - 1:
                await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))

        raise RuntimeError(f"Failed after {self.MAX_RETRIES} attempts: {last_error}")

    @abstractmethod
    async def collect(self) -> Any:
        """데이터를 수집하여 반환."""
        ...
