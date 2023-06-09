format:
	echo "Formatting..."
	echo "\nFormatting with black...\n"
	poetry run black .
	echo "\nFormatting with ruff...\n"
	poetry run ruff . --fix

format_check:
	echo "\nChecking formatting..."
	echo "\nChecking with black...\n"
	poetry run black --check .
	echo "\nChecking with ruff...\n"
	poetry run ruff .


game:
	poetry run python main.py


simulate:
	poetry run python main.py --simulate --revolutions 100000