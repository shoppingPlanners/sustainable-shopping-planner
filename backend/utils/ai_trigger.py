"""
AI Agent trigger utilities
"""

import asyncio
import subprocess
import logging
from config import AI_AGENT_PATH

logger = logging.getLogger(__name__)

async def trigger_ai_rating_calculation(product_id: str):
    """Trigger AI rating calculation in background"""
    try:
        logger.info(f"🤖 Triggering AI rating calculation for product {product_id}")
        
        # Run the AI agent
        process = await asyncio.create_subprocess_exec(
            "python", "app.py", product_id,
            cwd=AI_AGENT_PATH.replace("app.py", ""),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            logger.info(f"✅ AI rating calculation completed for product {product_id}")
            logger.info(f"AI Output: {stdout.decode()}")
        else:
            logger.error(f"❌ AI rating calculation failed: {stderr.decode()}")
            
    except Exception as e:
        logger.error(f"❌ Failed to trigger AI rating calculation: {e}")
