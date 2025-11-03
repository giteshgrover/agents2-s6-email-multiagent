# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp.server.lowlevel import Server
from mcp import types
from PIL import Image as PILImage
import math
import sys
import time
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import os
import subprocess
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from pydantic import BaseModel

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#Input & Output Models
class AddInput(BaseModel):
    a: int
    b: int

class AddOutput(BaseModel):
    result: int

class AddListInput(BaseModel):
    l: list[int]

class AddListOutput(BaseModel):
    result: int

class SubtractInput(BaseModel):
    a: int
    b: int

class SubtractOutput(BaseModel):
    result: int

class MultiplyInput(BaseModel):
    a: int
    b: int

class MultiplyOutput(BaseModel):
    result: int

class DivideInput(BaseModel):
    a: int
    b: int

class DivideOutput(BaseModel):
    result: float

class PowerInput(BaseModel):
    a: int
    b: int

class PowerOutput(BaseModel):
    result: int

class SqrtInput(BaseModel):
    a: int

class SqrtOutput(BaseModel):
    result: float

class CbrtInput(BaseModel):
    a: int

class CbrtOutput(BaseModel):
    result: float

class FactorialInput(BaseModel):
    a: int

class FactorialOutput(BaseModel):
    result: int

class LogInput(BaseModel):
    a: int

class LogOutput(BaseModel):
    result: float

class RemainderInput(BaseModel):
    a: int
    b: int

class RemainderOutput(BaseModel):
    result: int

class SinInput(BaseModel):
    a: int

class SinOutput(BaseModel):
    result: float

class CosInput(BaseModel):
    a: int

class CosOutput(BaseModel):
    result: float

class TanInput(BaseModel):
    a: int

class TanOutput(BaseModel):
    result: float

class MineInput(BaseModel):
    a: int
    b: int

class MineOutput(BaseModel):
    result: int

class CreateThumbnailInput(BaseModel):
    image_path: str

class StringsToCharsToIntInput(BaseModel):
    string: str

class StringsToCharsToIntOutput(BaseModel):
    result: list[int]

class IntListToExponentialSumInput(BaseModel):
    numbers: list[int]

class IntListToExponentialSumOutput(BaseModel):
    result: float

class FibonacciNumbersInput(BaseModel):
    n: int

class FibonacciNumbersOutput(BaseModel):
    result: list[int]

class DrawRectangleInput(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int

class DrawRectangleOutput(BaseModel):
    message: str

class AddTextInPaintInput(BaseModel):
    text: str

class AddTextInPaintOutput(BaseModel):
    message: str

class OpenPaintOutput(BaseModel):
    message: str

class CreateOpenKeynotePresentationOutput:
    message: str

class AddRectangleInKeynotePresentationOutput:
    message: str

class AddTextInKeynotePresentationInput(BaseModel):
    text: str

class AddTextInKeynotePresentationOutput(BaseModel):
    message: str

#addition tool
@mcp.tool()
def add(input: AddInput) -> AddOutput:
    """Add two numbers"""
    print("CALLED: add(input: AddInput) -> AddOutput:")
    return AddOutput(result = input.a + input.b)

@mcp.tool()
def add_list(input: AddListInput) -> AddListOutput:
    """Add all numbers in a list"""
    print("CALLED: add_list(input: AddListInput) -> AddListOutput:")
    return AddListOutput(result = sum(input.l))

# subtraction tool
@mcp.tool()
def subtract(input: SubtractInput) -> SubtractOutput:
    """Subtract two numbers"""
    print("CALLED: subtract(input: SubtractInput) -> SubtractOutput:")
    return SubtractOutput(result = int(input.a - input.b))

# multiplication tool
@mcp.tool()
def multiply(input: MultiplyInput) -> MultiplyOutput:
    """Multiply two numbers"""
    print("CALLED: multiply(input: MultiplyInput) -> MultiplyOutput:")
    return MultiplyOutput(result = int(input.a * input.b))

#  division tool
@mcp.tool() 
def divide(input: DivideInput) -> DivideOutput:
    """Divide two numbers"""
    print("CALLED: divide(input: DivideInput) -> DivideOutput:")
    return DivideOutput(result = float(input.a / input.b))

# power tool
@mcp.tool()
def power(input: PowerInput) -> PowerOutput:
    """Power of two numbers"""
    print("CALLED: power(input: PowerInput) -> PowerOutput:")
    return PowerOutput(result = int(input.a ** input.b))

# square root tool
@mcp.tool()
def sqrt(input: SqrtInput) -> SqrtOutput:
    """Square root of a number"""
    print("CALLED: sqrt(input: SqrtInput) -> SqrtOutput:")
    return SqrtOutput(result = float(input.a ** 0.5))

# cube root tool
@mcp.tool()
def cbrt(input: CbrtInput) -> CbrtOutput:
    """Cube root of a number"""
    print("CALLED: cbrt(input: CbrtInput) -> CbrtOutput:")
    return CbrtOutput(result = float(input.a ** (1/3)))

# factorial tool
@mcp.tool()
def factorial(input: FactorialInput) -> FactorialOutput:
    """factorial of a number"""
    print("CALLED: factorial(input: FactorialInput) -> FactorialOutput:")
    return FactorialOutput(result = int(math.factorial(input.a)))

# log tool
@mcp.tool()
def log(input: LogInput) -> LogOutput:
    """log of a number"""
    print("CALLED: log(input: LogInput) -> LogOutput:")
    return LogOutput(result = float(math.log(input.a)))

# remainder tool
@mcp.tool()
def remainder(input: RemainderInput) -> RemainderOutput:
    """remainder of two numbers divison"""
    print("CALLED: remainder(input: RemainderInput) -> RemainderOutput:")
    return RemainderOutput(result = int(input.a % input.b))

# sin tool
@mcp.tool()
def sin(input: SinInput) -> SinOutput:
    """sin of a number"""
    print("CALLED: sin(input: SinInput) -> SinOutput:")
    return SinOutput(result = float(math.sin(input.a)))

# cos tool
@mcp.tool()
def cos(input: CosInput) -> CosOutput:
    """cos of a number"""
    print("CALLED: cos(input: CosInput) -> CosOutput:")
    return CosOutput(result = float(math.cos(input.a)))

# tan tool
@mcp.tool()
def tan(input: TanInput) -> TanOutput:
    """tan of a number"""
    print("CALLED: tan(input: TanInput) -> TanOutput:")
    return TanOutput(result = float(math.tan(input.a)))

# mine tool
@mcp.tool()
def mine(input: MineInput) -> MineOutput:
    """special mining tool"""
    print("CALLED: mine(input: MineInput) -> MineOutput:")
    return MineOutput(result = int(input.a - input.b - input.b))

@mcp.tool()
def create_thumbnail(input: CreateThumbnailInput) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(input: CreateThumbnailInput) -> Image:")
    img = PILImage.open(input.image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(input: StringsToCharsToIntInput) -> StringsToCharsToIntOutput:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(input: StringsToCharsToIntInput) -> StringsToCharsToIntOutput:")
    return StringsToCharsToIntOutput(result = [int(ord(char)) for char in input.string])

@mcp.tool()
def int_list_to_exponential_sum(input: IntListToExponentialSumInput) -> IntListToExponentialSumOutput:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(input: IntListToExponentialSumInput) -> IntListToExponentialSumOutput:")
    return IntListToExponentialSumOutput(result = sum(math.exp(i) for i in input.numbers))

@mcp.tool()
def fibonacci_numbers(input: FibonacciNumbersInput) -> FibonacciNumbersOutput:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(input: FibonacciNumbersInput) -> FibonacciNumbersOutput:")
    if input.n <= 0:
        return FibonacciNumbersOutput(result = [])
    fib_sequence = [0, 1]
    for _ in range(2, input.n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return FibonacciNumbersOutput(result = fib_sequence[:input.n])

@mcp.tool()
def create_and_open_keynote_presentation() -> None:
    """Creates and opens a keynote presentation"""
    print("CALLED: create_and_open_keynote_presentation() -> None:")
    applescript = '''
    tell application "Keynote"
        activate
        if not (exists document 1) then
            set thisDoc to make new document with properties {document theme:theme "White"}
        end if
        tell the front document
            set thisSlide to slide 1
            -- Set slide layout to blank
            set base slide of thisSlide to master slide "Blank" of thisDoc
        end tell
    end tell
    '''
    try:
        result = subprocess.run(["osascript", "-e", applescript], 
                              capture_output=True, text=True, check=True)
        print(f"AppleScript executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"AppleScript execution failed: {e.stderr}")
        raise
    except Exception as e:
        print(f"Unexpected error in AppleScript execution: {e}")
        raise

@mcp.tool()
def add_rectangle_in_keynote_presentation() -> None:
    """Adds a rectangle to an opened keynote presentation"""
    print("CALLED: add_rectangle_in_keynote_presentation() -> None:")
    applescript = '''
    tell application "Keynote"
        activate
        tell the front document
            set thisSlide to slide 1
            tell thisSlide
                set newShape to make new shape with properties {position:{150, 150}, width:300, height:300}
            end tell
        end tell
    end tell
    '''
    try:
        result = subprocess.run(["osascript", "-e", applescript], 
                              capture_output=True, text=True, check=True)
        print(f"AppleScript executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"AppleScript execution failed: {e.stderr}")
        raise
    except Exception as e:
        print(f"Unexpected error in AppleScript execution: {e}")
        raise

@mcp.tool()
def add_text_in_keynote_presentation(input: AddTextInKeynotePresentationInput) -> None:
    """Adds text to an opened keynote presentation"""
    print("CALLED: add_text_in_keynote_presentation(input: AddTextInKeynotePresentationInput) -> None:")
    # Properly escape the text for AppleScript
    escaped_text = input.text.replace('"', '\\"').replace('\\', '\\\\')
    applescript = f'''
    tell application "Keynote"
        activate
        tell the front document
            set thisSlide to slide 1
            tell thisSlide
                set newShape to make new shape with properties {{object text:"{escaped_text}", position:{{150, 150}}, width:200, height:100}}
            end tell
        end tell
    end tell
    '''
    try:
        result = subprocess.run(["osascript", "-e", applescript], 
                              capture_output=True, text=True, check=True)
        print(f"AppleScript executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"AppleScript execution failed: {e.stderr}")
        raise
    except Exception as e:
        print(f"Unexpected error in AppleScript execution: {e}")
        raise

async def draw_rectangle(input: DrawRectangleInput) -> dict:
    """Draw a rectangle in Paint from (x1,y1) to (x2,y2)"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width to adjust coordinates
        primary_width = GetSystemMetrics(0)
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.2)
        
        # Click on the Rectangle tool using the correct coordinates for secondary screen
        paint_window.click_input(coords=(530, 82 ))
        time.sleep(0.2)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Draw rectangle - coordinates should already be relative to the Paint window
        # No need to add primary_width since we're clicking within the Paint window
        canvas.press_mouse_input(coords=(input.x1+2560, input.y1))
        canvas.move_mouse_input(coords=(input.x2+2560, input.y2))
        canvas.release_mouse_input(coords=(input.x2+2560, input.y2))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle drawn from ({input.x1},{input.y1}) to ({input.x2},{input.y2})"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }


async def add_text_in_paint(input: AddTextInPaintInput) -> dict:
    """Add text in Paint"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.5)
        
        # Click on the Rectangle tool
        paint_window.click_input(coords=(528, 92))
        time.sleep(0.5)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Select text tool using keyboard shortcuts
        paint_window.type_keys('t')
        time.sleep(0.1)
        paint_window.type_keys('x')
        time.sleep(0.5)
        
        # Click where to start typing
        canvas.click_input(coords=(810, 533))
        time.sleep(0.5)
        
        # Type the text passed from client
        paint_window.type_keys(input.text)
        time.sleep(0.5)
        
        # Click to exit text mode
        canvas.click_input(coords=(1050, 800))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text:'{input.text}' added successfully"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }


async def open_paint() -> dict:
    """Open Microsoft Paint maximized on secondary monitor"""
    global paint_app
    try:
        paint_app = Application().start('mspaint.exe')
        time.sleep(0.2)
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width
        primary_width = GetSystemMetrics(0)
        
        # First move to secondary monitor without specifying size
        win32gui.SetWindowPos(
            paint_window.handle,
            win32con.HWND_TOP,
            primary_width + 1, 0,  # Position it on secondary monitor
            0, 0,  # Let Windows handle the size
            win32con.SWP_NOSIZE  # Don't change the size
        )
        
        # Now maximize the window
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        time.sleep(0.2)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Paint opened successfully on secondary monitor and maximized"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Paint: {str(e)}"
                )
            ]
        }
# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING THE SERVER AT AMAZING LOCATION")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
