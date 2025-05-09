#!/bin/bash

uv run uvicorn app.main:app --reload --reload-dir ../client/ --log-level debug --host 0.0.0.0
