FROM python:3.12.1

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure the script is executable
RUN chmod +x ./app/prestart.sh

# Run prestart.sh.sh when the container launches
RUN bash app/prestart.sh
