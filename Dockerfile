FROM python:3.9-alpine as builder

WORKDIR /app

COPY docker-requirements.txt .

RUN apk add --no-cache g++ gcc libgfortran musl-dev build-base cmake linux-headers libffi-dev  && \
    python -m venv /venv && \
    /venv/bin/pip install -r docker-requirements.txt

COPY . .

# Stage 2: Create the final image with only necessary files
FROM python:3.9-alpine

WORKDIR /app


COPY --from=builder /venv /venv
COPY --from=builder /app /app

# Add /venv/bin to PATH to ensure that installed dependencies are available
ENV PATH="/venv/bin:$PATH"

EXPOSE 4200

# Your application entry point
CMD [ "prefect", "server", "start" ]