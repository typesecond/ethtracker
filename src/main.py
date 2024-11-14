import websocket
import json
import time
from datetime import datetime

# Enable debug messages if you want to see connection details
# websocket.enableTrace(True)

def on_message(ws, message):
    """Called when a new message arrives from the websocket"""
    try:
        data = json.loads(message)
        
        # Extract relevant information
        price = float(data['p'])  # Price
        quantity = float(data['q'])  # Quantity
        timestamp = datetime.fromtimestamp(data['T'] / 1000)  # Convert milliseconds to datetime
        
        # Determine which symbol we're processing
        symbol = data['s'].upper()  # ETHUSDT or SOLUSDT
        base_currency = symbol.replace('USDT', '')  # ETH or SOL
        
        print(f"Time: {timestamp}, {base_currency} Price: ${price:,.2f}, Quantity: {quantity:.4f}")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Raw message: {message}")
    except Exception as e:
        print(f"Processing Error: {e}")
        print(f"Raw message: {message}")

def on_error(ws, error):
    """Called when a websocket error occurs"""
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Called when the websocket connection closes"""
    print("WebSocket Connection Closed")

def on_open(ws):
    """Called when the websocket connection opens"""
    print("WebSocket Connection Opened")
    
    # Subscribe to BTC-USDT, ETH-USDT and SOL-USDT streams
    subscription_message = {
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@trade",
            "ethusdt@trade",
            "solusdt@trade"
        ],
        "id": 1
    }
    ws.send(json.dumps(subscription_message))

def main():
    # Use Binance.US WebSocket URL instead
    websocket_url = "wss://stream.binance.us:9443/ws"
    
    # Create a WebSocket connection with our callback functions
    ws = websocket.WebSocketApp(
        websocket_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    
    # Start the WebSocket connection
    ws.run_forever()

if __name__ == "__main__":
    main()