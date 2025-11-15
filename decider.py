import asyncio
import pdb
import logging

# Create a logger for this module
log = logging.getLogger(__name__)

async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    log.info("Starting Decider agent's LLM generation...")
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
        log.info("Decider agent's LLM generation completed")
        return response
    except TimeoutError:
        log.error("Decider agent's LLM generation timed out!")
        raise
    except Exception as e:
        log.error(f"Error in Decider agent's LLM generation: {e}")
        raise

async def decide(client, query, tools_description):
    # We are passing in the client to not to instantiate one after every iteration, but it can be instantiated here as well 
    function_format = "function_name|input_json"
    function_examples = """
    - FUNCTION_CALL: add|{"input":{"a":5,"b":10}}
    - FUNCTION_CALL: strings_to_chars_to_int|{"input":{"string":"INDIA"}}
    - FUNCTION_CALL: create_and_open_keynote_presentation|
    - FUNCTION_CALL: add_rectangle_in_keynote_presentation|
    - FUNCTION_CALL: add_text_in_keynote_presentation|{"input":{"text":"42"}}
    - FUNCTION_CALL: int_list_to_exponential_sum|{"input":{"numbers":[7, 10, 20]}}
    """

    system_prompt = f"""You are a math agent solving problems in iterations. You have access to various mathematical tools.

    Available tools:
    {tools_description}

    You must respond with EXACTLY ONE line in one of these formats (no additional text):
    1. For function calls:
    FUNCTION_CALL: {function_format}
    
    2. when you are done:
    DONE!!

    Important:
    - When a function returns multiple values, you need to process all of them
    - Only give DONE!! when you have completed all necessary calculations and performed all necessary actions
    - Do not repeat function calls with the same parameters

    Examples:
    {function_examples}
    - DONE!!

    DO NOT include any explanations or additional text.
    Your entire response should be a single line starting with either FUNCTION_CALL: or DONE!!"""

    log.info("Preparing to generate LLM response...")
    prompt = f"{system_prompt}\n\nQuery: {query}"
    # pdb.set_trace()

    response = await generate_with_timeout(client, prompt)
    response_text = response.text.strip()
    log.info(f"LLM Response: {response_text}")
    
    # Find the FUNCTION_CALL line in the response
    for line in response_text.split('\n'):
        line = line.strip()
        if line.startswith("FUNCTION_CALL:"):
            response_text = line
            break
    
    return response_text

