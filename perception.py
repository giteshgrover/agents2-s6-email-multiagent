import asyncio
import pdb
import logging

# Create a logger for this module
log = logging.getLogger(__name__)

async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    log.info("Starting Perception agent's LLM generation...")
    try:
        # Convert the synchronous generate_content call to run in a thread
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            ),
            timeout=timeout
        )
        log.info("Perception agent's LLM generation completed")
        return response
    except TimeoutError:
        log.error("Perception agent's LLM generation timed out!")
        raise
    except Exception as e:
        log.error(f"Error in LLM generation: {e}")
        raise

async def extract_facts_from_user_query(client, user_query):
    system_prompt = f"""You are a fact extraction agent. You are given a user query and you need to extract the facts from the user query. 
    Your response will be fed to the next agent to actually find the answre to the user query. """

    prompt = f"{system_prompt}\n\nQuery: {user_query}"
    response = await generate_with_timeout(client, prompt)
    response_text = response.text.strip()
    log.debug(f"Facts extracted from user query: {response_text}")
    return response_text

