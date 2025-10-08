from redis import Redis
import logging

class RedisManager:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: str = "", username: str = "") -> None:
        try:
            self.redis = Redis(host=host, port=port, db=db, password=password, username=username)
        except Exception as e:
            logging.error(e)
            pass

    def set_user_explained(self, user_id: int, explained: str) -> None:
        try:
            self.redis.hset(name=str(user_id), key="explained_symptom", value=explained)
        except Exception as e:
            logging.error(e)
            pass

    def set_user_symptoms(self, user_id: int, symptom_key: str, user_choose: str) -> None:
        try:
            self.redis.hset(name=str(user_id), key=symptom_key, value=user_choose)
        except Exception as e:
            logging.error(e)
            pass

    def get_user_symptoms(self, user_id: int) -> dict:
        try:
            return self.redis.hgetall(str(user_id))
        except Exception as e:
            logging.error(e)
            pass

    def delete_user_if_exists(self, user_id: int) -> None:
        try:
            self.redis.hdel(name=str(user_id))
        except Exception as e:
            logging.error(e)
            pass

    def _get_user_explained(self, user_id: int) -> str:
        try:
            return self.redis.hget(name=str(user_id), key="explained_symptom").decode("utf-8")
        except Exception as e:
            logging.error(e)
            pass