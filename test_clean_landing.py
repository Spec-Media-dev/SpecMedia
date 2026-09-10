import subprocess, time, json, urllib.request, asyncio, base64, os
import websockets

async def test_clean():
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    proc = subprocess.Popen([
        chrome_path,
        '--headless=new',
        '--remote-debugging-port=9222',
        '--no-first-run',
        '--no-default-browser-check',
        '--user-data-dir=C:/Users/acer/Desktop/specmedia/.chrome_debug_temp'
    ])
    time.sleep(2)
    try:
        with urllib.request.urlopen('http://127.0.0.1:9222/json/list') as resp:
            targets = json.loads(resp.read())
            ws_url = targets[0]['webSocketDebuggerUrl']

        async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
            await ws.send(json.dumps({"id": 3, "method": "Log.enable"}))

            file_url = "file:///" + os.path.abspath("clean_landing.html").replace("\\", "/")
            print("Testing URL:", file_url)

            # Navigate
            await ws.send(json.dumps({"id": 4, "method": "Page.navigate", "params": {"url": file_url}}))

            errors = []
            console_logs = []
            
            t0 = time.time()
            while time.time() - t0 < 4:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                    data = json.loads(msg)
                    method = data.get("method")
                    if method == "Runtime.consoleAPICalled":
                        args = [str(a.get("value", a.get("description"))) for a in data["params"].get("args", [])]
                        console_logs.append((data["params"]["type"], " ".join(args)))
                    elif method == "Runtime.exceptionThrown":
                        errors.append(data["params"]["exceptionDetails"])
                except asyncio.TimeoutError:
                    pass

            print(f"Initial load: {len(console_logs)} console logs, {len(errors)} exceptions")
            for e in errors:
                print("EXCEPTION:", e)

            # Screenshot initial
            await ws.send(json.dumps({"id": 10, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
            resp = await ws.recv()
            data = json.loads(resp)
            if "result" in data and "data" in data["result"]:
                with open("screenshot_clean_initial.png", "wb") as f:
                    f.write(base64.b64decode(data["result"]["data"]))
                print("Saved screenshot_clean_initial.png")

            # Now RELOAD
            print("\nTriggering RELOAD...")
            errors_reload = []
            await ws.send(json.dumps({"id": 11, "method": "Page.reload"}))

            t0 = time.time()
            while time.time() - t0 < 4:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                    data = json.loads(msg)
                    method = data.get("method")
                    if method == "Runtime.exceptionThrown":
                        errors_reload.append(data["params"]["exceptionDetails"])
                except asyncio.TimeoutError:
                    pass

            print(f"Reload: {len(errors_reload)} exceptions")
            for e in errors_reload:
                print("RELOAD EXCEPTION:", e)

            # Screenshot after reload
            await ws.send(json.dumps({"id": 12, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
            resp = await ws.recv()
            data = json.loads(resp)
            if "result" in data and "data" in data["result"]:
                with open("screenshot_clean_reload.png", "wb") as f:
                    f.write(base64.b64decode(data["result"]["data"]))
                print("Saved screenshot_clean_reload.png")

            # Check DOM
            await ws.send(json.dumps({
                "id": 13,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": "({ hasThumbnail: !!document.getElementById('__bundler_thumbnail'), hasUnpacking: !!document.getElementById('__bundler_loading'), h1: document.querySelector('h1')?.textContent, canvasCount: document.querySelectorAll('canvas').length })",
                    "returnByValue": True
                }
            }))
            resp = await ws.recv()
            data = json.loads(resp)
            print("Clean DOM check:", data.get("result", {}).get("result", {}).get("value"))

    finally:
        proc.terminate()

asyncio.run(test_clean())
