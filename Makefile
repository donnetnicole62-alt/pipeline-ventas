.PHONY: data run test dbt all

data:
	python data/generate_data.py

run:
	python run_pipeline.py

test:
	pytest -v

dbt:
	cd dbt_project && dbt run --profiles-dir . && dbt test --profiles-dir .

all: data run dbt test
