import click
import os
from clickclickclick.config import get_config
from clickclickclick.planner.task import execute_with_timeout, execute_task
from clickclickclick.executor.osx import MacExecutor
from clickclickclick.executor.android import AndroidExecutor
from clickclickclick.planner.gemini import GeminiPlanner
from clickclickclick.finder.gemini import GeminiFinder
from clickclickclick.planner.openai import ChatGPTPlanner
from clickclickclick.finder.local_ollama import OllamaFinder
from clickclickclick.finder.openai import OpenAIFinder
from clickclickclick.planner.local_ollama import OllamaPlanner


@click.group()
def cli():
    pass


@click.command()
@click.argument("task_prompt", nargs=-1)
@click.option("--platform", default="android", help="The platform to use, 'android' or 'osx'.")
@click.option(
    "--planner-model",
    default="openai",
    help="The planner model to use, 'openai', 'gemini', or 'ollama'.",
)
@click.option(
    "--finder-model",
    default="gemini",
    help="The finder model to use, 'openai', 'gemini', or 'ollama'.",
)
@click.option(
    "--image-quality",
    default=100,
    type=int,
    help="Image quality percentage (1-100). Lower values reduce image size for faster processing.",
)
def run(task_prompt, platform, planner_model, finder_model, image_quality):
    """
    Execute a task with the given TASK_PROMPT using the specified
    platform, planner model, and finder model.
    """
    task_prompt = " ".join(task_prompt)

    c = get_config(platform, planner_model, finder_model)

    if platform == "osx":
        executor = MacExecutor()
    else:
        executor = AndroidExecutor()

    # Set image quality for executor
    executor.image_quality = max(1, min(100, image_quality))

    if planner_model == "openai":
        executor.screenshot_as_base64 = True
        planner = ChatGPTPlanner(c)
    elif planner_model == "gemini":
        executor.screenshot_as_tempfile = True
        planner = GeminiPlanner(c)
    elif planner_model == "ollama":
        executor.screenshot_as_tempfile = True
        planner = OllamaPlanner(c, executor)

    if finder_model == "openai":
        finder = OpenAIFinder(c, executor)
    elif finder_model == "gemini":
        finder = GeminiFinder(c, executor)
    elif finder_model == "ollama":
        finder = OllamaFinder(c, executor)

    if not task_prompt:
        task_prompt = c.SAMPLE_TASK_PROMPT

    result = execute_with_timeout(
        execute_task, c.TASK_TIMEOUT_IN_SECONDS, task_prompt, executor, planner, finder, c
    )

    if result is not None:
        print(result)


@click.command()
def setup():
    """Setup command to configure planner and finder"""
    planner = click.prompt("Choose planner model ('gemini', '4o', or 'ollama')", type=str)

    if planner.lower() == "gemini":
        gemini_api_key = click.prompt("Enter your Gemini API key", hide_input=True)
        os.environ["GEMINI_API_KEY"] = gemini_api_key
    elif planner.lower() == "4o":
        version = click.prompt("Is it OpenAI or Azure version?", type=str)
        if version.lower() == "openai":
            openai_api_key = click.prompt("Enter your OpenAI API key", hide_input=True)
            os.environ["AZURE_OPENAI_API_KEY"] = openai_api_key
            os.environ["OPENAI_API_TYPE"] = "openai"
        elif version.lower() == "azure":
            azure_api_key = click.prompt("Enter your Azure API key", hide_input=True)
            os.environ["AZURE_OPENAI_API_KEY"] = azure_api_key
            azure_model_name = click.prompt("Enter your Azure model name", type=str)
            os.environ["AZURE_OPENAI_MODEL_NAME"] = azure_model_name
            azure_endpoint = click.prompt("Enter your Azure endpoint", type=str)
            os.environ["AZURE_OPENAI_ENDPOINT"] = azure_endpoint
            azure_api_version = click.prompt("Enter your Azure API version", type=str)
            os.environ["AZURE_OPENAI_API_VERSION"] = azure_api_version
            os.environ["OPENAI_API_TYPE"] = "azure"
    elif planner.lower() == "ollama":
        ollama_model_name = click.prompt(
            "Select the model name (press enter to use 'llama3.2:latest')",
            default="llama3.2:latest",
        )
        os.environ["OLLAMA_MODEL_NAME"] = ollama_model_name

    finder = click.prompt(
        "Choose finder model ('gemini', '4o', or 'ollama') (press enter to use '{}')".format(
            planner
        ),
        type=str,
        default=planner,
    )

    if finder.lower() == "gemini":
        gemini_api_key = click.prompt(
            "Enter your Gemini API key (press enter to use existing)",
            hide_input=True,
            default=os.getenv("GEMINI_API_KEY", ""),
        )
        os.environ["GEMINI_API_KEY"] = gemini_api_key
    elif finder.lower() == "4o":
        version = click.prompt(
            "Is it OpenAI or Azure version? (press enter to use existing)",
            type=str,
            default=os.getenv("OPENAI_API_TYPE", "openai"),
        )
        if version.lower() == "openai":
            openai_api_key = click.prompt(
                "Enter your OpenAI API key (press enter to use existing)",
                hide_input=True,
                default=os.getenv("AZURE_OPENAI_API_KEY", ""),
            )
            os.environ["AZURE_OPENAI_API_KEY"] = openai_api_key
            os.environ["OPENAI_API_TYPE"] = "openai"
        elif version.lower() == "azure":
            azure_api_key = click.prompt(
                "Enter your Azure API key (press enter to use existing)",
                hide_input=True,
                default=os.getenv("AZURE_OPENAI_API_KEY", ""),
            )
            os.environ["AZURE_OPENAI_API_KEY"] = azure_api_key
            azure_model_name = click.prompt(
                "Enter your Azure model name (press enter to use existing)",
                type=str,
                default=os.getenv("AZURE_OPENAI_MODEL_NAME", ""),
            )
            os.environ["AZURE_OPENAI_MODEL_NAME"] = azure_model_name
            azure_endpoint = click.prompt(
                "Enter your Azure endpoint (press enter to use existing)",
                type=str,
                default=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            )
            os.environ["AZURE_OPENAI_ENDPOINT"] = azure_endpoint
            azure_api_version = click.prompt(
                "Enter your Azure API version (press enter to use existing)",
                type=str,
                default=os.getenv("AZURE_OPENAI_API_VERSION", ""),
            )
            os.environ["AZURE_OPENAI_API_VERSION"] = azure_api_version
            os.environ["OPENAI_API_TYPE"] = "azure"
    elif finder.lower() == "ollama":
        ollama_model_name = click.prompt(
            "Select the model name (press enter to use 'llama3.2:latest')",
            default=ollama_model_name,
        )
        os.environ["OLLAMA_MODEL_NAME"] = ollama_model_name


cli.add_command(run)
cli.add_command(setup)

if __name__ == "__main__":
    cli()
