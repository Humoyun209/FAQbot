from attr import dataclass
from environs import Env


@dataclass(frozen=True, slots=True)
class Bot:
    bot_token: str
    admin_id: int


def load_data() -> Bot:
    env = Env()
    env.read_env(None)
    return Bot(bot_token=env('BOT_TOKEN'), 
               admin_id=int(env('ADMIN_ID')))