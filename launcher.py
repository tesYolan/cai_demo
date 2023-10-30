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
    path_2 = "../meditation-sample-demo"
    sys.path.append(path_2)

    path_3 = "../llm_test_cn"
    sys.path.append(path_3)
    path_4 = "../assistive_chat"
    sys.path.append(path_4)
    module_one = importlib.import_module("assignment_one")
    demo_one = getattr(module_one, "demo")
    module_two = importlib.import_module("assignment_two")
    demo_two = getattr(module_two, "demo")

    module_three = importlib.import_module("meditation")
    demo_three = getattr(module_three, "demo")
    demo_three.queue(concurrency_count=3, api_open=False)

    module_four = importlib.import_module("chinese_task")
    demo_four = getattr(module_four, "demo")
    demo_four.queue(concurrency_count=3, api_open=False)

    module_five = importlib.import_module("assistor_chat")
    demo_five = getattr(module_five, "demo")
    demo_five.queue(concurrency_count=3, api_open=False)

    # add queue processing to each one
    demo.queue(concurrency_count=3, api_open=False)
    demo_one.queue(concurrency_count=3, api_open=False)
    demo_two.queue(concurrency_count=3, api_open=False)
    demo_three.queue(concurrency_count=3, api_open=False)
    demo_four.queue(concurrency_count=3, api_open=False)
    app = gr.mount_gradio_app(app, demo, path="/chat")
    app = gr.mount_gradio_app(app, demo_one, path="/assignment_one")
    app = gr.mount_gradio_app(app, demo_two, path="/assignment_two")
    app = gr.mount_gradio_app(app, demo_three, path="/meditation")
    app = gr.mount_gradio_app(app, demo_four, path="/chinese_llm")
    app = gr.mount_gradio_app(app, demo_five, path="/assistive_chat")
    uvicorn.run(app, host="0.0.0.0", port=10000)