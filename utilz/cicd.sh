#!/bin/bash

# Lint the code
lint_code() {
  cd .. && cd src
  flake8 --max-line-length=120 --ignore=E203,E501,W503 .
  if [[ $? -ne 0 ]]; then
    echo "Linting failed."
  else
    echo "Linting passed."
  fi
  cd .. && cd utilz
}

# Build the package
build_package() {
  cd .. && cd src
  python -m build
  if [[ $? -ne 0 ]]; then
    echo "Build failed."
  else
    echo "Build completed successfully."
  fi
  cd .. && cd utilz
}

# Ship the package (placeholder for implementation)
ship_package() {
  repoConfig="../utilz/.pypirc"
  distPath="./dist/*"
  cd .. && cd src
  twine upload --config-file "$repoConfig" "$distPath"
  if [[ $? -ne 0 ]]; then
    echo "Ship failed."
  else
    echo "Ship completed successfully."
  fi
  cd .. && cd utilz
}

# Cleanup build artifacts
cleanup() {
  cd .. && cd src
  rm -rf dist/
  echo "Removed dist directory."
  find . -type d -name "*.egg-info" -exec rm -rf {} +
  echo "Removed *.egg-info directories."
  cd .. && cd utilz
  echo "Cleanup completed."
}

running=true
while $running; do
  echo "CI/CD Menu:"
  echo "1) Lint"
  echo "2) Build"
  echo "3) Build + Ship + Cleanup"
  echo "4) Cleanup only"
  echo "5) Exit"
  read -p "Enter your choice (1-5): " choice
  case $choice in
    1)
      lint_code
      ;;
    2)
      build_package
      ;;
    3)
      build_package
      ship_package
      cleanup
      ;;
    4)
      cleanup
      ;;
    5)
      echo "Exiting..."
      running=false
      ;;
    *)
      echo "Invalid option. Please try again."
      ;;
  esac
done