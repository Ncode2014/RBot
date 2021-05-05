# Using Property Docker 
FROM narima/nekadok:buster

# Clone repo and prepare working directory
RUN git clone -b master https://github.com/Ncode2014/nikabut /home/weebmax/ \
    && chmod 777 /home/weebmax \
    && mkdir /home/weebmax/bin/

# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/weebmax/

# Setup Working Directory
WORKDIR /home/weebmax/

# Finalization
CMD ["python3","-m","userbot"]
