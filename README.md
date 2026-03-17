## ClickClickClick

### A framework to enable autonomous android and computer use using any LLM (local or remote)

![click3](https://github.com/user-attachments/assets/103afd59-ae29-45d2-9d77-75375b1538a0)

## Demos

### create a draft gmail to rob@gmail.com and ask him if he is free for lunch on coming saturday at 1PM. Congratulate on the baby - write one para.
https://github.com/user-attachments/assets/7cdbebb7-0ac4-4c20-8d67-f3c07cd4ab01

### Can you open the browser at https://www.google.com/maps/ and answer the corresponding task: Find bus stops in Alanson, MI
https://github.com/user-attachments/assets/eb5dc968-206b-422d-aa3c-20c48bac3fed

### start a 3+2 game on lichess
https://github.com/user-attachments/assets/68fc3475-2299-4254-8673-3123356177b5


Currently supporting local models via Ollama (Llama 3.2-vision, qwen3.5:4b), Gemini, GPT 4o. The current code is highly experimental and will evolve in future commits. Please use at your own risk.

The best result currently comes from using GPT 4o/4o-mini as planner and Gemini Pro/Flash as finder.

**Ollama models:** qwen3.5:4b works as planner (slow, basic navigation) but not reliable as finder (poor UI element detection). Use with `--image-quality=45` for better performance.

![model recommendations](https://github.com/user-attachments/assets/355865f9-704b-483c-a23b-5dc9be54aeda)

#### How to install

Clone the repository and navigate into the project directory:

```sh
git clone https://github.com/yourusername/clickclickclick
cd clickclickclick
```

It is recommended to create a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the dependencies:

```sh
pip install -r requirements.txt
```


#### How to use

Put your model specific settings in config/models.yaml and export the keys specified in the yaml file.

## As CLI tool

Install the tool

```sh
pip install <repo-whl>
```

```sh
./click3 run open google.com in browser
```


### Setup

Before running any tasks, you need to configure your planner and finder models using the `setup` command:

```sh
python main.py setup
```

You will be prompted to choose the planner and finder models and provide any necessary API keys.

### Running Tasks

To execute a task, use the `run` command. The basic usage is:

```sh
pip install <repo-whl>
```

```sh
./click3 run <task-prompt>
```

#### Options

- `--platform`: Specifies the platform to use, either `android` or `osx`. Default is `android`.

  ```sh
  python main.py run "example task" --platform=osx
  ```

- `--planner-model`: Specifies the planner model to use, either `openai`, `gemini`, or `ollama`. Default is `openai`.

  ```sh
  python main.py run "example task" --planner-model=gemini
  ```

- `--finder-model`: Specifies the finder model to use, either `openai`, `gemini`, or `ollama`. Default is `gemini`.

  ```sh
  python main.py run "example task" --finder-model=ollama
  ```

- `--image-quality`: Image quality percentage (1-100). Lower values reduce image size for faster processing. Default is `100`.

  ```sh
  python main.py run "example task" --image-quality=45
  ```

### Example

```sh
python main.py run "Open Google news" --platform=android --planner-model=openai --finder-model=gemini
```

With local ollama model and reduced image quality:

```sh
python main.py run "Open Reddit" --platform=android --planner-model=ollama --finder-model=gemini --image-quality=45
```

## Use as an API

### POST /execute

#### Description:
This endpoint executes a task based on the provided task prompt, platform, planner model, and finder model.

#### Request Body:
- `task_prompt` (string): The prompt for the task that needs to be executed.
- `platform` (string, optional): The platform on which the task is to be executed. Default is "android". Supported platforms: "android", "osx".
- `planner_model` (string, optional): The planner model to be used for planning the task. Default is "openai". Supported models: "openai", "gemini", "ollama".
- `finder_model` (string, optional): The finder model to be used for finding elements to interact with. Default is "gemini". Supported models: "gemini", "openai", "ollama".
- `image_quality` (integer, optional): Image quality percentage (1-100). Lower values reduce processing time. Default is 100.

#### Response:
- `200 OK`:
  - `result` (object): The result of the task execution.
- `400 Bad Request`:
  - `detail` (string): Description of why the request is invalid (e.g., unsupported platform, unsupported planner model, unsupported finder model).
- `500 Internal Server Error`:
  - `detail` (string): Description of the error that occurred during task execution.

#### Example Request:
```bash
curl -X POST "http://localhost:8000/execute" -H "Content-Type: application/json" -d '{
  "task_prompt": "Open uber app",
  "platform": "android",
  "planner_model": "gemini",
  "finder_model": "openai"
}'
```

#### Example Response:
```json
{
  "result": {
    "status": "success",
    "data": {
      // actual task execution result
    }
  }
}
```

#### Prerequisites

This project needs adb to be installed on your local machine where the code is being executed.

#### Project structure


#### How to contribute

Contributions are welcome! Please open an issue or submit a pull request.


#### Things to do

Three components-

1. Planner
2. Finder
3. Executor


pip install -r requirements.txt

uvicorn api:app --reload

curl -X POST "http://127.0.0.1:8000/execute" -H "Content-Type: application/json" -d '{
    "task_prompt": "Open Safari"
}'



Pre-commit -


pre-commit install
pre-commit autoupdate

pre-commit run --all-files


## License

This project is licensed under the MIT License. See the LICENSE file for details.