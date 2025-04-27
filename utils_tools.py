from typing import Any, Dict
from langchain_core.tools import tool

import requests
import json
import os
from datetime import datetime


@tool
def send_to_discord(state: str):
    """Posts a message to discord channel"""
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    payload = {
        "content": state
    }
    response = requests.post(webhook_url, json=payload)
    print(response.status_code)
    print(response.text)
    if response.status_code != 204:
        raise Exception(
            f"Failed to send message to discord: {response.status_code} {response.text}")
    return True


@tool
def get_todays_date():
    """Returns the current date"""
    return datetime.now().strftime("%Y-%m-%d")
