from aiogram import Router
from bot_states import PokurimStates

router = Router()


@router.message(
    PokurimStates.idle
)
async def passad():
    pass
