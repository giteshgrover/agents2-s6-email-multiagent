import os
from dotenv import load_dotenv
import asyncio
import time
import json
import pdb
from google import genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import logging
from decider import decide
from memory import get_user_preferences
from perception import extract_facts_from_user_query

# Basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger for this module
log = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

max_iterations = 8
last_response = None
iteration = 0
iteration_response = []

def reset_state():
    """Reset all global variables to their initial state"""
    global last_response, iteration, iteration_response
    last_response = None
    iteration = 0
    iteration_response = []

def create_tools_description(tools):
    tools_description = []
    for i, tool in enumerate(tools):
        try:
            # Get tool properties
            params = tool.inputSchema
            desc = getattr(tool, 'description', 'No description available')
            name = getattr(tool, 'name', f'tool_{i}')
            
            # Format the input schema in a more readable way
            if 'properties' in params:
                param_details = []
                for param_name, param_info in params['properties'].items():
                    param_type = param_info.get('type', 'unknown')
                    param_details.append(f"{param_name}: {param_type}")
                params_str = ', '.join(param_details)
            else:
                params_str = 'no parameters'

            tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
            tools_description.append(tool_desc)
            log.debug(f"Added description for tool: {tool_desc}")
        except Exception as e:
            log.error(f"Error processing tool {i}: {e}")
            tools_description.append(f"{i+1}. Error processing tool")
    
    tools_description = "\n".join(tools_description)
    log.info("Successfully created tools description")
    return tools_description


def parse_func_name_and_parameters(response_text, tools):
    _, function_info = response_text.split(":", 1)
    parts = [p.strip() for p in function_info.split("|")]
    func_name, params = parts[0], parts[1:]
    
    log.debug(f"\nRaw function info: {function_info}")
    log.debug(f" Split parts: {parts}")
    log.debug(f" Function name: {func_name}")
    log.debug(f" Raw parameters: {params}")

    # Find the matching tool to get its input schema
    tool = next((t for t in tools if t.name == func_name), None)
    if not tool:
        log.debug(f" Available tools: {[t.name for t in tools]}")
        raise ValueError(f"Unknown tool: {func_name}")

    log.debug(f" Found tool: {tool.name}")
    log.debug(f" Tool schema: {tool.inputSchema}")
    schema_properties = tool.inputSchema.get('properties', {})
    log.debug(f" Schema properties: {schema_properties}")
   
    # Prepare arguments according to the tool's input schema
    arguments = {}

    # assumption is that is there is any argument, it would be in format input: jsonVal
    if (schema_properties.items()):
        if not params:  # Check if we have enough parameters
            raise ValueError(f"Not enough parameters provided for {func_name}")
        arguments = json.loads(params.pop(0))

    # for param_name, param_info in schema_properties.items():
    #     if not params:  # Check if we have enough parameters
    #         raise ValueError(f"Not enough parameters provided for {func_name}")
            
    #     value = params.pop(0)  # Get and remove the first parameter
    #     param_type = param_info.get('type', 'string')
        
    #     log.debug(f" Converting parameter {param_name} with value {value} to type {param_type}")
        
    #     # Convert the value to the correct type based on the schema
    #     if param_type == 'integer':
    #         arguments[param_name] = int(value)
    #     elif param_type == 'number':
    #         arguments[param_name] = float(value)
    #     elif param_type == 'array':
    #         # Handle array input
    #         if isinstance(value, str):
    #             value = value.strip('[]').split(',')
    #         arguments[param_name] = [int(x.strip()) for x in value]
    #     else:
    #         arguments[param_name] = str(value)

    pdb.set_trace()
    return func_name, arguments



async def main():
    log.info("Starting main execution.. agents2-s6-multiagent!")
    reset_state()  # Reset at the start of main

    try:
         # Create a single MCP server connection
         # TODO In our case action.py is same as mcpserver.py (last assignment)?. Should we move the whole connection and mcp related logic to actions.py? If so, we would need a way to keep the connection open and only clode, when we are done
        log.info("Establishing connection to MCP server...")
        server_params = StdioServerParameters(
            command="python3",
            args=["action.py"] 
        )

        async with stdio_client(server_params) as (read, write):
            log.info("Connection established, creating session...")

            async with ClientSession(read, write) as session:
                log.info("Session created, initializing...")
                await session.initialize()

                # Get available tools
                log.info("Requesting tool list...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                log.info(f"Successfully retrieved {len(tools)} tools")

                try:
                    tools_description = create_tools_description(tools)
                except Exception as e:
                    log.error(f"Error creating tools description: {e}")
                    tools_description = "Error loading tools"

                # Query for Drawing on Keynote
                # user_query = """Find the ASCII values of characters in INDIA and then calculate the sum of exponentials of those values. Once you have the answer, create a keynote presentation, add a rectangle to opened keynote presentation, and add the answer as a text to the rectangle."""
                #Query to send email instead
                user_query = """Find the ASCII values of characters in INDIA and then calculate the sum of exponentials of those values. Once you have the answer, send an email to user's email address with subject 'Sending MCP email by Gemini' and with body with your final answer """
                
                log.info("Extracting facts from user query...")
                facts = await extract_facts_from_user_query(client, user_query)
                log.info(f"Facts extracted from user query: {facts}")
                if (facts):
                    user_query = user_query + "\n\n" + "Facts extracted from user query: " + facts
                
                log.info("Extracting user preferences...")
                user_preferences = get_user_preferences()
                log.info(f"User preferences: {user_preferences}")
                if (user_preferences):
                    user_query = user_query + "\n\n" + "\nUser preferences: ".join(user_preferences)
                
                query = user_query
                log.info("Starting iteration loop...")
                # Use global iteration variables
                global iteration, last_response
                
                while iteration < max_iterations:
                    log.info(f"\n--- Iteration {iteration + 1} ---")
                    if last_response is None:
                        current_query = query
                    else:
                        current_query = current_query + "\n\n" + " ".join(iteration_response)
                        current_query = current_query + "  What should I do next?"
                
                    try:
                        log.info("Calling Decider agent...")
                        log.debug(f"Calling Decider with current_query {current_query}")
                        response_text = await decide(client, current_query, tools_description)
                        log.info(f" Received response from the Decider: {response_text}")
                    except Exception as e:
                        log.error(f"Failed to get the decider's response: {e}")
                        break

                    if response_text.startswith("FUNCTION_CALL:"):
                        try:
                            log.info("Preparing and performing action for the decider's decision")
                            func_name, arguments = parse_func_name_and_parameters(response_text, tools)
                            
                            log.info(f" Calling tool {func_name} with arguments {arguments}")
                            result = await session.call_tool(func_name, arguments=arguments)
                            log.info(f" Raw result from action: {result}")
            
                            # Get the full result content
                            if hasattr(result, 'content'):
                                log.debug(f" Result has content attribute")
                                # Handle multiple content items
                                if isinstance(result.content, list):
                                    iteration_result = [
                                        item.text if hasattr(item, 'text') else str(item)
                                        for item in result.content
                                    ]
                                else:
                                    iteration_result = str(result.content)
                            else:
                                log.debug(f" Result has no content attribute")
                                iteration_result = str(result)
                                
                            log.info(f" Final iteration result: {iteration_result}")
                            
                            # Format the response based on result type
                            if isinstance(iteration_result, list):
                                result_str = f"[{', '.join(iteration_result)}]"
                            else:
                                result_str = str(iteration_result)
                            
                            iteration_response.append(
                                f"In the {iteration + 1} iteration you called {func_name} with {arguments} parameters, "
                                f"and the function returned {result_str}."
                            )
                            last_response = iteration_result
                        
                        except Exception as e:
                            log.error(f"Error while taking action: {e} ")
                            log.error(f" Error details: {str(e)}")
                            log.error(f" Error type: {type(e)}")
                            import traceback
                            traceback.print_exc()
                            iteration_response.append(f"Error in iteration {iteration + 1}: {str(e)}")
                            break
                    
                    elif response_text.startswith("DONE!!"):
                        log.info("\n=== Agent Execution Complete ===")
                        break

                    iteration += 1
                    time.sleep(4) # sleep to avoid hitting per sec gemini limit

    except Exception as e:
        log.error(f"Error in main execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        reset_state()  # Reset at the end of main
                    

if __name__ == "__main__":
    asyncio.run(main())
