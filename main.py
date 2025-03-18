from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import cloudscraper
from typing import List, Dict, Any
import re

# Create a scraper with browser emulation
scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
    }
)

app = FastAPI(
    title="Codeforces API Extended",
    description="An extended API for Codeforces platform",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {
        "Name": "Codeforces API Extended",
        "GitHub": "https://github.com/OneDroid/codeforces-api-extended",
        "Documentation": "https://onedroid.github.io/docs/codeforces-api-extended",
        "Developed by": "Tawhid Monowar (https://github.com/tawhidmonowar)"
    }


def extract_problem_statement(problem_div) -> Dict[str, Any]:
    """Extract problem details from a problem div element"""
    if not problem_div:
        return {}

    # Extract problem title and ID
    header = problem_div.select_one(".title")
    problem_id = header.text.split(".")[0].strip() if header else ""
    title = header.text.split(".", 1)[1].strip() if header and "." in header.text else ""

    # Extract time and memory limits
    limits = {}
    limit_div = problem_div.select_one(".time-limit")
    if limit_div:
        time_limit = limit_div.text.strip()
        if "Time Limit" in time_limit:
            limits["time_limit"] = time_limit.split("Time Limit:")[1].split("second")[0].strip()

    memory_div = problem_div.select_one(".memory-limit")
    if memory_div:
        memory_limit = memory_div.text.strip()
        if "Memory Limit" in memory_limit:
            limits["memory_limit"] = memory_limit.split("Memory Limit:")[1].split("megabyte")[0].strip()

    # Extract problem statement
    statement_div = problem_div.select_one(".problem-statement")
    statement = ""
    if statement_div:
        # Remove the header part which contains time/memory limits
        for div in statement_div.select(".header"):
            div.extract()

        statement = statement_div.text.strip()

    # Extract input specification
    input_spec = ""
    input_div = problem_div.select_one(".input-specification")
    if input_div:
        input_spec = input_div.text.replace("Input", "", 1).strip()

    # Extract output specification
    output_spec = ""
    output_div = problem_div.select_one(".output-specification")
    if output_div:
        output_spec = output_div.text.replace("Output", "", 1).strip()

    # Extract sample tests
    samples = []
    sample_divs = problem_div.select(".sample-test")
    for sample_div in sample_divs:
        input_divs = sample_div.select(".input pre")
        output_divs = sample_div.select(".output pre")

        for i in range(min(len(input_divs), len(output_divs))):
            samples.append({
                "input": input_divs[i].text.strip(),
                "output": output_divs[i].text.strip()
            })

    # Extract notes if available
    notes = ""
    notes_div = problem_div.select_one(".note")
    if notes_div:
        notes = notes_div.text.replace("Note", "", 1).strip()

    return {
        "problem_id": problem_id,
        "title": title,
        "limits": limits,
        "statement": statement,
        "input_specification": input_spec,
        "output_specification": output_spec,
        "samples": samples,
        "notes": notes
    }


@app.get("/contest/{contest_id}")
def all_problem_statements(contest_id: int):
    """Get all problem statements for a specific contest ID"""
    try:
        # Construct URL with the provided contest ID
        url = f"https://codeforces.com/contest/{contest_id}/problems"
        response = scraper.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Failed to fetch contest data. Status code: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract contest name
        contest_name = soup.select_one(".rtable th.left").text.strip() if soup.select_one(
            ".rtable th.left") else "Unknown Contest"

        # Get problem divs
        problem_divs = soup.select(".problemindexholder")

        if not problem_divs:
            return {
                "contest_id": contest_id,
                "contest_name": contest_name,
                "problems": [],
                "message": "No problems found for this contest."
            }

        problems = []
        for problem_div in problem_divs:
            problem_data = extract_problem_statement(problem_div)
            problems.append(problem_data)

        return {
            "contest_id": contest_id,
            "contest_name": contest_name,
            "problems": problems
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching contest data: {str(e)}")


@app.get("/contest/{contest_id}/problem/{problem_index}")
def get_specific_problem(contest_id: int, problem_index: str):
    """Get a specific problem statement from a contest"""
    try:
        # Construct URL with the provided contest ID and problem index
        url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_index}"
        response = scraper.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Failed to fetch problem data. Status code: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Get problem div
        problem_div = soup.select_one(".problemindexholder")

        if not problem_div:
            raise HTTPException(status_code=404, detail="Problem not found")

        problem_data = extract_problem_statement(problem_div)

        return {
            "contest_id": contest_id,
            "problem_index": problem_index,
            "problem_data": problem_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching problem data: {str(e)}")