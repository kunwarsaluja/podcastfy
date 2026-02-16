lint:
	black podcastfy/*.py
	black tests/*.py
	mypy podcastfy/*.py

test:
	poetry run pytest -n auto
    
doc-gen:
	sphinx-apidoc -f -o ./docs/source ./podcastfy
	(cd ./docs && make clean && make html)

diyfire-podcast:
	@if [ -z "$(URL)" ]; then \
		echo "Usage: make diyfire-podcast URL='https://diyfire.ca/learn/your-article' [TTS=edge] [OUTPUT_ROOT=/Users/saluja/Desktop/WorkArea/Franklin/diyfire_podcasts] [PODCAST_NAME='Our Podcast'] [PODCAST_TAGLINE='A diyFIRE audio breakdown']"; \
		exit 1; \
	fi
	@. .venv/bin/activate && \
	python usage/generate_diyfire_podcast.py \
		--url "$(URL)" \
		--tts-model "$(or $(TTS),edge)" \
		--output-root "$(or $(OUTPUT_ROOT),/Users/saluja/Desktop/WorkArea/Franklin/diyfire_podcasts)" \
		--podcast-name "$(or $(PODCAST_NAME),Our Podcast)" \
		--podcast-tagline "$(or $(PODCAST_TAGLINE),A diyFIRE audio breakdown)"
	