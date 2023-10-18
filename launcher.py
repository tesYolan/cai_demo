from character import demo
import importlib
from fastapi import FastAPI
import gradio as gr

import sys
app = FastAPI(port=10000)
@app.get("/")
def read_main():
    return {"message": "Server is up. Navigate to /chat to use chat"}

if __name__ == '__main__':
    import uvicorn 
    path = "../aifordesign_firstassignment"
    funcs = ["assignment_one", "assignment_two"]
    sys.path.append(path)
    module_one = importlib.import_module("assignment_one")
    demo_one = getattr(module_one, "demo")
    module_two = importlib.import_module("assignment_two")
    demo_two = getattr(module_two, "demo")
    demo.queue(concurrency_count=3, api_open=False)

    # add queue processing to each one
    demo.queue(concurrency_count=3, api_open=False)
    demo_one.queue(concurrency_count=3, api_open=False)
    demo_two.queue(concurrency_count=3, api_open=False)
    app = gr.mount_gradio_app(app, demo, path="/chat")
    app = gr.mount_gradio_app(app, demo_one, path="/assignment_one")
    app = gr.mount_gradio_app(app, demo_two, path="/assignment_two")
    uvicorn.run(app, host="0.0.0.0", port=10000)