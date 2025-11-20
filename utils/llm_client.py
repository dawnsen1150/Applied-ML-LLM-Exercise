import textwrap
from pathlib import Path

from utils.model import ReformulationQuery, UserResponse
from utils.openai_client import get_openai_client


class LLMClient:
    def __init__(self):
        self.path = Path.cwd()
        self.classification_prompt = self.load_prompt(
            self.path / "llm_prompt", "classification_prompt.txt"
        )
        self.query_modification_prompt = self.load_prompt(
            self.path / "llm_prompt", "query_modification_prompt.txt"
        )

    def load_prompt(self, agent_folder: Path, prompt_filename: str) -> str:
        with open(agent_folder / prompt_filename) as f:
            return textwrap.dedent(f.read().strip())

    def classify(self, query, product_title):
        """This function is used to classify the query as either 'Accurate' or 'Inaccurate' based on the product title.

        Args:
            query (str): The query to classify.
            product_title (str): The product title to compare the query to.

        Returns:
            tuple: A tuple containing the classification and the reasoning.
        """
        human_message = (
            f"The query is: {query}\n"
            f"The product title is: {product_title}\n"
            "Please classify the label as either 'Accurate' or 'Inaccurate', and provide a short reasoning explaining your classification. "
            'Output your reply in JSON with fields: response, reasoning (e.g. {"response": "Inaccurate", "reasoning": "Direct contradiction"}).'
        )
        messages = [
            {"role": "system", "content": self.classification_prompt},
            {"role": "user", "content": human_message},
        ]

        response = get_openai_client(messages, UserResponse)

        return response.response, response.reasoning

    def reformulation(self, query, product_title, reasoning):
        """This function is used to reformulate the user query when the original query and the product information do not match

        Args:
            query (str): The query to reformulate.
            product_title (str): The product title to compare the query to.
            reasoning (str): The reasoning explaining why the query is inaccurate.

        Returns:
            str: The reformulated query.
        """
        human_message = (
            f"Original Query: {query}\n"
            f"Product Title: {product_title}\n"
            f"Reasoning (why it's inaccurate): {reasoning}\n"
            "Please reformulate the query to match the product title based on the instructions provided to you. "
            "Remember to only change the contradictory specification and preserve the original query structure."
        )
        messages = [
            {"role": "system", "content": self.query_modification_prompt},
            {"role": "user", "content": human_message},
        ]

        response = get_openai_client(
            messages=messages, response_format=ReformulationQuery
        )
        return response.text
