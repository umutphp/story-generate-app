# Bedtime Story Generation

This is an experimental project for generating bedtime stories for kids. It is a PoC project in which a software developer experiments with applications while improving himself.

Django and Langchain are used as frameworks to perform the related tasks.

# Install and Local Setup

Use `requirements.txt` to install the required packages and setup locally or use can use Docker Compose to run the setup at containers.

### Import Initial Data

To import initial Turkish stories, run the following command.

```bash
 python manage.py import_initial_data
```

To import the initial English stories from [readthetale.com](https://readthetale.com/popular-bedtime-stories/), run the following command.

```bash
python manage.py import_data_readthetale
```

### Ollama container
TODO: Same cache folder with host machine