import asyncio

async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    print("Starting LLM generation...")
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
        print("LLM generation completed")
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

async def decide(client, query, tools_description):
    # We are passing in the client to not to instantiate one after every iteration, but it can be instantiated here as well 
    system_prompt = f"""You are a math agent solving problems in iterations. You have access to various mathematical tools.

    Available tools:
    {tools_description}

    You must respond with EXACTLY ONE line in one of these formats (no additional text):
    1. For function calls:
    FUNCTION_CALL: function_name|param1|param2|...
    
    2. when you are done:
    DONE!!

    Important:
    - When a function returns multiple values, you need to process all of them
    - Only give DONE!! when you have completed all necessary calculations and performed all necessary actions
    - Do not repeat function calls with the same parameters

    Examples:
    - FUNCTION_CALL: add|5|3
    - FUNCTION_CALL: strings_to_chars_to_int|INDIA
    - FUNCTION_CALL: create_and_open_keynote_presentation|
    - FUNCTION_CALL: add_rectangle_in_keynote_presentation|
    - FUNCTION_CALL: add_text_in_keynote_presentation|42
    - DONE!!

    DO NOT include any explanations or additional text.
    Your entire response should be a single line starting with either FUNCTION_CALL: or DONE!!"""

    print("Preparing to generate LLM response...")
    prompt = f"{system_prompt}\n\nQuery: {query}"

    response = await generate_with_timeout(client, prompt)
    response_text = response.text.strip()
    print(f"LLM Response: {response_text}")
    
    # Find the FUNCTION_CALL line in the response
    for line in response_text.split('\n'):
        line = line.strip()
        if line.startswith("FUNCTION_CALL:"):
            response_text = line
            break
    
    return response_text

